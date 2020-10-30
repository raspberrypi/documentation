# Using RAW on the Raspberry Pi cameras

The definition of raw images can vary. The usual meaning is raw Bayer data directly from the sensor, although some may regard an uncompressed image that has passed through the ISP (and has therefore been processed) as raw.

Both options are available from the Raspberry Pi cameras.

## Processed, non-lossy images

The usual output from `raspistill` is a compressed JPEG file that has passed through all the stages of image processing to produce a high-quality image. However, JPEG, being a lossy format does throw away some information that the user may want.

`raspistill` has an `encoding` option that allows you to specify the output format: either `jpg`, `gif`, `bmp` or `png`. The latter two are non-lossy, so no data is thrown away in an effort to improve compression, but do require conversion from the original YUV, and because these formats do not have hardware support they produce images slightly more slowly than JPEG.

e.g.

`raspistill --encoding png -o fred.png`

Another option is to use the [`raspiyuv`](./raspiyuv.md) application. This avoids any final formatting stage, and writes raw YUV420 or RGB888 data to the requested file. YUV420 is the format used in much of the ISP, so this can be regarded as a dump of the processed image data at the end of the ISP processing.

## Unprocessed images

For some applications, such as astrophotography, having the raw Bayer data direct from the sensor can be useful. This data will need to be post-processed to produce a useful image.

`raspistill` has a raw option that will append this raw Bayer data onto the end of the output JPEG file.

`raspistill --raw -o fred.jpg`

The raw data will need to be extracted from the `JPEG` file. Information on doing this can be found [here](https://www.raspberrypi.org/blog/processing-raw-image-files-from-a-raspberry-pi-high-quality-camera/)
