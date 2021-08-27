# Welcome to the Raspberry Pi Documentation

This repository contains the Asciidoc source and the toolchain to build the [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/). For details of how to contribute to the documentation see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

**NOTE:** This repository has undergone some recent changes. See our [blog post](https://www.raspberrypi.org/blog/bring-on-the-documentation/) for more details.

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

You can install the necessary dependencies on Linux as follows,

```
$ sudo apt-get -qq -y install ruby ruby-bundler ruby-dev build-essential python3 git ninja-build
```

This works on both regular Ubuntu Linux — and has been tested in a minimal Docker container — and also under Raspberry Pi OS if you are working from a Raspberry Pi.

#### On macOS

If you don't already have it installed you should go ahead and install [HomeBrew](https://brew.sh/), 

```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Then you need to install Ruby,

```
$ brew install ruby@2.7
```

**NOTE:** Homebrew defaults to Ruby 3.0 which is incompatible with Asciidoctor.

##### Set up Homebrew Version of Ruby

If you're using `csh` or `tcsh` add the following lines to your `.cshrc` or `.tcshrc`,

```
setenv PATH /usr/local/opt/ruby/bin:${PATH}
setenv PATH ${PATH}:/usr/local/lib/ruby/gems/2.7.0/bin
setenv LDFLAGS -L/usr/local/opt/ruby@2.7/lib
setenv CPPFLAGS -I/usr/local/opt/ruby@2.7/include
setenv PKG_CONFIG_PATH /usr/local/opt/ruby@2.7/lib/pkgconfig
```

or if you're using `bash` add the following lines to your `.bash_profile`,

```
export PATH="/usr/local/opt/ruby/bin:$PATH"
export PATH="$PATH:/usr/local/lib/ruby/gems/2.7.0/bin"
export PATH="/usr/local/opt/ruby@2.7/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/ruby@2.7/lib"
export CPPFLAGS="-I/usr/local/opt/ruby@2.7/include"
export PKG_CONFIG_PATH="/usr/local/opt/ruby@2.7/lib/pkgconfig"
```

##### Install Dependencies

Go ahead and `brew install` the other dependencies,

```
$ brew install python@3
$ brew install ninja
```

### Configuring the Repository

After you've installed the toolchain, you'll need to install the required Ruby gems. Make sure you're in the `documentation` directory and then run,
```
$ bundle install
```

### Building the Documentation Site

After you've installed the toolchain and configured the repository you can build the documentation with,

```
$ make
```

This will automatically convert the `build/jekyll/` files to HTML and put them into `documentation/html/`.

You can also start a local server to view the compiled site by running,
```
$ make serve_html
```

As the local server launches, the local URL will be printed in the terminal -- open this URL in a browser to see the locally-built site.

To build without an active internet connection, run
```
$ OFFLINE_MODE=1 make
```
which will copy the `fonts.html` and `header.html` files from `offline_includes` (instead of downloading them from esi.raspberrypi.org).

## License

The Raspberry Pi documentation is [licensed](https://github.com/raspberrypi/documentation/blob/develop/LICENSE.md) under a Creative Commons Attribution 4.0 International Licence. While the toolchain source code is Copyright © 2020 Raspberry Pi (Trading) Ltd. and licensed under the [BSD 3-Clause](https://opensource.org/licenses/BSD-3-Clause) licence.
