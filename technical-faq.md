## Technical FAQs

This page gives short answers to some of the more commonly asked technical questions about the Raspberry Pi computers. More details on these topics can be found in the rest of the documentation.

### Why does my Pi not start up/boot?

Probably the most frequently asked question! We have full instructions for setting up your Raspberry Pi [here](./setup/), but if it still will not boot, you will find advice on what to do in the [troubleshooting post on our forum](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=58151).

### What differences are there in the GPU between different models?

All of the Raspberry Pi models use the same GPU, the Videocore4. Since the GPU provides the camera and display interfaces, codecs, 2D/3D graphics, etc., this means all Raspberry Pis have the same capabilities. The real difference between models is the type of ARM core used, and the additional peripherals that are attached, e.g. connectivity, USB ports, etc.

### Why does my Pi run at a slower clock speed that advertised?

The Raspberry Pi (all models) idles at a lower speed than advertised. If the workload of the CPU increases, then the clock speed increases until it reaches its maximum value, which varies between models. If the CPU starts to overheat, there are added complexitites: depending on the model, when the device reaches a particular temperature, the clock is throttled back to prevent overheating. This is called thermal throttling. If the Pi does thermal-throttle, you will see a warning icon in the top right-hand corner of the desktop (see [here](./configuration/warning-icons.md)).

### Why is my Pi hot?

All electronics give off heat, and the Pi is no exception. The latest model (3B+) has heat-spreading technology to use the entire PCB and connectors as a heatsink to dissipate excess energy. This means that except in exceptional conditions, you are unlikely to need a heatsink on the SoC or the Ethernet hub chip. You can still add a heatsink if you wish, and this may prevent thermal throttling by keeping the chips below the throttling temperature (see the paragraph on clock speed).

### I keep getting a lightning bolt symbol and messages about power...

Most Pi models have circuity to detect drops of the incoming power supply voltage below around 4.65V. If such a drop happens, the lightning bolt warning icon (see [here](./configuration/warning-icons.md)) will appear, and a message will be sent to the system log. Below this voltage, there is no guarantee the Pi will work correctly; it may result in the device locking up, or bad SD card writes, USB device failure, Ethernet dropping out, etc. We recommend a good-quality 5V power supply, 2.5A for the Pi 3B+, with a thick copper supply cable, such as [our official power supply](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/). The cable itself can be very important: often the cheaper cables use very thin copper wire, which can cause a significant voltage drop.

### What manufacturing standards etc. does the Pi comply with?

We have put the Pi models through extensive compliance testing, for Europe, the USA, and other countries around the world. You can find many of the reports [here](./hardware/raspberrypi/conformity.md).

### I don't seem to get full-speed gigabit networking on my Pi 3B+.

Although the Ethernet chip on the Raspberry Pi 3B+ is gigabit-capable, the connection from the chip to the SoC is still via USB 2.0, which limits the total bandwidth available to approximately 220–250Mbits/s in the real world. Although not gigabit, this is a healthy bump over the 100Mbits/s top speed of the 3B model. To get the best performance, you should ensure that Ethernet flow control is turned ON on your router.

### The processors on the latest Pi models are 64-bit, but I cannot find an official 64-bit OS.

Raspberry Pi do not current provide an official 64-bit OS, for a number of reasons. Firstly, since we still sell devices that are 32-bit, we would need to support two separate distributions, and at the moment we do not have the support capacity. Secondly, building a full 64-bit OS would require a considerable amount of work to, for example, fix the interfacing to the 32-bit Videocore GPU. There are third-party 64-bit operating systems available, but they do not have the full support for the GPU that would be a requirement for an official release. 

### What voltage devices can I attach to the GPIO pins, and how much current can I pull?

The GPIO pins are natively 3.3V, so 5V devices **MUST NOT** be attached directly without some sort of voltage conversion. The pins can provide up to 16mA current. See the [GPIO docs page](hardware/raspberrypi/gpio/README.md) for more information.

### Can I use a Pi in a commercial product?

This is a very common question, and the answer is yes! Once you have bought a Pi, it's yours to do with as you wish. Note, however, that a lot of the software in the Raspbian distribution is GPL-licenced, which comes with certain requirements, most significantly that you must provide access to the source code if requested. This is usually pretty easy to do.

### Is a Pi suitable for industrial applications?

Yes and no — it depends on the use case. Pis have been used successfully in industrial environments, but the final decision must be in the hands of the end user as to whether the device is suitable for the task at hand. See our [Compute Module documentation](./hardware/computemodule/README.md) for more details on our Pi model specifically designed for use in commercial and industrial products.

### I'm worried I have a fake Pi!

Don't worry, as far as we know, there are no fake Pis. The SoCs used on the Pi range are only available from one supplier, and only in large quantities, which together with the low price of the Pi means it's not cost-effective for clones to be made. There are a number of competitor products that use similar names, but not actual clones or fakes. 

### My SD card seems to have stopped working.

SD cards have a limited lifespan due to the way they work. Under most circumstances, they offer some years of use, but heavy file accessing, or using it as a swap drive, may reduce the SD card's lifespan considerably. Note that there are also fake capacity SD cards being sold that are likely to be unreliable.

### My `.exe` file won't run!

Most `.exe` files come from Windows and are compiled for the x86 processor architecture. These will not run on the Raspberry Pi, which uses an ARM processor architecture. A minority of `.exe` files, compiled from C# code or similar, actually use a Byte Code rather than a processor-specific instruction set, and therefore might work on the Pi if the correct Mono interpreter software is installed.

### Can I use a Pi for audio or video input?

Not by itself: there is no audio or video (HDMI/composite) IN capability on the Pi. You can add third-party boards to add this sort of functionality. Ther Pi has a camera interface that can record video from the [Raspberry Pi Camera Module](https://www.raspberrypi.org/products/camera-module-v2/).

### Is it safe to just pull the power?

No, not really — you may corrupt your SD card if you do that. We recommend issueing the `sudo halt` or `sudo shutdown` command prior to pulling the power. This ensures that any outstanding file transactions are written to the SD card, and that the SD card is no longer 'active'. Pulling the power during a SD card transaction can occasionally corrupt the card.

### Can I use my Pi as a desktop replacement?

Yes and no, it depends! For many daily tasks the Pi is quite suitable, however, because internet browsers nowadays require a lot of memory, browsing can be a bit slow if you open too many browser tabs. Although 1GB of RAM seems like a lot, modern browsers are real memory hogs!

### Can I boot a Pi from a USB-attached hard drive instead of the SD card?

Yes, booting from a USB-attached drive (either a SSD or actual hard drive) can make the Pi boot and work faster. We have extensive instructions on how to do this [here](./hardware/raspberrypi/bootmodes/msd.md). 

### Can I boot a Pi over a network?

Yes, this is possible — see the documentation [here](./hardware/raspberrypi/bootmodes/net.md).

### Can I share files from my Pi with my Windows machines?

Yes, there are a number of ways of doing this, and the most common is to use what are called Samba shares. We don't have any specific documentation on Samba shares in our official docs just yet, but [here](https://www.raspberrypi.org/magpi/samba-file-server/) is some from our magazine, [The MagPi](https://www.raspberrypi.org/magpi).

It's also easy to copy files to and from Windows devices, rather than sharing folders. There is plenty of documentation [here](./remote-access/README.md).

### Can I connect multiple Pis together to make a faster computer?

Sort of, but not in the way you might want to do it. You cannot simply make a more powerful computer, to play games faster for example, by bolting together smaller ones. You can network computers to create a cluster computer, but you do need to modify your software to work in this distributed fashion. We've put together a tutorial for [how to build a Raspberry Pi cluster](https://projects.raspberrypi.org/en/projects/build-an-octapi), in collaboration with GCHQ.

### Why does cpuinfo report I have a BCM2835?

The upstream Linux kernel developers had decided that all models of Raspberry Pi return `bcm2835` as the SoC name. At Raspberry Pi we like to use as much upstream kernel code as possible, as it makes software maintenance much easier, so we use this code. Unfortunately, it means that `cat /proc/cpuinfo` is inaccurate on later Raspberry Pi models that use different SoCs. You can use `cat /proc/device-tree/model` to get an accurate description of the SoC on your Pi model.

### I've imaged an SD card with Raspbian/NOOBS, but when I look at it with my Windows PC, it's not all there!

This is to do with the capabilities of Windows to read Linux-formatted partitions. When you image the SD card, it is automatically split into multiple partitions. The first partition uses a format that Windows can read, but the other partitions use a Linux-specific file system, which Windows simply does not recognise. This means when you put an SD card in a Windows machine, it only displays the first partition, and may well say the other partitions are corrupted and need formatting - **do not format them**! Here's some information on what goes in that first [partition](./configuration/boot_folder.md). If you insert the SD card on a machine running Linux, it will display all the partitions correctly. 

### How do I run a program at startup?

There are a number of ways of doing this — [here's one](./linux/usage/rc-local.md).

### How do I run a program at a specific time?

With Cron! [Here's how](./linux/usage/cron.md).

### Updates? Upgrades? What do I do?

It's important to keep your system up to date with the latest security updates, as well as bug fixes for any applications you might be using. You can easily do this by opening a terminal window and running the following two commands:

+ `sudo apt update` will update the internal software database, so the system knows what the latest updates are

+ `sudo apt full-upgrade` will then download all the updates and install them

We recommend going through this process once a week or so. 

### I heard about something called `rpi-update`. When should I use that?

Do not use `rpi-update` unless you have been recommended to do so by a Raspberry Pi engineer. This is because it updates the Linux kernel and Raspberry Pi firmware to the very latest version which is currently under test. It may therefore make your Pi unstable, or cause random breakage.
