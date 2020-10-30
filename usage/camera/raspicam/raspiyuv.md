# raspiyuv

`raspiyuv` has the same set of features as `raspistill` but instead of outputting standard image files such as `.jpg`s, it generates YUV420 or RGB888 image files from the output of the camera ISP.

In most cases using `raspistill` is the best option for standard image capture, but using YUV can be of benefit in certain circumstances. For example if you just need a uncompressed black and white image for computer vision applications, you can simply use the Y channel of a YUV capture.

There are some specific points about the YUV420 files that are required in order to use them correctly. Line stride (or pitch) is a multiple of 32, and each plane of YUV is a multiple of 16 in height. This can mean there may be extra pixels at the end of lines, or gaps between planes, depending on the resolution of the captured image. These gaps are unused.

See [this page](./raw.md) for more details.
