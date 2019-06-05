# Licence key and codec options in config.txt

Hardware decoding of additional codecs on the Pi3 and earlier can be enabled by [purchasing a licence](http://swag.raspberrypi.org/collections/software) that is locked to the CPU serial number of your Raspberry Pi.

On the Pi4 the hardware codecs for MPEG2 or VC1 are permanently disabled, and cannot be enabled even with a licence key. Because of the extra processing power of the Raspberry Pi 4, MPEG2 and VC1 can be decoded in software via applications such as VLC and therefore do not need a HW licence key. 

## decode_MPG2

`decode_MPG2` is a licence key to allow hardware MPEG-2 decoding, e.g. `decode_MPG2=0x12345678`.

## decode_WVC1

`decode_WVC1` is a licence key to allow hardware VC-1 decoding, e.g. `decode_WVC1=0x12345678`.

If you have multiple Raspberry Pis and you've bought a codec licence for each of them, you can list up to eight licence keys in a single `config.txt`, for example `decode_MPG2=0x12345678,0xabcdabcd,0x87654321`. This enables you to swap the same SD card between the different Pis without having to edit `config.txt` each time.




*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
