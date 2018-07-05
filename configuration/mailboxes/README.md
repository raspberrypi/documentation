## Overview

Mailboxes are a inter-processor communication mechanism between the ARM cores and the VideoCore GPU, both hardware blocks on the SoC.
There are two mailboxes, each mailbox is an 8-deep FIFO of 32-bit words, which can be read (popped)/written (pushed) by the ARM and VC.
Only mailbox 0's status can trigger interrupts on the ARM, so mailbox 0 is always for communication from Videocore to ARM and mailbox 1 is for ARM to Videocore. The ARM should never need to write mailbox 0 or read mailbox 1.

## Channels

Each mailbox has a list of defined virtual 'channels', which subdivides the types of mailbox call in to related categories. 

Mailbox 0 defines the following channels:

0. Power management
1. [Framebuffer](framebuffer.md)
2. Virtual UART
3. VCHIQ
4. LEDs
5. Buttons
6. Touch screen
7.
8. [Property tags (ARM -> VC)](propertiesARM-VC.md)
9. Property tags (VC -> ARM)

## Using the Mailboxes from Kernel modules

If using mailboxes from kernel code, there are functions already defined which can be used for setting and getting property tags. You will need access to the device tree node to get the required firmware pointers, which are usually available during probe functions. 

````C
/**
 * rpi_firmware_get - Get pointer to rpi_firmware structure.
 * @firmware_node:    Pointer to the firmware Device Tree node.
 *
 * Returns NULL is the firmware device is not ready.
 */
struct rpi_firmware *rpi_firmware_get(struct device_node *firmware_node)
````
````C
/**
 * rpi_firmware_property - Submit single firmware property
 * @fw:		Pointer to firmware structure from rpi_firmware_get().
 * @tag:	One of enum_mbox_property_tag.
 * @tag_data:	Tag data buffer.
 * @buf_size:	Buffer size.
 *
 * Submits a single tag to the VPU firmware through the mailbox
 * property interface.
 *
 * This is a convenience wrapper around
 * rpi_firmware_property_list() to avoid some of the
 * boilerplate in property calls.
 */
int rpi_firmware_property(struct rpi_firmware *fw,
			  u32 tag, void *tag_data, size_t buf_size)
````
````C
/**
 * rpi_firmware_property_list - Submit firmware property list
 * @fw:		Pointer to firmware structure from rpi_firmware_get().
 * @data:	Buffer holding tags.
 * @tag_size:	Size of tags buffer.
 *
 * Submits a set of concatenated tags to the VPU firmware through the
 * mailbox property interface.
 *
 * The buffer header and the ending tag are added by this function and
 * don't need to be supplied, just the actual tags for your operation.
 * See struct rpi_firmware_property_tag_header for the per-tag
 * structure.
 */
int rpi_firmware_property_list(struct rpi_firmware *fw,
			       void *data, size_t tag_size)
````

## Using Mailboxes on the command line

There is an app available called `vcmailbox` which allows use of the mailboxes from the command line. In addition it is a good source of information on using the mailbox system in a Linux application.

By default the `vcmailbox` application can be found in `/opt/vc/bin`

The `vcmailboc` application simply sends a user supplied set of 32bit words (in decimal or hexadecimal if using 0x) to the mailbox property system, then displays the resulting returned values. 

The source for `vcmailbox` can  be found [here](https://github.com/raspberrypi/userland/blob/master/host_applications/linux/apps/vcmailbox/vcmailbox.c)

## Mailbox registers

The following table shows the register offsets for the different mailboxes. For a description of the procedure for using these registers to access a mailbox from code running on the ARM, see [here](accessing.md).

| Mailbox | Read/Write | Peek | Sender | Status | Config |
| ------- | ---------- | ---- | ------ | ------ | ------ |
| 0 | 0x00 | 0x10 | 0x14 | 0x18 | 0x1c |
| 1 | 0x20 | 0x30 | 0x34 | 0x38 | 0x3c |
