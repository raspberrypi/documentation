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
$ gem install bundler -v 2.2.15
```
to install the latest version of the Ruby `bundle` command.

#### On macOS

If you don't already have it installed you should go ahead and install [HomeBrew](https://brew.sh/), 

```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Then you need to install Ruby,

```
$ brew install ruby@2.7
$ gem install bundler -v 2.2.15
```

**NOTE:** Homebrew defaults to Ruby 3.0 which is incompatible with Asciidoctor.

**IMPORTANT:** Homebrew has problems using `/bin/zsh`, you may have to change your default shell to `/bin/bash`.

##### Set up Homebrew Version of Ruby

If you're using `csh` or `tcsh` add the following lines to your `.cshrc` or `.tcshrc`,

```
setenv PATH /usr/local/bin:/usr/local/sbin:$PATH

setenv PATH /usr/local/opt/ruby/bin:${PATH}
setenv PATH ${PATH}:/usr/local/lib/ruby/gems/2.7.0/bin
setenv LDFLAGS -L/usr/local/opt/ruby@2.7/lib
setenv CPPFLAGS -I/usr/local/opt/ruby@2.7/include
setenv PKG_CONFIG_PATH /usr/local/opt/ruby@2.7/lib/pkgconfig
```

or if you're using `bash` add the following lines to your `.bash_profile`,

```
export PATH="/usr/local/bin:/usr/local/sbin:$PATH"

export PATH="/usr/local/opt/ruby/bin:$PATH"
export PATH="$PATH:/usr/local/lib/ruby/gems/2.7.0/bin"
export PATH="/usr/local/opt/ruby@2.7/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/ruby@2.7/lib"
export CPPFLAGS="-I/usr/local/opt/ruby@2.7/include"
export PKG_CONFIG_PATH="/usr/local/opt/ruby@2.7/lib/pkgconfig"
```
NOTE: If you are running macOS on an Apple Silicon based Mac, rather than an Intel Mac, substitute `/opt/homebrew/` for `/usr/local` in the lines dealing with `ruby@2.7` in the above block.

and then open a new Terminal window to make sure you're using the right version of Python and Ruby.

##### Install Dependencies

Go ahead and `brew install` the other dependencies,

```
$ brew install python@3
$ brew install ninja
$ brew install gumbo-parser
$ pip3 install pyyaml
```

### Install Scripting Dependencies

After you've installed the toolchain (on either Linux or macOS), you'll need to install the required Ruby gems and Python modules. Make sure you're in the top-level `documentation/` directory (i.e. the one containing `Gemfile.lock` and `requirements.txt`) and then run,
```
$ bundle install
```
(which may take several minutes), followed by,
```
$ pip3 install --user -r requirements.txt
```

### Building the Documentation Site

After you've installed both the toolchain and scripting dependencies, you can build the documentation with,

```
$ make
```

This will automatically use [Ninja build](https://ninja-build.org/) to convert the source files in `documentation/asciidoc/` to a suitable intermediate structure in `build/jekyll/`, and then use [Jekyll AsciiDoc](https://github.com/asciidoctor/jekyll-asciidoc) to convert the files in `build/jekyll/` to the final output HTML files in `documentation/html/`.

You can also start a local server to view the built site by running,
```
$ make serve_html
```

As the local server launches, the local URL will be printed in the terminal -- open this URL in a browser to see the locally-built site.

You can revert your repository to a pristine state by running,
```
$ make clean
```
which will delete the `build/` and `documentation/html/` directories.

### Building with Doxygen

If you want to build the Pico C SDK Doxygen documentation alongside the main documentation site you can do so with,

```
$ make build_doxygen_doc
$ make
```

and clean up afterwards by using,

```
$ make clean_everything
```

which will revert the repository to a pristine state.

## Licence

The Raspberry Pi [documentation](./documentation/) is [licensed](https://github.com/raspberrypi/documentation/blob/develop/LICENSE.md) under a Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA). While the toolchain source code — which is everything outside of the top-level `documentation/` subdirectory — is Copyright © 2021 Raspberry Pi Ltd and licensed under the [BSD 3-Clause](https://opensource.org/licenses/BSD-3-Clause) licence.
