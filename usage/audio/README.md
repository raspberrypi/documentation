# 在Raspberry Pi 3 上面播放音频文件(.mp3)。

要播放一个MP3 文件, 在终端中使用'cd'命令，导航到 .mp3 文件所在的位置，然后输入以下命令: 

```bash
omxplayer example.mp3
```
    
This will play the audio file `example.mp3` through either your monitor's built-in speakers or your headphones - connected via the headphone jack.

If you need an example file you can download one from here using the following command:

```bash
wget https://goo.gl/XJuOUW -O example.mp3 --no-check-certificate
```

If you cannot hear anything, make sure your headphones or speakers are connected correctly. Note that omxplayer doesn't use ALSA and so ignores the [audio configuration](../../configuration/audio-config.md) set by `raspi-config` or `amixer`.

If omxplayer's auto-detection of the correct audio output device fails, you can force output over hdmi with:

```bash
omxplayer -o hdmi example.mp3
```

or you can force output over the headphone jack with:

```bash
omxplayer -o local example.mp3
```
