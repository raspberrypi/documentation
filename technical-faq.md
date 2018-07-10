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





