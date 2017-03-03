## config.txt - Licence keys/codec Options

Hardware decoding of additional codecs can be enabled by [purchasing a licence](http://swag.raspberrypi.org/collections/software) that is locked to the CPU serial number of your Raspberry Pi.

### decode_MPG2

Licence key to allow hardware MPEG-2 decoding, e.g. `decode_MPG2=0x12345678`.

### decode_WVC1

Licence key to allow hardware VC-1 decoding, e.g. `decode_WVC1=0x12345678`.

If you've got multiple Raspberry Pis and you've bought a codec licence for each of them, you can list up to 8 licence keys in a single `config.txt`, for example `decode_MPG2=0x12345678,0xabcdabcd,0x87654321`. This enables you to swap the same SD card between the different Pis without having to edit `config.txt` each time.




*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
