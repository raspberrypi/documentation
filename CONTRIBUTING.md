# Contributing to the Raspberry Pi Documentation

The Raspberry Pi Documentation website is built from Asciidoc source using:

* [Asciidoctor](https://asciidoctor.org/)
* [Jekyll](https://jekyllrb.com/)
* [jekyll-asciidoc](https://github.com/asciidoctor/jekyll-asciidoc)
* Python

The website automatically deploys to [www.raspberrypi.com/documentation](https://www.raspberrypi.com/documentation) using GitHub Actions when new commits appear in the `master` branch.

## Contribute

To contribute or update documentation:

1. Create a fork of this repository on your GitHub account.

1. Make changes in your fork. Start from the default `develop` branch.

1. Read our [style guide](https://github.com/raspberrypi/style-guide/blob/master/style-guide.md) to ensure that your changes are consistent with the rest of our documentation. Since Raspberry Pi is a British company, be sure to include all of your extra `u`s and transfigure those `z`s (pronounced 'zeds') into `s`s!

1. [Open a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) against this repository.

1. The maintainers will assess and copy-edit the PR. This can take anywhere from a few minutes to a few days, depending on the size of your PR, the time of year, and the availability of the maintainers.

1. After making any requested improvements to your PR, the maintainers will accept the PR and merge your changes into `develop`.

1. When the maintainers next release the documentation by merging `develop` into `master`, your changes will go public on the production documentation site.

Alternatively, [open an issue](https://github.com/raspberrypi/documentation/issues) to discuss proposed changes.

## Build

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

Configure a Python virtual environment for this project:

```console
$ python -m venv .env
```

Activate the virtual environment:

```console
$ source .env/bin/activate
```

> [!TIP]
> When you're using a virtual environment, you should see a `(.venv)` prefix at the start of your terminal prompt. At any time, run the `deactivate` command to exit the virtual environment.

In the virtual environment, install the [YAML module for Python 3](https://formulae.brew.sh/formula/pyyaml#default):

```console
$ pip3 install pyyaml
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

