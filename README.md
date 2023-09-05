# Welcome to the Raspberry Pi Documentation

This repository contains the Asciidoc source and the toolchain to build the [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/). For details of how to contribute to the documentation see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

**NOTE:** This repository has undergone some recent changes. See our [blog post](https://www.raspberrypi.com/blog/bring-on-the-documentation/) for more details.

## Building the Documentation

Instructions on how to checkout the `documentation` repo, and then install the toolchain needed to convert from Asciidoc to HTML and build the documentation site.

### Checking out the Repository

Install `git` if you don't already have it, and check out the `documentation` repo as follows,
```
$ git clone https://github.com/raspberrypi/documentation.git
$ cd documentation
```

### Installing the Toolchain

#### On Linux

This works on both regular Debian or Ubuntu Linux — and has been tested in a minimal Docker container — and also under Raspberry Pi OS if you are working from a Raspberry Pi.

You can install the necessary dependencies on Linux as follows,

```
$ sudo apt install -y ruby ruby-dev python3 python3-pip make ninja-build
```

then add these lines to the bottom of your `$HOME/.bashrc`,
```
export GEM_HOME="$(ruby -e 'puts Gem.user_dir')"
export PATH="$PATH:$GEM_HOME/bin"
```

and close and relaunch your Terminal window to have these new variables activated. Finally, run
```
$ gem install bundler
```
to install the latest version of the Ruby `bundle` command.

#### On macOS

If you don't already have it, install the [Homebrew](https://brew.sh/) package manager: 

```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Next, install Ruby:

```
$ brew install ruby
```

And install the [Ruby bundler](https://bundler.io/):

```
$ gem install bundler
```

##### Set up Homebrew Version of Ruby

Because macOS provides its own version of Ruby, Homebrew doesn't automatically set up symlinks to access the version you just installed with the `ruby` command. But after a successful install, Homebrew outputs the commands you'll need to run to set up the symlink yourself. If you use the default macOS `zsh` shell on Apple Silicon, you can set up the symlink with the following command:

```
$ echo 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' >> ~/.zshrc
```

If you run macOS on an Intel-based Mac, replace `opt/homebrew` with `usr/local` in the above command.

If you run a shell other than the default, check which config file to modify for the command. For instance, `bash` uses `~/.bashrc` or `~/.bash_profile`.

Once you've made the changes to your shell configuration, open a new terminal instance and run the following command:

```
$ ruby --version
```

You should see output similar to the following:

```
ruby 3.2.2 (2023-03-30 revision e51014f9c0) [arm64-darwin22]
```

As long as you see a Ruby version greater than or equal to 3.2.2, you've succeeded.

##### Install Homebrew Dependencies

Next, use Homebrew to install the other dependencies.
Start with the latest version of Python:

```
$ brew install python@3
```

Then install the [Ninja build system](https://formulae.brew.sh/formula/ninja#default):

```
$ brew install ninja
```

Then install the [Gumbo HTML5 parser](https://formulae.brew.sh/formula/gumbo-parser#default):

```
$ brew install gumbo-parser
```

And finally, install the [YAML module for Python 3](https://formulae.brew.sh/formula/pyyaml#default):

```
$ pip3 install pyyaml
```

Now you've installed all of the dependencies you'll need from Homebrew.

### Install Scripting Dependencies

After installing the toolchain, install the required Ruby gems and Python modules. Make sure you're in the top-level directory of this repository (the one containing `Gemfile.lock` and `requirements.txt`), and run the following command to install the Ruby gems (this may take several minutes):

```
$ bundle install
```

Then, run the following command to install the remaining required Python modules:

```
$ pip3 install --user -r requirements.txt
```

### Building the Documentation Site

After you've installed both the toolchain and scripting dependencies, you can build the documentation with the following command:

```
$ make
```

This automatically uses [Ninja build](https://ninja-build.org/) to convert the source files in `documentation/asciidoc/` to a suitable intermediate structure in `build/jekyll/` and then uses [Jekyll AsciiDoc](https://github.com/asciidoctor/jekyll-asciidoc) to convert the files in `build/jekyll/` to the final output HTML files in `documentation/html/`.

You can also start a local server to view the built site:

```
$ make serve_html
```

As the local server launches, the local URL will be printed in the terminal -- open this URL in a browser to see the locally-built site.

You can also use `make` to delete the `build/` and `documentation/html/` directories:

```
$ make clean
```

### Building with Doxygen

If you want to build the Pico C SDK Doxygen documentation alongside the main documentation site you can do so with,

```
$ make build_doxygen_adoc
$ make
```

and clean up afterwards by using,

```
$ make clean_everything
```

which will revert the repository to a pristine state.

## Licence

The Raspberry Pi [documentation](./documentation/) is [licensed](https://github.com/raspberrypi/documentation/blob/develop/LICENSE.md) under a Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA). While the toolchain source code — which is everything outside of the top-level `documentation/` subdirectory — is Copyright © 2021 Raspberry Pi Ltd and licensed under the [BSD 3-Clause](https://opensource.org/licenses/BSD-3-Clause) licence.
