# Raspberry Pi Documentation

This is the official documentation for the Raspberry Pi, written by the [Raspberry Pi Foundation](https://www.raspberrypi.org/) with community contributions.

## Contents

- [Setup / Quickstart](./_content/setup)
    - Getting started with your Raspberry Pi, including what you need and how to get it booted
- [Installation](./_content/installation)
    - Installing an operating system on your Raspberry Pi
- [Usage Guide](./_content/usage)
    - Explore the desktop and try out all the main applications
- [Configuration](./_content/configuration)
    - Configuring the Pi's settings to suit your needs
- [Remote Access](./_content/remote-access)
    - Accessing your Pi remotely via SSH, VNC or over the web
- [Linux](./_content/linux)
    - Fundamental Linux usage for beginners and more advanced information for power users
- [Raspbian](./_content/raspbian)
    - Information about the recommended operating system for Raspberry Pi
- [Hardware](./_content/hardware)
    - Technical specifications about the Raspberry Pi hardware and the camera module
- [Technical FAQ](./_content/technical-faq)
    - Answers to frequently asked technical questions

## General Documentation Help

In addition to the topics above, we have a set of [Frequently Asked Questions](faqs/README.md), and a [Glossary](glossary/README.md) to help with any technical terms you may encounter in our documentation.

## Contributions

If you have anything to fix or details to add, first [file an issue](http://github.com/raspberrypi/documentation/issues) on GitHub to see if it is likely to be accepted, then file a pull request with your change (one PR per issue).

This is not intended to be an open wiki; we want to keep it concise and minimal but will accept fixes and suitable additions.

See our [contributing policy](./CONTRIBUTING).

## Licence

Unless otherwise specified, everything in this repository is covered by the following licence:

[![Creative Commons Attribution-ShareAlike 4.0 International](https://licensebuttons.net/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

***Raspberry Pi Documentation*** by the [Raspberry Pi Foundation](https://www.raspberrypi.org/) is licensed under a [Creative Commons Attribution 4.0 International Licence](http://creativecommons.org/licenses/by-sa/4.0/).

Based on a work at https://github.com/raspberrypi/documentation

## Development

Dependencies:

- Preferably, a Node.js version manager (eg. [nvm](https://github.com/creationix/nvm))
- A Node.js version installed matching that in `.nvmrc`

Install dependencies:
```
npm install
```

Start a local server that builds the site and watches for changes:
```
npm run dev
```

Visit: http://127.0.0.1:8000
