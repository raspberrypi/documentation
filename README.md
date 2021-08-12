# README

Instructions on how to checkout the `documentation` repo, and then install the toolchain needed to convert from Asciidoc to HTML and build the documentation site.

## Checking out the repository

Install `git` if you don't already have it, and check out the `documentation` repo as follows,
```
$ git clone https://github.com/raspberrypi/documentation.git
$ cd documentation
```

## Installing the toolchain

### On Linux

You can install the necessary dependencies on Linux as follows,

```
$ sudo apt-get -qq -y install ruby ruby-bundler ruby-dev build-essential python3 git ninja-build
```

This works on both regular Ubuntu Linux — and has been tested in a minimal Docker container — and also under Raspberry Pi OS if you are working from a Raspberry Pi.

### On macOS

If you don't already have it installed you should go ahead and install [HomeBrew](https://brew.sh/), 

```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Then you need to install Ruby,

```
$ brew install ruby@2.7
```

**NOTE:** Homebrew defaults to Ruby 3.0 which is incompatible with Asciidoctor.

#### Set up Homebrew version of Ruby

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

#### Install dependencies

Go ahead and `brew install` the other dependencies,

```
$ brew install python@3
$ brew install ninja
```

## Configuring the repository

After you've installed the toolchain, you'll need to install the required Ruby gems. Make sure you're in the `documentation` directory and then run,
```
$ bundle install
```

## Building the documentation

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
