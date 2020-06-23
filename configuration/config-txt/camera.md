# Camera Settings in config.txt

## disable_camera_led

Setting `disable_camera_led` to `1` prevents the red camera LED from turning on when recording video or taking a still picture. This is useful for preventing reflections when the camera is facing a window, for example.

Setting `awb_auto_is_greyworlds`to `1` allows libraries or applications that doesn't support greyworld to capture valid frames and videos with NoIR cameras. It switches "auto" awb mode to select "greyworld" instead. This should be needed for NoIR cameras only, but is needed in case of [Removing the infrared (IR) filter from the Raspberry Pi High Quality Camera](../../hardware/camera/hqcam_filter_removal.md) as well.


*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
