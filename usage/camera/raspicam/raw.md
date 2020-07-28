# Using RAW on the Raspberry pi cameras

The definition of raw images can vary. The usual meaning is raw bayer data directly from the sensor, although more unusually, some may regard an uncompressed image that has passed through the ISP (and has therefor been processed) as raw.

Both options are available from the Raspberry Pi camera.

## Processed, non-lossy images

The usual output from raspistill is a compressed JPEG file that has passed through all the stages of image processing to produce a high quality image. However, JPEG, being a lossy format does throw away from some information that the user may want.

`raspstill` has an `encoding` option that allows you to specify the output format. Options are `jpg`, `bmp`, `gif` and `png`. The latter three are non-lossy, so no data is thrown away in an effort to improve compression. Because these formats do not have hardware support they produce images slighly more slowly than JPEG.

e.g.

`raspstill --encoding png -o  fred.png`

Another option is to use the [`raspiyuv`](./raspiyuv.md) application. This avoids any final formatting stage, and writes raw YUV420 data to the requested file. YUV420 is the format used in much of the ISP, so this can be regarded as a dump of the processed image data at the end of the ISP processing.

## Unprocessed images

For some applications, having the raw Bayer data direct from the sensor can be useful (e.g. astrophotography). This data will need to be post processed to produce a useful image.

`raspistill` has a raw option that will append this raw bayer data on to the end of the output JPEG file.

`raspstill --raw -o fred.jpg`

The raw data will need to be extracted from the `JPEG` file.