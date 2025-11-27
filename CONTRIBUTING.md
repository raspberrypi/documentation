# Contributing to the Raspberry Pi Documentation

Welcome to the [public repository](https://github.com/raspberrypi/documentation/) for the Raspberry Pi documentation. This repository contains the Asciidoc source and the Jekyll-based build tools for the HTML documentation hosted at the [Raspberry Pi documentation site](https://www.raspberrypi.com/documentation/).

The public repository is a mirror of an internal repository from which the site is built. The master branch of this repository is automatically kept up to date with the latest published content on the [website](https://www.raspberrypi.com/documentation/).

We encourage and value all types of contributions from our community. Please make sure to read the following section before making your contribution. It makes it a lot easier for the Raspberry Pi Technical Documentation team (the maintainers) and smooths out the experience for all involved. We look forward to your contributions.

## Contribute

To suggest changes to this documentation:

1. Create a fork of the `raspberrypi/documentation` repository on your GitHub account.

1. Make changes in your fork. Start by branching from the default `master` branch.

1. Read our [style guide](https://github.com/raspberrypi/style-guide/blob/master/style-guide.md) to ensure that your changes are consistent with the rest of our documentation. Since Raspberry Pi is a British company, be sure to include all of your extra `u`s and transfigure those `z`s (pronounced 'zeds') into `s`s!

1. [Open a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) against this repository.

1. The maintainers assess the PR. We hope to get back to you within a fortnight, but this might vary depending on the size of your PR, the time of year, and the availability of the maintainers.

1. What happens next depends on the content of the PR and whether it inspires any wider changes:

   * If we have questions about the PR, we work with you to understand what you are going for and how best the docs can achieve it.
   * If your PR can be included as-is, we use the patch mechanism to bring it across to the internal repository and commit it there. When the change is published on the Raspberry Pi Documentation website, it is mirrored to the public repository with you listed as author. We then close the original PR.
   * If your PR needs significant editing or prompts a wider change to the documentation, we take on that work in our internal repository. We'll let you know if that's the case and how long we expect it to take.
   If we don't bring your initial changes over as a patch, we use the [co-author mechanism](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors) to ensure you get credit for your contribution.

Alternatively, [open an issue](https://github.com/raspberrypi/documentation/issues) to discuss proposed changes.

## Build

The Raspberry Pi Documentation website is built from Asciidoc source using:

* [Asciidoctor](https://asciidoctor.org/)
* [Jekyll](https://jekyllrb.com/)
* [jekyll-asciidoc](https://github.com/asciidoctor/jekyll-asciidoc)
* Python

The website deploys to [www.raspberrypi.com/documentation](https://www.raspberrypi.com/documentation) from an internal repository that is mirrored to the [public repository](https://github.com/raspberrypi/documentation/).

### Install dependencies

To build the Raspberry Pi documentation locally, you'll need Ruby, Python, and the Ninja build system.

#### Linux

Use `apt` to install the dependencies:

```console
$ sudo apt install -y ruby ruby-dev python3 python3-pip make ninja-build
```

Then, append the following lines to your `~/.bashrc` file (or equivalent shell configuration):

```bash
export GEM_HOME="$(ruby -e 'puts Gem.user_dir')"
export PATH="$PATH:$GEM_HOME/bin"
```

Close and re-launch your terminal window to use the new dependencies and configuration.

#### macOS

If you don't already have it, we recommend installing the [Homebrew](https://brew.sh/) package manager:

```console
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Next, use Homebrew to install Ruby:

```console
$ brew install ruby
```

After installing Ruby, follow the instructions provided by Homebrew to make your new Ruby version easily accessible from the command line.

Then, use Homebrew to install the most recent version of Python:

```console
$ brew install python
```

Then, install the [Ninja build system](https://formulae.brew.sh/formula/ninja#default):

```console
$ brew install ninja
```

### Set up environment

Use the `gem` package manager to install the [Ruby bundler](https://bundler.io/), which this repository uses to manage Ruby dependencies:

```console
$ gem install bundler
```

And then install the required Ruby gems:

```console
$ bundle install
```

Configure a Python virtual environment for this project:

```console
$ python -m venv .env
```

Activate the virtual environment:

```console
$ source .env/bin/activate
```

> [!TIP]
> When you're using a virtual environment, you should see a `(.env)` prefix at the start of your terminal prompt. At any time, run the `deactivate` command to exit the virtual environment.

In the virtual environment, install the required Python modules:

```console
$ pip3 install -r requirements.txt
```

### Build HTML

> [!IMPORTANT]
> If you configured a Python virtual environment as recommended in the previous step, **always** run `source .env/bin/activate` before building. You must activate the virtual environment to access to all of the Python dependencies installed in that virtual environment.

To build the documentation and start a local server to preview the built site, run the following command:

```console
$ make serve_html
```

You can access the virtual server at [http://127.0.0.1:4000/documentation/](http://127.0.0.1:4000/documentation/).

> [!TIP]
> To delete and rebuild the documentation site, run `make clean`, then re-run the build command. You'll need to do this every time you add or remove an Asciidoc, image, or video file.


### Build the Pico C SDK Doxygen documentation

The Raspberry Pi documentation site includes a section of generated Asciidoc that we build from the [Doxygen Pico SDK documentation](https://github.com/raspberrypi/pico-sdk).

We use the tooling in this repository and [doxygentoasciidoc](https://github.com/raspberrypi/doxygentoasciidoc) to generate that documentation section. By default, local documentation builds don't include this section because it takes a bit longer to build (tens of seconds) than the rest of the site.

Building the Pico C SDK Doxygen documentation requires the following additional package dependencies:

```console
$ sudo apt install -y cmake gcc-arm-none-eabi doxygen graphviz
```

Then, initialise the Git submodules used in the Pico C SDK section build:

```console
$ git submodule update --init
```

Run the following command to build the Pico C SDK section Asciidoc files from the Doxygen source:

```console
$ make build_doxygen_adoc
```

The next time you build the documentation site, you'll see the Pico C SDK section in your local preview.

> [!TIP]
> To delete and rebuild the generated files, run `make clean_doxygen_xml`, then re-run the build command.

