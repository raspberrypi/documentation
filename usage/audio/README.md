# Playing audio on the Raspberry Pi

To play an MP3 file, navigate to the location of the .mp3 file in the terminal using `cd` and then type the following command: 

```bash
omxplayer example.mp3
```
    
This will play the audio file `example.mp3` through either your monitor's built-in speakers or your headphones - connected via the headphone jack.

If you need an example file you can download one from here using the following command:

```bash
wget http://goo.gl/MOXGX3 -O la.mp3 --no-check-certificate
```

If you cannot hear anything, make sure your headphones or speakers are connected correctly. Be sure to check your audio configuration settings, as described below.

## Audio Configuration

To switch your audio output between HDMI and the headphone jack, use either the `raspi-config` tool or the `amixer` command. See [audio configuration](../../configuration/audio-config.md)
