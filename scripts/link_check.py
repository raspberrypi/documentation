#!/usr/bin/env python3

import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
import urllib3
from urllib.parse import urlparse
from collections import namedtuple
from csv import DictWriter

# Silence noisy warnings if we ever fall back to verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Reasonably permissive URL regex - matches http(s) URLs, trims common trailing punctuation
URL_RE = re.compile(
    r"""https?://[^\s"'<>\]\[#]+"""
)

TRAILING_JUNK = "`.,;:!?\"/+'>]"

EXCLUDE_DOMAINS = [
    "localhost",
    "127.0.0.1",
    "192.168.0.1",
    "192.168.1.1",
    "192.168.1.10",
    "raspberrypi.local",
    "yourserver.org",
    "example.com",
    "api.connect.raspberrypi.com"
]

# Use a namedtuple to guarantee the same fieldnames for both the success and error paths
UrlResult = namedtuple("UrlResult", ["url", "status", "live", "final_url", "content_type", "size", "is_download", "error"])

def check_internet():
    test_urls = [
        "https://www.google.com",
        "https://www.cloudflare.com",
        "https://1.1.1.1",
    ]
    for url in test_urls:
        try:
            requests.head(url, timeout=5, allow_redirects=True)
            return True
        except requests.RequestException:
            continue
    return False

def gather_files(path, extension):
    files = set()

    dir_path = Path(path)
    if not dir_path.is_dir():
        print(f"Can't find {path} directory")
        sys.exit(1)
    pattern = "**/*"
    for fp in dir_path.glob(pattern):
        if fp.is_file() and fp.suffix.lower() == extension:
            files.add(fp)

    return files

def extract_urls_from_file(path: Path):
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except (UnicodeDecodeError, OSError) as exc:
        print(f"  ! skipping {path}: {exc}", file=sys.stderr)
        return set()

    found = set()
    for match in URL_RE.findall(text):
        url = match.rstrip(TRAILING_JUNK)
        # Special case for round brackets (thanks, wikipedia)
        if not "(" in url:
            url = url.rstrip(")")
        found.add(url)
    return found

def check_url(url, timeout=8, connect_timeout=None):

    connect_timeout = connect_timeout or timeout
    last_error = ""
    result = None

    for method in ("HEAD", "GET"):
        resp = None
        try:
            resp = requests.request(
                method,
                url,
                timeout=(connect_timeout, timeout),  # (connect, read) tuple
                allow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0 (url-checker script)"},
                stream=True,  # never buffer/download the body automatically
            )

            # HEAD "succeeding" with 405/501 means the server doesn't support
            # it (common on file hosts/CDNs/S3) - fall through to GET.
            if method == "HEAD" and resp.status_code in (405, 501):
                resp.close()
                continue

            live = resp.status_code < 400
            content_type = resp.headers.get("Content-Type", "").lower()
            content_length = int(resp.headers.get("Content-Length", "0"))
            is_download = not content_type.startswith("text/")

            result = UrlResult(
                url=url,
                status=resp.status_code,
                live=live,
                final_url=resp.url if resp.url != url else "",
                content_type=content_type,
                size=content_length,
                is_download=is_download,
                error="",
            )
            break
        except requests.RequestException as exc:
            last_error = str(exc)
            continue  # try GET if HEAD failed outright
        finally:
            # Critical for downloads: close without reading resp.content/.iter_content
            if resp is not None:
                resp.close()

    if result is None:
        result = UrlResult(
            url=url,
            status=None,
            live=False,
            final_url="",
            content_type="",
            size=0,
            is_download=False,
            error=last_error,
        )

    return result

def exclude_domains(urls):
    # Normalise excluded domains once (lowercase, strip any accidental scheme/path)
    excluded = {d.lower().strip().lstrip("www.") for d in EXCLUDE_DOMAINS}

    def is_excluded(url):
        netloc = urlparse(url).netloc.lower()
        # Strip port if present, e.g. "example.com:8080" -> "example.com"
        host = netloc.split(":")[0]
        # Strip a leading "www." so www.example.com matches example.com
        host = host[4:] if host.startswith("www.") else host

        for domain in excluded:
            if host == domain or host.endswith("." + domain):
                return True
        return False

    return {url for url in urls if not is_excluded(url)}


if __name__ == "__main__":
    # Only run if we have internet connection.
    if not check_internet():
        print("No internet connectivity. Can't check URLs")
        sys.exit(1)

    # Get a list of all the adoc files (pre-build).
    search_path = "documentation/asciidoc"
    search_extension = ".adoc"
    files = gather_files(search_path, search_extension)
    if not files:
        print("Couldn't find any {search_extension} files in {search_path}")
        sys.exit(1)

    # Get a list of all the URLs in those adoc files.
    all_urls = set()
    for f in files:
        all_urls.update(extract_urls_from_file(f))

    if not all_urls:
        print("No URLs to check.")
        sys.exit(0)

    # Clean out the example or localhost URLs.
    real_urls = exclude_domains(all_urls)
    num_excluded = len(all_urls) - len(real_urls)
    # Print a quick message so it doesn't look like we've just hung
    print(f"Checking {len(real_urls)} URLs found in {len(files)} {search_extension} files...")

    # Check each URL
    results = []
    with ThreadPoolExecutor(max_workers=10) as pool:
        future_to_url = {pool.submit(check_url, url, 5): url for url in real_urls}
        for future in as_completed(future_to_url):
            results.append(future.result())

    results.sort(key=lambda r: r.url)

    # Formulate output
    dead = [r for r in results if not r.live]
    live = [r for r in results if r.live]

    for name, lst in [("dead", dead), ("live", live)]:
        with open(f"{name}_urls.csv", 'w', newline='') as csvfile:
            writer = DictWriter(csvfile, fieldnames=UrlResult._fields)
            writer.writeheader()
            for r in lst:
                writer.writerow(r._asdict())

    for r in dead:
        status = r.status if r.status is not None else "ERR"
        extra = f" -> {r.final_url}" if r.final_url else ""
        err = f" ({r.error})" if r.error else ""
        print(f"{status:>4} {r.url}{extra}{err}")

    print(f"\nSummary: {len(live)} live, {len(dead)} possibly dead, {num_excluded} excluded from check, {len(all_urls)} total")
    sys.exit(0)

