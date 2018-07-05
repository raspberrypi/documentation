## Framebuffer Mailbox

## Note: This particular mailbox call is deprecated, and is not guaranteed to work as expected. Please use the property framebuffer commands for accessing and defining framebuffer information. See [here](propertiesARM-VC.md)

Channel 1 of mailbox 0 is used.

Mailbox messages:
* Request data: The 28 most significant bits of the address of a buffer
* Response data: 0x0000000 (0x00000001 including the channel identifier)

The buffer must be 16-byte aligned as only the upper 28 bits of the address can be passed via the mailbox.

The buffer contains the following structure:

* u32: Requested width of the physical display
* u32: Requested height of the physical display
* u32: Requested width of the virtual framebuffer
* u32: Requested height of the virtual framebuffer
* u32: Pitch
 * Request: Set to zero
 * Response: Number of bytes between each row of the frame buffer
* u32: Requested depth (bits per pixel)
* u32: Requested X offset of the virtual framebuffer
* u32: Requested Y offset of the virtual framebuffer
* u32: Framebuffer address
 * Request: Set to zero
 * Response: Address of buffer allocated by VC, or zero if request fails
* u32: Framebuffer size
 * Request: Set to zero
 * Response: Size of buffer allocated by VC

All u32 values are little endian.

