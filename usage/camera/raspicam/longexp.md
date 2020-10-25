# Long exposures

The different camera modules have different capabilities with regard to exposure times:

| Module | Max exposure (seconds) |
| - | :-: |
|V1 (OMx5647) | 6 |
|V2 (IMX219)  | 10 |
|HQ (IMX417)  | 230 |



Due to the way the ISP works, by default asking for a long exposure can result in the capture process taking up to 7 times the exposure time, so a 200 second exposure on the HQ camera could take 1400 seconds to actually return an image. This is due to the way the camera system works out the correct exposures and gains to use in the image, using it's AGC (automatic gain control) and AWB (automatic white balance) algorithms. The system needs a few frames to calculate these numbers in order to produce a decent image. When combined with frame discards at the start of processing (in case they are corrupt), and the switching between preview and captures modes, this can result in up to 7 frames needed to produce a final image. With long exposures, that can take a long time.

Fortunately, the camera parameters can be altered to reduce frame time dramatically; however this means turning off the automatic algorithms and manually providing values for the AGC and, if required, AWB. In addition, a burst mode can be used to mitigate the effects of moving between preview and captures modes.

For the HQ camera, the following example will take a 100 second exposure.

`raspistill -t 10 -bm -ex off -ag 1 -ss 100000000 -st -o long_exposure.jpg`

This example turns on burst mode (`-bm`) which will disable the preview switching, turns off automatic gain control and manually sets it to 1 (`-ag 1`). The `-st` option forces statistics like AWB to be calculated from the captured frame, avoiding the need to provide specific values, although these can be entered if necessary.


