# FAQs

## Table of contents

### [What is a Raspberry Pi?](#introduction)

### [Buying your first Raspberry Pi](#buying)

- Where can I buy a Raspberry Pi, and how much does it cost?
- What do I get when I buy one?
- I'm worried I have a fake Raspberry Pi!

### [Commercial and industry applications, resale](#commercial)
- I want to be a Raspberry Pi reseller.
- What manufacturing standards etc. does the Raspberry Pi comply with?
- Can I use a Raspberry Pi in a commercial product?
- Is a Raspberry Pi suitable for industrial applications?

### [The computer hardware](#hardware)

- What are the differences between Raspberry Pi models?
- What hardware documentation is available?
- What hardware interfaces does it have?
- Can I use a Raspberry Pi for audio or video input?
- Where is the on/off switch?
- What are the dimensions of the Raspberry Pi?

### [Performance](#pi-performance)

- How powerful is it?
- Can I use my Raspberry Pi as a desktop replacement?
- Can I add extra RAM?
- Can I connect multiple Raspberry Pis together to make a faster computer?
- Why does my Raspberry Pi run at a slower clock speed than advertised?
- Does it overclock?
- What is its operating temperature? Does it need a heatsink?

### [Software](#pi-software)

- What operating system (OS) does it use?
- Can I run Windows 10 on the Raspberry Pi?
- Updates? Upgrades? What do I do?
- I heard about something called `rpi-update`. When should I use that?
- The processors on the latest Raspberry Pi models are 64-bit, but I cannot find an official 64-bit OS.
- Can I run PC software on the Raspberry Pi?
- Will it run Android or Android Things?
- Will it run old software?
- My `.exe` file won't run!
- Can I share files from my Raspberry Pi with my Windows machines?
- Why does `cpuinfo` report I have a bcm2835?
- How do I run a program at startup?
- How do I run a program at a specific time?

### [Video](#pi-video)

- What displays can I use?
- Does the HDMI port support CEC?
- Why is there no VGA support?
- Can I add a touchscreen?
- What codecs can it play?

### [Audio](#pi-audio)

- Is sound over HDMI supported?
- What about standard audio in and out?

### [Power](#pi-power)

- Is it safe to just pull the power?
- What about unplanned power interruptions?
- What are the power requirements?
- Can I power the Raspberry Pi from a USB hub?
- Can I power the Raspberry Pi from batteries as well as from a wall socket?
- Is Power over Ethernet (PoE) possible?
- What voltage devices can I attach to the GPIO pins, and how much current can I pull?

### [SD cards and storage](#sd-cards)

- What size of SD card do I need?
- What size of SD card can it support?
- Can I boot a Raspberry Pi from a USB-attached hard drive instead of the SD card?
- What happens if I brick the device?

### [Networking and wireless connectivity](#networking)

- Does the device support networking?
- Is there built-in wireless networking?
- Is there built-in Bluetooth?
- I don't seem to get full-speed gigabit networking on my Raspberry Pi 3B+.
- Does the device have support for any form of netbooting or PXE?

### [Camera Module](#cameramodule)

- What is the Camera Module?
- What model of camera does the Camera Module use?
- What resolutions are supported?
- What picture formats are supported?
- How do I use the Camera Module?
- How much power does the Camera Module use?

### [Troubleshooting](#troubleshoot)

- What is the username and password for the Raspberry Pi?
- Why does nothing happen when I type in my password?
- Why does my Raspberry Pi not start up/boot?
- Why is my Raspberry Pi hot?
- I keep getting a lightning bolt symbol and messages about power...
- My SD card seems to have stopped working.
- I've imaged an SD card with Raspberry Pi OS/NOOBS, but when I look at it with my Windows PC, it's not all there!

---

<a name="introduction"></a>
## What is a Raspberry Pi?

Raspberry Pi is the third best-selling computer brand in the world. The Raspberry Pi is a credit card–sized computer that plugs into your TV or display, and a keyboard and mouse. You can use it to learn coding and to build electronics projects, and for many of the things that your desktop PC does, like spreadsheets, word processing, browsing the internet, and playing games. It also plays high-definition video. The Raspberry Pi is being used by adults and children all over the world to learn programming and digital making. You can learn how to set up and use your Raspberry Pi [here](https://www.raspberrypi.org/help/).

<a name="buying"></a>
## Buying your first Raspberry Pi

### Where can I buy a Raspberry Pi, and how much does it cost?

Go to our [products page](https://www.raspberrypi.org/products/) and choose the product(s) you want to buy. Then select your country from the drop-down menu. You will be presented with our approved resellers for your country.

The following prices are exclusive of any local taxes and shipping/handling fees.

|Product|Price|
|-------|-----|
| Raspberry Pi Model A+| $20 |
| Raspberry Pi Model B+ |$25 |
| Raspberry Pi 2 Model B| $35 |
| Raspberry Pi 3 Model B | $35 |
| Raspberry Pi 3 Model A+ | $25 |
| Raspberry Pi 3 Model B+ | $35 |
| Raspberry Pi 4 Model B 2GB | $35 |
| Raspberry Pi 4 Model B 4GB | $55 |
| Raspberry Pi 4 Model B 8GB | $75 |
| Raspberry Pi Zero | $5 |
| Raspberry Pi Zero W |$10 |
| Raspberry Pi Zero WH |$15 |

### What do I get when I buy one?

You get the Raspberry Pi board itself. The [official power supply](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/) and an SD card are not included, but they can be purchased at the same time from most places that sell the Raspberry Pi. You can also purchase pre-loaded SD cards; we recommend buying these from us or our licensed distributors rather than from third parties, as our software is updated regularly and cards sold by third parties can quickly become outdated.

An official case for the Raspberry Pi is available separately [from our distributors](https://www.raspberrypi.org/products/). There are also lots of home-brew case discussions on the forum, as well as several third-party cases available. There are also loads of awesome [3D-printable cases](https://www.raspberrypi.org/blog/3d-printed-raspberry-pi-cases/) that community members have designed.

### I'm worried I have a fake Raspberry Pi!

Don't worry, as far as we know, there are no fake Raspberry Pis. The processors used on the Raspberry Pi range are only available from one supplier, and only in quantities of several million at a time, which, together with the low price of the Raspberry Pi means it's not cost-effective for clones to be made. There are a number of competitor products that use similar names, but no actual clones or fakes.

<a name="commercial"></a>
## Commercial and industry applications, resale

### I want to be a Raspberry Pi reseller.

We have an exclusive manufacturing and distribution arrangement with [RS](http://uk.rs-online.com/web/generalDisplay.html?id=raspberrypi) and [Farnell](https://www.element14.com/community/community/raspberry-pi). Resellers buy the Raspberry Pi in bulk from them (which reduces shipping costs to nearly nothing) and sell on. You do not need any special licence to resell, and the distributors are very happy to sell on to resellers. If you are interested in joining our [Approved Reseller](https://www.raspberrypi.org/blog/approved-reseller/) programme, contact us by emailing info@raspberrypi.com.

### What manufacturing standards etc. does the Raspberry Pi comply with?

We have put the Raspberry Pi models through extensive compliance testing, for Europe, the USA, and other countries around the world. You can find many of the reports [here](../hardware/raspberrypi/conformity.md).

### Can I use a Raspberry Pi in a commercial product?

This is a very common question, and the answer is yes! Once you have bought a Raspberry Pi, it's yours to do with as you wish. Note, however, that a lot of the software in the Raspberry Pi OS distribution is GPL-licenced, which comes with certain requirements, most significantly that you must provide access to the source code if requested. This is usually pretty easy to do.

### Is a Raspberry Pi suitable for industrial applications?

Yes — it depends on your use case. Raspberry Pis have been used successfully in industrial environments, but the final decision must be in the hands of the end user as to whether the device is suitable for the task at hand. See our [Compute Module documentation](../hardware/computemodule/README.md) for more details on our Raspberry Pi model specifically designed for use in commercial and industrial products.

<a name="hardware"></a>
## The computer hardware

### What are the differences between Raspberry Pi models?

These are the [models of the Raspberry Pi](https://www.raspberrypi.org/products/) which are currently available: the Pi 3 Model B, the Pi 2 Model B, the Pi Zero, the Pi Zero W and the Pi 1 Model B+ and A+.

| Product | SoC | Speed | RAM | USB Ports | Ethernet | Wireless | Bluetooth |
|---------|-----|-------|-----|:--------:|:--------:|:--------:|:---------:|
| Raspberry Pi Model A+ | BCM2835 | 700MHz | 512MB | 1 | No | No | No |
| Raspberry Pi Model B+ | BCM2835 | 700MHz | 512MB | 4 |100Base-T | No | No |
| Raspberry Pi 2 Model B | BCM2836/7 | 900MHz | 1GB | 4 |100Base-T| No | No |
| Raspberry Pi 3 Model B | BCM2837A0/B0 | 1200MHz | 1GB | 4 |100Base-T| 802.11n| 4.1 |
| Raspberry Pi 3 Model A+ | BCM2837B0 | 1400MHz | 512MB | 1 | No | 802.11ac/n | 4.2 |
| Raspberry Pi 3 Model B+ | BCM2837B0 | 1400MHz | 1GB | 4 |1000Base-T | 802.11ac/n | 4.2 |
| Raspberry Pi 4 Model B | BCM2711 | 1500MHz | 2GB | 2xUSB2, 2xUSB3 |1000Base-T | 802.11ac/n | 5.0 |
| Raspberry Pi 4 Model B | BCM2711 | 1500MHz | 4GB | 2xUSB2, 2xUSB3 |1000Base-T | 802.11ac/n | 5.0 |
| Raspberry Pi 4 Model B | BCM2711 | 1500MHz | 8GB | 2xUSB2, 2xUSB3 |1000Base-T | 802.11ac/n | 5.0 |
| Raspberry Pi Zero | BCM2835 | 1000MHz | 512MB | 1 | No | No | No |
| Raspberry Pi Zero W | BCM2835 | 1000MHz | 512MB | 1 | No | 802.11n | 4.1 |
| Raspberry Pi Zero WH | BCM2835 | 1000MHz | 512MB | 1 | No | 802.11n | 4.1 |

The Model A+ is the low-cost variant of the Raspberry Pi. It has 512MB RAM (as of August 2016: earlier models have 256MB), one USB port, 40 GPIO pins, and no Ethernet port.

The Model B+ is the final revision of the original Raspberry Pi. It has 512MB RAM, four USB ports, 40 GPIO pins, and an Ethernet port.

In February 2015, it was superseded by the Raspberry Pi 2 Model B, the second generation of the Raspberry Pi. The Raspberry Pi 2 shares many specs with the Raspberry Pi 1 B+, and originally used a 900MHz quad-core Arm Cortex-A7 CPU and has 1GB RAM. Some recent version of the Raspberry Pi 2 (v1.2) now use a 900MHz Arm Cortex-A53 CPU.

The Raspberry Pi 3 Model B was launched in February 2016. It uses a 1.2GHz 64-bit quad-core Arm Cortex-A53 CPU, has 1GB RAM, integrated 802.11n wireless LAN, and Bluetooth 4.1.

The Raspberry Pi 3 Model B+ was launched in March 2018. It uses a 1.4GHz 64-bit quad-core Arm Cortex-A53 CPU, has 1GB RAM, gigabit Ethernet, integrated 802.11ac/n wireless LAN, and Bluetooth 4.2.

The Raspberry Pi 4 Model B was launched in June 2019. It uses a 1.5GHz 64-bit quad-core Arm Cortex-A72 CPU, has three RAM options (2GB, 4GB, 8GB), gigabit Ethernet, integrated 802.11ac/n wireless LAN, and Bluetooth 5.0. Originally launched with a 1GB option, this has been superceded by the 2GB at the original 1GB price. The 1GB device is still available as a special order.

The Raspberry Pi Zero and Raspberry Pi Zero W/WH are half the size of a Model A+, with a 1GHz single-core CPU and 512MB RAM, and mini-HDMI and USB On-The-Go ports and a camera connector. The Raspberry Pi Zero W also has integrated 802.11n wireless LAN and Bluetooth 4.1. The Raspberry Pi Zero WH is identical to the Zero W, but comes with a pre-soldered header.

The Model A/A+ has one USB port, the Model B has two ports, and the Model B+, Raspberry Pi 2 Model B, and Raspberry Pi 3 Model B have four ports. These can be used to connect most USB 2.0 devices. Additional USB devices such as mice, keyboards, network adapters, and external storage can be connected via a USB hub. The Raspberry Pi Zero and Raspberry Pi Zero W have a single micro USB port, this requires a USB OTG cable to connect devices such as keyboards or hubs.

The final model (not described in the table above) is the [Compute Module](https://www.raspberrypi.org/products/compute-module-3/), which is intended for industrial applications. It is a small form factor device that connects to a carrier board, for example a circuit board inside an industrial product, and gives manufacturers an easy way to use the Raspberry Pi ecosystem in their own devices.

You can check our [products](https://www.raspberrypi.org/products/) pages for more details on current boards. There are also some models of Raspberry Pi which are no longer in production, but which may be available second-hand or from resellers. The Model A was the initial low-cost variant of the Raspberry Pi. It was replaced by the smaller, neater Model A+ in November 2014; it shares the same specs as the A+, but has only 26 GPIO pins and 128MB of RAM. The Model B was the previous incarnation of the B+; again, it shares most of the same specs, but has only two USB ports and 26 GPIO pins. The original version of the Raspberry Pi Zero did not come with a camera connector, but all current versions have the connector as standard.

### What hardware documentation is available?

All available documentation is in our [documentation repository](./README.md).

### What hardware interfaces does it have?

Depending on the model, the Raspberry Pi has either 40 or 26 dedicated interface pins. In all cases, these include a UART, an I2C bus, a SPI bus with two chip selects, I2S audio, 3V3, 5V, and ground. The maximum number of GPIOs can theoretically be indefinitely expanded by making use of the I2C or SPI bus.

There is also a dedicated CSI-2 camera port for the [Raspberry Pi Camera Module](https://www.raspberrypi.org/products/), and a DSI display port for the [Raspberry Pi LCD touchscreen display](https://www.raspberrypi.org/products/raspberry-pi-touch-display/).

### Can I use a Raspberry Pi for audio or video input?

Not by itself: there is no audio or video (HDMI/composite) IN capability on the Raspberry Pi. You can add third-party boards to add this sort of functionality. The Raspberry Pi has a camera interface that can record video from the [Raspberry Pi Camera Module](https://www.raspberrypi.org/products/) — you can find the the [Camera Module FAQ section here](#cameramodule).

### Where is the on/off switch?

There is no on/off switch! To switch on, just plug it in. To switch off, if you are in the graphical environment, you can either log out from the main menu, exit to the Bash prompt, or open the terminal. From the Bash prompt or terminal you can shut down the Raspberry Pi by entering `sudo halt -h`. Wait until all the LEDs except the power LED are off, then wait an additional second to make sure the SD card can finish its wear-levelling tasks and write actions. You can now safely unplug the Raspberry Pi. Failure to shut the Raspberry Pi down properly may corrupt your SD card, which would mean you would have to re-image it.

### What are the dimensions of the Raspberry Pi?

The Raspberry Pi Model B versions measure 85.60mm x 56mm x 21mm (or roughly 3.37″ x 2.21″ x 0.83″), with a little overlap for the SD card and connectors which project over the edges. They weigh 45g. The Raspberry Pi Zero and Raspberry Pi Zero W measure 65mm x 30mm x 5.4mm (or roughly 2.56″ x 1.18″ x 0.20″) and weigh 9g. For the mechanical outlines, please see the documentation [here](../hardware/raspberrypi/mechanical/README.md)

<a name="pi-performance"></a>

## Performance

### How powerful is it?

All Raspberry Pi models up to the Raspberry Pi 3 have a GPU that provides OpenGL ES 2.0, hardware-accelerated OpenVG, and 1080p30 H.264 high-profile encode and decode. The GPU is capable of 1Gpixel/s, 1.5Gtexel/s, or 24 GFLOPs of general-purpose compute, and it features a range of texture filtering and DMA infrastructure. This means that graphics capabilities are roughly equivalent to the original Xbox's level of performance. Overall real-world performance for Raspberry Pi 1 Model A, A+, B, B+, Raspberry Pi Zero/Zero W, and CM1 is similar to that of a 300MHz Pentium 2, but with much better graphics. The Raspberry Pi 2 Model B is approximately equivalent to an Athlon Thunderbird running at 1.1GHz; again, it has the much higher-quality graphics, which come from using the same GPU as previous models. The Raspberry Pi 3 Model B is around twice as fast as the Raspberry Pi 2 Model B, depending on the benchmarks chosen.

The Raspberry Pi 4 uses an improved GPU — the VideoCore VI. This is around four times faster than the VideoCore IV used for previous models. The new ARM A72 cores on the BCM2711 chip give much better performance than the previous models, and a new PCIe bus gives faster USB 2.0 and new USB 3.0 functionality. Raspberry Pi 4's native Ethernet capability allows full 1Gbit I/O. These features, combined with the optional extra RAM (the Raspberry Pi 4 can be purchased with 2GB, 4GB or 8GB RAM), mean that the Raspberry Pi 4 can now provide a great desktop computing experience!

### Can I use my Raspberry Pi as a desktop replacement?

It depends on the model you have! For many daily tasks the Raspberry Pi 3 is quite suitable, but because modern internet browsers require a lot of memory, browsing can be a bit slow if you open too many browser tabs. Although 1GB of RAM seems like a lot, modern browsers are real memory hogs!

The Raspberry Pi 4 — with its faster cores, extra memory, and much improved I/O — is a very good desktop replacement. 

### Can I add extra RAM?

No. The RAM on the Raspberry Pi 1 Model A, A+, B, B+, and Raspberry Pi Zero/Zero W is a Package on Package (POP) on top of the SoC, which means you cannot remove or swap it. The RAM on the Raspberry Pi 2 and 3 Model B versions is on a separate chip on the bottom of the PCB, but 1GB is the maximum RAM that the SoC used by the Raspberry Pi 2 and 3 Model B can support. The Raspberry Pi 4 supports up to 8GB of RAM, but like previous models, it is not upgradeable after purchase.

### Can I connect multiple Raspberry Pis together to make a faster computer?

Sort of, but not in the way you might want to do it. You cannot simply make a more powerful computer, to play games faster for example, by bolting together smaller ones. You can network computers to create a cluster computer, but you do need to modify your software to work in this distributed fashion. We've put together a tutorial for [how to build a Raspberry Pi cluster](https://projects.raspberrypi.org/en/projects/build-an-octapi), in collaboration with GCHQ.

### Why does my Raspberry Pi run at a slower clock speed than advertised?

The Raspberry Pi (all models) idles at a lower speed than advertised. If the workload of the CPU increases, then the clock speed increases until it reaches its maximum value, which varies between models. If the CPU starts to overheat, there are added complexities: depending on the model, when the device reaches a particular temperature, the clock is throttled back to prevent overheating. This is called thermal throttling. If the Raspberry Pi does thermal-throttle, you will see a warning icon in the top right-hand corner of the desktop (see [here](../configuration/warning-icons.md)).

### Does it overclock?

The Raspberry Pi 1 Model A, A+, B, and B+ operate at 700MHz by default. Most devices will run happily at 800MHz. The Raspberry Pi 2 Model B operates at 900MHz by default and should run quite happily at 1000MHz. The Raspberry Pi 3 Model B runs at 1.2GHz, but this model has no standard overclocking settings. The Raspberry Pi 4 runs at 1.5GHz, and has no overclocking options.

### What is its operating temperature? Does it need a heatsink?

The Raspberry Pi is built from commercial chips which are qualified to different temperature ranges; the LAN9514 (LAN9512 on older models with 2 USB ports) is specified by the manufacturers as being qualified from 0°C to 70°C, while the SoC is qualified from -40°C to 85°C. You may well find that the board will work outside those temperatures, but we're not qualifying the board itself to these extremes.

You should not need to use a heatsink, as the chip used in the Raspberry Pi is equivalent to one used in a mobile phone, and should not become hot enough to require any special cooling. However, depending on the case you are using and the overclocking settings, you might find a heatsink to be advantageous. We do recommend the use of a heatsink if you are overclocking the Raspberry Pi 3 Model B. Of course, if you just like the look of one, you will not hurt the Raspberry Pi by placing an appropriately-sized heatsink on it.

<a name="pi-software"></a>

## Software

### What operating system does it use?
The recommended distribution (distro) is Raspberry Pi OS, which is specifically designed for the Raspberry Pi and which our engineers are constantly optimising. It is, however, a straightforward process to replace the root partition on the SD card with another Arm Linux distro, so we encourage you to try out several distros to see which one you like the most. There are several other distros available on our [downloads](https://www.raspberrypi.org/downloads) page. The OS is stored on the SD card.

### Can I run Windows 10 on the Raspberry Pi?
You cannot run Windows 10 on the Raspberry Pi. There is however a special "Internet of Things" version of Windows 10 that runs on the Raspberry Pi 3B and 3B+, called Windows 10 IoT. Windows 10 IoT does not have a graphical desktop, and is intended for use in embedded devices.

You may see reference to Windows 10 running on the Raspberry Pi online. This is because the community have devised a way to run regular Windows 10 on the Raspberry Pi. Although it will run, it runs extremely slowly so is not of any real use. Rather, it is a proof-of-concept. Microsoft do not sanction running Windows 10 on the Raspberry Pi.

### Updates? Upgrades? What do I do?

It's important to keep your system up to date with the latest security updates, as well as bug fixes for any applications you might be using. You can easily do this by opening a terminal window and running the following two commands:

+ `sudo apt update` will download package information from all configured sources, so the system knows what the latest updates are.

+ `sudo apt full-upgrade` will then download all the updates and install them.

We recommend going through this process once a week or so. 

### I heard about something called `rpi-update`. When should I use that?

Do not use `rpi-update` unless you have been recommended to do so by a Raspberry Pi engineer. This is because it updates the Linux kernel and Raspberry Pi firmware to the very latest version which is currently under test. It may therefore make your Raspberry Pi unstable, or cause random breakage.

### The processors on the latest Raspberry Pi models are 64-bit, but I cannot find an official 64-bit OS.

Raspberry Pi do not currently provide an official 64-bit OS, for a number of reasons. Firstly, since we still sell devices that are 32-bit, we would need to support two separate distributions, and at the moment we do not have the support capacity. Secondly, building a full 64-bit OS would require a considerable amount of work to, for example, fix the interfacing to the 32-bit VideoCore GPU. There are third-party 64-bit operating systems available, but they do not have the full support for the GPU that would be a requirement for an official release.

### Can I run PC or Mac software on the Raspberry Pi?

It is not possible to run Mac software on the Raspberry Pi.

You cannot run Windows software *directly* on the Raspberry Pi. It is sometimes possible to use emulation software to run Windows applications on the Raspberry Pi, but the use of emulation makes it run much more slowly. For example, Windows 98 runs reasonably well on the Raspberry Pi using an emulator called QEMU, however more recent Windows software runs too slowly to be useful on the Raspberry Pi.

There is a wealth of Linux software available directly on the Raspberry Pi itself. By default, Raspberry Pi OS comes installed with the most commonly used applications. If you need to install something else, use the "Add / Remove Software" application. You can also use the `apt` command - see [APT](../linux/software/apt.md). Linux software binaries available elsewhere are usually compiled for the x86 and x64 architectures, so cannot be used on the Raspberry Pi since it uses the ARM architecture. However, if the source code is available, you can compile an ARM-specific version yourself.

### Will it run Android or Android Things?

Raspberry Pi themselves do not support the consumer version of Android that you may be familiar with from your mobile phone. There are community efforts to make a version available that can be found online.

Google supports Android Things on the Raspberry Pi 3 as a development platform. Android Things is a variant of the Android platform enabling developers to build software for embedded and Internet of Things (IoT) devices with the Android SDK. To learn more about the platform and how to get started, visit [developer.android.com/things](https://developer.android.com/things/index.html).

### Will it run old software?

In general, you need to look to see whether the program you want can be compiled for the Armv6 (Raspberry Pi 1/Zero/Zero W/CM), Armv7 (Raspberry Pi 2) or Armv8 (Raspberry Pi 3) architecture on Linux. In most cases, the answer will be yes. Specific programs are discussed on [our forums](https://www.raspberrypi.org/forums/), so you might want to look there for an answer. Ultimately, nothing beats grabbing a Raspberry Pi and finding out the answer through direct testing!

### My `.exe` file won't run!

Most `.exe` files come from Windows and are compiled for the x86 processor architecture. These will not run on the Raspberry Pi, which uses an ARM processor architecture. A minority of `.exe` files, compiled from C# code or similar, actually use a Byte Code rather than a processor-specific instruction set, and therefore might work on the Raspberry Pi if the correct Mono interpreter software is installed.

### Can I share files from my Raspberry Pi with my Windows machines?

Yes, there are a number of ways of doing this, and the most common is to use what are called Samba shares. We don't have any specific documentation on Samba shares in our official docs just yet, but [here](https://www.raspberrypi.org/magpi/samba-file-server/) is some from our magazine, [The MagPi](https://www.raspberrypi.org/magpi).

It's also easy to copy files to and from Windows devices, rather than sharing folders. There is plenty of documentation [here](../remote-access/README.md).

### Why does `cpuinfo` report I have a BCM2835?

The upstream Linux kernel developers had decided that all models of Raspberry Pi return bcm2835 as the SoC name. At Raspberry Pi we like to use as much upstream kernel code as possible, as it makes software maintenance much easier, so we use this code. Unfortunately it means that `cat /proc/cpuinfo` is inaccurate for the Raspberry Pi 2, Raspberry Pi 3 and Raspberry Pi 4, which use the bcm2836/bcm2837, bcm2837 and bcm2711 respectively. You can use `cat /proc/device-tree/model` to get an accurate description of the SoC on your Raspberry Pi model.

### How do I run a program at startup?

There are a number of ways of doing this — [here's one](../linux/usage/rc-local.md).

### How do I run a program at a specific time?

With Cron! [Here's how](../linux/usage/cron.md).

<a name="pi-video"></a>
## Video

### What displays can I use?

There is composite and HDMI out on the board, so you can hook it up to an old analogue TV through the composite or through a composite to SCART connector, to a digital TV or to a DVI monitor (using a cheap, passive HDMI to DVI cable for the DVI). For the Model B+, Raspberry Pi 2, and Raspberry Pi 3, the RCA composite jack has been replaced with a 3.5mm jack that combines audio and video in one. You'll need a 3.5mm to 3RCA adapter cable to connect it to an older TV. There are many different types of this cable out there, but you want to purchase one that is compatible with the iPod Video (the iPod will have the left and right audio channels reversed, but the version of Raspberry Pi OS included with NOOBS can swap this for you). The Raspberry Pi Zero uses a mini-HDMI port.

The Raspberry Pi 4 has support for two HDMI monitors, which attach via micro HDMI ports. It is also capable of displaying at full resolution on a 4K monitor or TV. Note that for best HDMI performance at 4K, a good-quality HDMI cable is required. We sell a full set of ancilliary components, including HDMI cables.

### Why is there no VGA support?

Whilst there is no native VGA support, active adapters are available. Passive HDMI to VGA cables will not work with the Raspberry Pi. When purchasing an active VGA adapter, make sure it comes with an external power supply. HDMI to VGA adapters without an external power supply often fail to work.

### Does the HDMI port support CEC?

Yes, the HDMI port on the Raspberry Pi supports the CEC Standard. CEC may be called something else by your TV's manufacturer; check [the Wikipedia entry on CEC](http://en.wikipedia.org/wiki/Consumer_Electronics_Control#CEC) for more information.

### Can I add a touchscreen?

The Raspberry Pi Foundation provides a 7" capacitive [touchscreen](https://www.raspberrypi.org/products/raspberry-pi-touch-display) that utilises the Raspberry Pi's DSI port. This is available through the usual distributors. Alternatively, several third-party retailers offer a range of touchscreens for the Raspberry Pi.

### What codecs can it play?

The Raspberry Pi can encode (record) and decode (play) H.264 (MP4/MKV) out of the box. There are also two additional codecs you can [purchase through our Swag Store](http://swag.raspberrypi.org/collections/software) that enable you to decode [MPEG-2](http://swag.raspberrypi.org/collections/software/products/mpeg-2-license-key), a very popular and widely used format to encode DVDs, video camera recordings, TV and many others, and [VC-1](http://swag.raspberrypi.org/collections/software/products/vc-1-license-key), a Microsoft format found in Blu-ray discs, Windows Media, Slingbox, and HD-DVDs.

On the Raspberry Pi 4, the extra hardware CODEC support for MPEG-2 and VC-1 is not available: because the Raspberry Pi 4's processors are powerful enough to decode these in software, no CODEC licence is necessary. In addition, the Raspberry Pi 4 also has hardware support for decoding H265/HEVC.

<a name="pi-audio"></a>

## Audio

### Is sound over HDMI supported?

Yes.

### What about standard audio in and out?

There is a standard 3.5mm jack for audio out to an amplifier (not on Zero models). You can add any supported USB microphone for audio in or, using the I2S interface, you can add a codec for additional audio I/O.

<a name="pi-power"></a>

## Power

### Is it safe to just pull the power?

No, not really — you may corrupt your SD card if you do that. We recommend issuing the `sudo halt` or `sudo shutdown` command prior to pulling the power. This ensures that any outstanding file transactions are written to the SD card, and that the SD card is no longer 'active'. Pulling the power during a SD card transaction can occasionally corrupt the card.

### What about unplanned power interruptions?

Power interruptions can cause problems on all sorts of electronic devices, and the Pi is no different. SD card corruption can be caused if the power is simply turned off without going through a normal shutdown. This is because the system may be writing to the SD card at the point of power failure, leaving the SD card filesystem in an invalid state. So, if you cannot prevent power interruptions, one way of making the system more robust is to limit the amount of writing that is done to the SD card, or even to stop it altogether. You can disable swap, enable logging to RAM, and disable systemd-timesyncd, all of which greatly reduce the number of accesses to the SD card. You can also make the entire Raspberry Pi OS installation read-only, preventing any writing to the card at all. An internet search will provide instructions on how to implement these measures. 

### What are the power requirements?

The device needs to be powered with a 5V power supply with a USB connector; USB-C for the Raspberry Pi 4, and micro USB for all other models. Exactly how much current (mA) the Raspberry Pi requires is dependent on which model you are using, and what you hook up to it. We recommend our own power supplies, and sell a [2.5A (2500mA)](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/) supply for models up to the Pi 3, and a [3.0A (3000mA) supply](https://www.raspberrypi.org/products/type-c-power-supply/) for the Pi 4. These will provide you with enough power to run your Raspberry Pi for most applications, including use of the 4 USB ports. Very high-demand USB devices may however require the use of a powered hub. The table below outlines the specific power requirements of each model.

| Product | Recommended PSU current capacity | Maximum total USB peripheral current draw | Typical bare-board active current consumption |
|-|-|-|-|
|Raspberry Pi Model A | 700mA | 500mA | 200mA |
| Raspberry Pi Model B |1.2A | 500mA | 500mA |
| Raspberry Pi Model A+ | 700mA | 500mA | 180mA
| Raspberry Pi Model B+ | 1.8A | 1.2A | 330mA |
| Raspberry Pi 2 Model B | 1.8A | 1.2A | 350mA |
| Raspberry Pi 3 Model B | 2.5A | 1.2A | 400mA |
| Raspberry Pi 3 Model A+ | 2.5A | Limited by PSU, board, and connector ratings only. | 350mA |
| Raspberry Pi 3 Model B+ | 2.5A | 1.2A | 500mA |
| Raspberry Pi 4 Model B | 3.0A | 1.2A | 600mA |
| Raspberry Pi Zero W/WH | 1.2A | Limited by PSU, board, and connector ratings only.| 150mA |
| Raspberry Pi Zero | 1.2A | Limited by PSU, board, and connector ratings only | 100mA |

The specific current requirements of each model are dependent on the use case: the PSU recommendations are based on **typical maximum** current consumption, the typical current consumption is for each board in a *desktop computer* configuration. The Raspberry Pi Model A, A+, and B can supply a maximum of 500mA to downstream USB peripherals. If you wish to connect a high-power USB device, it is recommended that you connect a powered USB hub to the Raspberry Pi and connect your peripherals to the USB hub.

From the Raspberry Pi B+ onwards, 1.2A is supplied to downstream USB peripherals. This allows the vast majority of USB devices to be connected directly to these models, assuming the upstream power supply has sufficient available current.

Very high-current devices, or devices which can draw a surge current such as certain modems and USB hard disks, will still require an external powered USB hub. The power requirements of the Raspberry Pi increase as you make use of the various interfaces on the Raspberry Pi. The GPIO pins can draw 50mA safely (note that that means 50mA distributed across all the pins: an individual GPIO pin can only safely draw 16mA), the HDMI port uses 50mA, the Camera Module requires 250mA, and keyboards and mice can take as little as 100mA or as much as 1000mA! Check the power rating of the devices you plan to connect to the Raspberry Pi and purchase a power supply accordingly. If you're not sure, we would advise you to buy a powered USB hub.

This is the typical amount of power (in ampere) drawn by different Raspberry Pi models during standard processes:

| | | Raspberry Pi 1B+ | Raspberry Pi 2B | Raspberry Pi 3B | Raspberry Pi Zero | Raspberry Pi 4B |
|-|-|----------|-------|-------------|------------|------|
| Boot | Max |0.26 | 0.40| 0.75| 0.20 | 0.85 |
| | Avg | 0.22 | 0.22 | 0.35 | 0.15 | 0.7 |
| Idle |Avg | 0.20 | 0.22 | 0.30 | 0.10 | 0.6 |
| Video playback (H.264) | Max | 0.30 | 0.36 |0.55 |0.23 | 0.85 | 
| | Avg | 0.22 | 0.28 | 0.33 | 0.16 | 0.78 |
| Stress | Max | 0.35 | 0.82 | 1.34 | 0.35 | 1.25 |
| | Avg | 0.32 | 0.75 | 0.85 | 0.23 | 1.2 |
| Halt current | | | | 0.10 | 0.055 | 0.023 | 

**Test conditions:** We used a standard Raspberry Pi OS image (current as of 26 Feb 2016, or June 2019 for the Raspberry Pi 4), at room temperature, with the Raspberry Pi connected to a HDMI monitor, USB keyboard, and USB mouse. The Raspberry Pi 3 Model B was connected to a wireless LAN access point, the Raspberry Pi 4 was connected to Ethernet. All these power measurements are approximate and do not take into account power consumption from additional USB devices; power consumption can easily exceed these measurements if multiple additional USB devices or a HAT are connected to the Raspberry Pi.

### Can I power the Raspberry Pi from a USB hub?

It depends on the hub. Some hubs comply with the USB 2.0 Standard and only provide 500mA per port, which may not be enough to power your Raspberry Pi. Other hubs view the USB standards more like guidelines, and will provide as much power as you want from each port. Please also be aware that some hubs have been known to *backfeed* the Raspberry Pi. This means that the hubs will power the Raspberry Pi through its USB input cable, without the need for a separate micro-USB power cable, and bypass the voltage protection. If you are using a hub that *backfeeds* to the Raspberry Pi and the hub experiences a power surge, your Raspberry Pi could potentially be damaged.

### Can I power the Raspberry Pi from batteries as well as from a wall socket?

Running the Raspberry Pi directly from batteries requires special care and can result in damaging or destroying your Raspberry Pi. If you consider yourself an advanced user, though, you could have a go. For example, four of the most common AA rechargeable batteries would provide 4.8V on a full charge. 4.8V would technically be just within the range of tolerance for the Raspberry Pi, but the system would quickly become unstable as the batteries lost their full charge. Conversely, using four AA Alkaline (non-rechargeable) batteries will result in 6V. 6V is outside the acceptable tolerance range and would potentially damage or, in the worst-case scenario, destroy your Raspberry Pi. It is possible to provide a steady 5V from batteries by using a buck and/or boost circuit, or by using a charger pack which is specifically designed to output a steady 5V from a couple of batteries; these devices are typically marketed as mobile phone emergency battery chargers.

### Is Power over Ethernet possible?

Yes: if you own a 3B+ or 4B, you can use our [official Raspberry Pi PoE HAT](https://www.raspberrypi.org/products/poe-hat/) to power that Raspberry Pi over Ethernet. For other models, there are adapters that split the voltage off the Ethernet line before connecting to the Raspberry Pi. However, we have not tested any third-party PoE solutions, so we cannot recommend any of these. 

### What voltage devices can I attach to the GPIO pins, and how much current can I pull?

The GPIO pins are natively 3.3V, so 5V devices **MUST NOT** be attached directly without some sort of voltage conversion. The pins can provide up to 16mA current. See the [GPIO docs page](../hardware/raspberrypi/gpio/README.md) for more information.

<a name="sd-cards"></a>

## SD cards and storage

### What size of SD card do I need?

Whether you want to use the [official Raspberry Pi OS operating system](https://www.raspberrypi.org/downloads/raspbian/) (or the [NOOBS installer for Raspberry Pi OS](https://www.raspberrypi.org/downloads/noobs/) or a different standalone operating system image (see [recommended third-party OS](https://www.raspberrypi.org/downloads/)), **the minimum-size SD card we recommend using is 8GB**. This will give you the free space you need to install additional packages or make programs of your own. The original Raspberry Pi Model A and Model B require full-size SD cards. The newer Raspberry Pi 1 Model A+, Model 1 B+, 2B, 3B, 3B+, 3A+, 4B, Zero, Zero W, and Zero WH require microSD cards.

### What size of SD card can it support?

While the recommended minimum of 8GB should be enough for most people, we have tried cards up to 128GB, and most cards seem to work OK. You can also attach a USB stick or USB hard drive to provide extra storage.

### Can I boot a Raspberry Pi from a USB-attached hard drive instead of the SD card?

USB boot is only possible on the Raspberry Pi 2B v1.2, 3B, 3B+, and 3A+. Booting from a USB-attached drive (either a SSD or actual hard drive) can make the Raspberry Pi boot and work faster. We have extensive instructions on how to do this [here](../hardware/raspberrypi/bootmodes/msd.md).

### What happens if I brick the device?

If you brick the device, you can restore it by reflashing the SD card.

<a name="networking"></a>

## Networking and wireless connectivity

### Does the device support networking?

The Raspberry Pi 1 Model B and B+, Raspberry Pi 2, and Raspberry Pi 3 Model B versions of the device have built in 10/100 wired Ethernet. The Raspberry Pi 3B+ and Raspberry Pi 4 have 1000BaseT wired Ethernet, but on the 3B+, throughput is limited by its USB 2.0 connection to the SoC. There is no Ethernet on the Raspberry Pi 1 Model A and A+, and the Raspberry Pi Zero/Zero W.

### Is there built-in wireless networking?

The Raspberry Pi 3, 3+, 4, and Raspberry Pi Zero W have built-in wireless LAN connectivity. You can also add a USB wireless LAN dongle to any model of Raspberry Pi.

The Raspberry Pi Model 3B+ and 4B support 802.11ac, and all earlier models support up to 802.11n.

### Is there built-in Bluetooth?

Yes, the Raspberry Pi 3, Raspberry Pi 4, and Raspberry Pi Zero W have built-in Bluetooth.

### I don't seem to get full-speed gigabit networking on my Raspberry Pi 3B+.

Although the Ethernet chip on the Raspberry Pi 3B+ is gigabit-capable, the connection from the chip to the SoC is still via USB 2.0, which limits the total bandwidth available to approximately 220–250Mbits/s in the real world. Although not gigabit, this is a healthy bump over the 100Mbits/s top speed of the 3B model. To get the best performance, you should ensure that Ethernet flow control is turned ON on your router.

### Does the device have support for any form of netbooting or PXE?

The Raspberry Pi 3 can be set up to network boot without an SD card present; earlier models can PXE/Netboot with an appropriately set up SD card. You can find our netbooting documentation [here](../hardware/raspberrypi/bootmodes/net.md).

The Raspberry Pi 4 does not currently support network booting without an SD card present. A bootloader update to support network boot is planned but not yet available.

We have also developed [PiServer](https://www.raspberrypi.org/blog/piserver/), a piece of software that lets you easily set up a network of client Raspberry Pis connected to a single x86-based server via Ethernet. With PiServer, you don’t need SD cards, you can control all clients via the server, and you can add and configure user accounts — ideal for the classroom, your home, or an industrial setting.

Another option is [PiNet](http://pinet.org.uk), which is a free and open-source community-based project initially designed for schools. Each Raspberry Pi boots off a small set of startup files on an SD card and fetches the rest of the data it needs from the PiNet server, thereby allowing you to maintain a single operating system image for all the Raspberry Pis. PiNet also adds network user accounts, shared folders and automated backups.

<a name="cameramodule"></a>

## Camera Module

### What is the Camera Module?

The Raspberry Pi Camera Modules are small PCB's that connects to the CSI-2 camera port on the Raspberry Pi using a short ribbon cable. They provide connectivity for a camera capable of capturing still images or video recordings. The Camera Modules connect to the Image System Pipeline (ISP) in the Raspberry Pi's SoC, where the incoming camera data is processed and eventually converted to an image or video on the SD card (or other storage). You can [read more about the Camera Modules here](https://www.raspberrypi.org/products/). 

### What model of camera does the Camera Module use?

The original Camera Module is an Omnivision OV5647, the V2 which replaced it is a Sony IMX219. There is now a High quality camera module available, with an interchangeable lens mount, using the Sony IMX447 sensor.  

### What resolutions are supported?

The original Camera Module is capable of taking photos up to 5 megapixels and can record video at resolutions up to 1080p30. The Camera Module V2 is capable of taking photos up to 8 megapixels (8MP). It supports 1080p30, 720p60 and VGA90 video modes, as well as still capture. The High Quality camera module is 12.3MP, with the same video performance as the other models.

### What picture formats are supported?

The Raspberry Pi Camera Modules supports raw capturing (Bayer data direct from the sensor) or encoding as JPEG, PNG, GIF and BMP, uncompressed YUV, and uncompressed RGB photos. They can record video as H.264, baseline, main, and high-profile formats.

### How do I use the Camera Module?

We've put together [a how-to](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera) for that!

There are also a number of command line applications provided for stills and video output. These applications provide the typical features you might find on a compact camera, such as set image size, compression quality, exposure mode, and ISO. See the [documentation](https://www.raspberrypi.org/documentation/hardware/camera/README.md) for more details.

### Can I extend the ribbon cable?

Yes. We have reports of people using cables up to four metres in length and still receiving acceptable images, though your experience may differ.

### How much power does the Camera Module use?

The Raspberry Pi Camera Modules requires 250mA to operate. Ensure that your power supply can provide enough power for the connected Camera Module, as well as for the Raspberry Pi itself and any peripherals directly attached to it.

<a name="troubleshoot"></a>

## Troubleshooting

### What is the username and password for the Raspberry Pi?

The default username for Raspberry Pi OS is `pi` (without any quotation marks) and the default password is `raspberry` (again, do not include the quotation marks). If this does not work, check the information about your specific distro on the [downloads page](https://www.raspberrypi.org/downloads).

### Why does nothing happen when I type in my password?

To protect your information, Linux does not display anything when you are entering passwords in the Bash prompt or the terminal. As long as you were able to see the username being typed in, your keyboard is working correctly.

### Why does my Raspberry Pi not start up/boot?

Probably the most frequently asked question! We have full instructions for setting up your Raspberry Pi [here](../setup/), but if it still will not boot, you will find advice on what to do in the [troubleshooting post on our forum](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=58151).

### Why is my Raspberry Pi hot?

All electronics give off heat, and the Raspberry Pi is no exception. The Raspberry Pi 3 Model B+ has heat-spreading technology to use the entire PCB and connectors as a heatsink to dissipate excess energy. This means that except in exceptional conditions, you are unlikely to need a heatsink on the SoC or the Ethernet hub chip.

The Raspberry Pi 4 Model B uses the same heat-spreading technology but due to the much more powerful CPU cores is capable of higher peak power consumption than a Model 3B+. Under a continuously heavy processor workload, the Model 4B is more likely to throttle than a Model 3B+.

You can add a heatsink if you wish, and this may prevent thermal throttling by keeping the chips below the throttling temperature (see the clock speed paragraph in the [Performance](#pi-performance) section).

### I keep getting a lightning bolt symbol and messages about power.

Most Raspberry Pi models have circuity to detect drops of the incoming power supply voltage below around 4.65V. If such a drop happens, the lightning bolt warning icon (see [here](../configuration/warning-icons.md)) will appear, and a message will be sent to the system log. Below this voltage, there is no guarantee the Raspberry Pi will work correctly; it may result in the device locking up, or bad SD card writes, USB device failure, Ethernet dropping out, etc. We recommend a good-quality 5V power supply, 2.5A for the Raspberry Pi 3B+, with a thick copper supply cable, such as [our official power supply](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/). The cable itself can be very important: often the cheaper cables use very thin copper wire, which can cause a significant voltage drop.

### My SD card seems to have stopped working.

SD cards have a limited lifespan due to the way they work. Under most circumstances, they offer some years of use, but heavy file accessing, or using it as a swap drive, may reduce the SD card's lifespan considerably. Note that there are also fake capacity SD cards being sold that are likely to be unreliable.

### I've imaged an SD card with Raspberry Pi OS/NOOBS, but when I look at it with my Windows PC, it's not all there!

This is to do with the capabilities of Windows to read Linux-formatted partitions. When you image the SD card, it is automatically split into multiple partitions. The first partition uses a format that Windows can read, but the other partitions use a Linux-specific file system, which Windows simply does not recognise. This means when you put an SD card in a Windows machine, it only displays the first partition, and may well say the other partitions are corrupted and need formatting - **do not format them**! Here's some information on what goes in that first [partition](../configuration/boot_folder.md). If you insert the SD card on a machine running Linux, it will display all the partitions correctly.

## I still have more questions!

Read the sticky subjects in the [Beginners subforum](https://www.raspberrypi.org/forums/viewforum.php?f=91) and check the [Help pages](https://www.raspberrypi.org/help/) for more information. If the answer is not there, ask in [the forums](https://www.raspberrypi.org/forums), where there are lots of helpful Raspberry Pi owners, users, and fans who will be more than happy to help you out.
