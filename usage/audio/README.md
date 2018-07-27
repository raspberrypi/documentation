# Playing audio on the Raspberry Pi

To play an MP3 file, navigate to the location of the `.mp3` file in the terminal using `cd` and then type the following command: 

```bash
omxplayer example.mp3
```
    
This will play the audio file `example.mp3` through either your monitor's built-in speakers or your headphones, connected via the headphone jack.

If you need an example file you can download one from here using the following command:

```bash
wget http://rpf.io/lamp3 -O example.mp3 --no-check-certificate
```

If you cannot hear anything, make sure your headphones or speakers are connected correctly. Note that omxplayer doesn't use ALSA and so ignores the [audio configuration](../../configuration/audio-config.md) set by `raspi-config` or `amixer`.

If omxplayer's auto-detection of the correct audio output device fails, you can force output over HDMI with:

```bash
omxplayer -o hdmi example.mp3
```

Alternatively, you can force output over the headphone jack with:

```bash
omxplayer -o local example.mp3
```

You can even force output over both the headphone jack and HDMI with:

```bash
omxplayer -o both example.mp3
```
## Using omxplayer as a background job

omxplayer will close if run in the background without tty (user input).

To circumvent this (and disable keyboard input), run with:

```bash
omxplayer --no-keys example.mp3 &
```

You can then check the status of the job you just spawned using `jobs`, and kill it using `kill`:

```bash
$ jobs
[1]-  Running             omxplayer --no-keys example.mp3 &
$ kill %1
$
[1]-  Terminated          omxplayer --no-keys example.mp3 &
```
