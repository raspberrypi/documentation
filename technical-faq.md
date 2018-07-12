## Technical FAQs

This page gives short answers to some of the more commonly asked technical questions about the Raspberry Pi range of SBC's. More detail on these topics can be found in the rest of the documentation.

### What differences are there in the GPU between different models

All of the Raspberry Pi range use the same GPU, the Videocore4. Since the GPU provides the camera and display interfaces, codecs, 2/3D graphics etc, this means all Raspberry Pi's have the same capabilities. The real difference in models is the type of ARM cores used, and the additional peripherals, e.g. networking, USB ports etc that are attached.

### Why does my Pi run at a slower clock speed that advertised?

The Raspberry Pi (all models) idles at a lower speed than advertised. If the workload of the CPU increases, then the clock speed is increased until it reaches its maximum value, which varies between models. There are also added complexitites if the CPU starts to over heat. Depending on the model, when the device reaches a particular temperature, the clock is throttled back to prevent overheating. This is caled thermal throttling. If the Pi does thermal throttle you will see a warning icon on the top right of the display. See [here](./configuration/warning-icons.md) 

### My Pi is HOT!

All electronics give out heat, and the Pi is no exception. The latest model (3B+) uses heat spreading technology to use the entire PCB and connectors as a heatsink to disipate the excess energy. This means that except in ecceptional conditions, you are unlikely to need a heatsink on the SoC or the ethernet hub chip. You can still add a heatsink if you wish, and it may prevent thermal throttling by keeping the chips below the throttling temperature.

### I keep getting a lightning bolt symbol and messages about power

The recent Pi models have circuity to detect if the incoming power supply voltage drops below about 4.65v, and if this happens the lightning bolt will appear and a message will be set to the system log. Below this voltage, there is no guarantee the Pi will work correctly; this may exhibit as the device locking up, or bad SD card writes, USB device failure, ethernet dropping out etc. We recommend a good quality 5v power supply, 2.5A for the Pi3B+, with a thick copper supply cable. The cable itself can be very important, often the cheaper cables use very thin copper wire, which can cause a significant voltage drop. See [here](./configuration/warning-icons.md)

### What manufacturing standards etc does the Pi comply with?

We have put the Pi models through extensive compliance testing, both for Europe, USA and other countries around the world. We have a page which publishes many of the reports [here](./hardware/raspberrypi/conformity.md).

### I don't seem to get full speed gigabit networking on my Pi3B+

ALthough the ethernet chip on the Raspberry Pi 3B+ is gigabit capable, the connection from the chip to the SoC is still via USB2.0, which limits the total bandwidth available to approximately 220-250Mbits/s in the real world. Although not gigabit, this is a healthy bump over the 100Mbits/s top speed of the 3B model. 

### The processors on the latest Pi models are 64bit, but I cannot find a official 64bit OS

Raspberry Pi do not current have an official 64bit OS. There are a number of reasons. Firstly, since we still sell devices that are 32bit, we would need to support two separate distributions, and at the moment we do not have the support capability. Secondly, to have a full 64bit OS would require a considerably amount of work to, for example, fix the interfacing to the 32bit Videocore GPU. There are third party 64bit OS's available, but they do not have the full support for the GPU that would be required for an official release. 

### What voltage devices can I attach to the GPIO pins, and how much current can I pull?

The GPIO are natively 3.3v, so 5v devices MUST NOT be attached directly, without some sort of voltage conversion. They can provide up to 16mA current. See the GPIO docs page for more information. [GPIO](hardware/raspberrypi/gpio/README.md)

### Can I use a Pi in a commercial product

A very common question is "Can I use a Raspberry Pi in a commercial product", and the answer is yes. Once you have bought it its yours to do with as you wish. Note however, that a lot of the software in the Raspbian distribution is GPL licenced, which does have certain requirement, mainly that you must provide access to the source code if requested. This is usually pretty easy to do.

### Is a Pi suitable for industrial applications?

Yes and no, as it depends on the use case. They have been used succesfully in industrial environments, but the final decision must be in the hands of the end user as to whether the device is suitable for the task in hand. See our Compute Module documentation for more details on a Pi model specifically designed for use in commercial and industrial products.

### I'm worried I have a fake Pi

Don't worry, as far as we know, there are no fake Pi's. The SoC's used on the Pi range are only available from one supplier, and only in large quantities, which when added to the low cost of the Pi itself, means it's not cost effective for clones to be made. There are a number of competitor products that use similar names, but not actual clones or fakes. 

### My SD card seems to have stopped working

SD cards have a limtited lifespan due to the way they work. Under most circumstances that can give some years of use, but heavy file accessing or using the SD card as a swap drive may reduce lifespan considerable. Note that there are also fake capacity SD cards that are likely to be unreliable.

## My .exe file won't run!

Most .exe files come from Windows, and are compiled for the x86 processor architecture. These will not run on the Raspberry Pi, which uses an ARM processor architecture. A minority of .exe's, compiled from C# code or similar, actually use a Byte Code rather than a processor specific instruction set, and might work with the correct Mono interpreter software installed.

### Can I use a Pi for Audio or Video input?

No. There is no audio or video (HDMI/composite) in capability on the Pi. You can add third party boards which can provide this sort of functionality. There is a camra interface which can record video from the Raspberry Pi camera module.

## Is it safe to just pull the power?

Depends. We recommend issueing the "sudo halt" or "sudo shutdown" command prior to pulling the power. This ensures that any outstanding file transaction are written to the SD card, and that the SD card is no longer 'active' Pulling the power during a SD card transaction can occasionally corrupt the card.

## Can I use my Pi as a desktop replacement?

Yes, and no! For many tasks the Pi is quite suitable, however, because internet browsers nowadays require a lot of memory, browsing can be a bit slow if you open too many browser tabs. Although 1GB of RAM seems a lot, modern browsers are real memory hogs!

## Can I boot a Pi from a USB attached harddrive instead of the SD card?

Yes, booting from a USB attached rive (either a SSD or actual harddrive) can make the Pi boot and work faster. We have extensive instruction on how to do it [here](./hardware/raspberrypi/bootmodes/msd.md). 

## Can I boot a Pi over a network?

Yes, this is also possible. See the documenation [here](./hardware/raspberrypi/bootmodes/net.md).

## Can I share files with my Windows machines

Yes, there are a number of ways of doing this, but the most common is to use what are called Samba shares. We don't have any specific documentation on Samba shares in our official docs just yet, but [here](https://www.raspberrypi.org/magpi/samba-file-server/) is one from our magazine, [The Magpi](https://www.raspberrypi.org/magpi)

It's also easy to copy files to and from Windows devices, rather than sharing folders. There is plenty of documentation [here](./remote-access/README.md)

## Can I attached multiple Pi's together to make a faster computer?

Well, sort of. But not in the way you might want to do it. You cannot simply make a better computer, to play games faster for example,  by bolting together smaller ones. However, you can network computers together to create a clustered computer, but you do need to modify your software to work in this distributed fashion. It's a bit too complicated to go in to here, but try this page on Wikipedia, and the ones referenced from it, for more information. [Computer clusters](https://en.wikipedia.org/wiki/Computer_cluster). There are also some Raspberry Pi clusters, [here's one example](https://www.pidramble.com/).

## Why does cpuinfo report I have a BCM2835?

The upstream Linux kernel developers had decided that all models of Raspbery Pi return bcm2835 as the SoC name. At Raspberry Pi we like to use as much upstream kernel code as possible, as it makes software maintenance much easier, so we use this code. Unfortunately it means that cat /proc/cpuinfo is inaccurate later Raspberry Pi models which use different SoC's. You can use cat /proc/device-tree/model to get an accurate description of the SoC on your Pi model.

## I've imaged an SD card with Raspbian/NOOBS, but when I look at it with my Windows PC it not all there!

This is to do with the capabilities of Windows to read Linux formatted partitions. When you image the SD card, it is automatically split in to multiple partitions. The first partition uses a format that Windows can read, but the other partitions use a Linux specific file system, and Windows simply does not recognise them. This means when you put an SD card in a Windows machine, it only displays the first partition, and may well say the other partitions are corrupted, and need reformatting - Don't do this! Here's some information on what goes in that first [partition](./configuration/boot_folder.md). If you insert the SD card on a machine running Linux, it will display all the partitions correctly. 





