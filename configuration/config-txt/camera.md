# Camera Settings in config.txt

## disable_camera_led

Setting `disable_camera_led` to `1` prevents the red camera LED from turning on when recording video or taking a still picture. This is useful for preventing reflections when the camera is facing a window, for example.

Setting `awb_auto_is_greyworld`to `1` allows libraries or applications that do not support the greyworld option internally to capture valid images and videos with NoIR cameras. It switches "auto" awb mode to use the "greyworld" algorithm. This should only be be needed for NoIR cameras, or when the High Quality camera has had its IR filter removed. (see [here](../../hardware/camera/hqcam_filter_removal.md).


*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
