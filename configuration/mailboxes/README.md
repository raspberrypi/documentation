## Overview

Mailboxes are a inter-processor communication mechanism between the ARM cores and the VideoCore GPU, both hardware blocks on the SoC.
There are two mailboxes, each mailbox is an 8-deep FIFO of 32-bit words, which can be read (popped)/written (pushed) by the ARM and VC.
Only mailbox 0's status can trigger interrupts on the ARM, so mailbox 0 is always for communication from Videocore to ARM and mailbox 1 is for ARM to Videocore. The ARM should never need to write mailbox 0 or read mailbox 1.

## Channels

Each mailbox has a list of defined virtual 'channels', which subdivides the types of mailbox call in to related categories. 

Mailbox 0 defines the following channels:

0. Power management
1. Framebuffer
2. Virtual UART
3. VCHIQ
4. LEDs
5. Buttons
6. Touch screen
7.
8. Property tags (ARM -> VC)
9. Property tags (VC -> ARM)

## Using the Mailboxes

If using mailboxes from the ARM, there are API functions already defined which can be used. 

## Mailbox registers

The following table shows the register offsets for the different mailboxes. For a description of the procedure for using these registers to access a mailbox from code running on the ARM, see [here](accessing.md).

| Mailbox | Read/Write | Peek | Sender | Status | Config |
| ------- | ---------- | ---- | ------ | ------ | ------ |
| 0 | 0x00 | 0x10 | 0x14 | 0x18 | 0x1c |
| 1 | 0x20 | 0x30 | 0x34 | 0x38 | 0x3c |
