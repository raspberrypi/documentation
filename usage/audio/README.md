# 在Raspberry Pi 3 上面播放音频文件(.mp3)。

要播放一个MP3 文件, 在终端中使用'cd'命令，导航到 .mp3 文件所在的位置，然后输入以下命令: 

```bash
omxplayer example.mp3
```
    
这将会播放音频文件 `example.mp3` 要么通过你的监视器内置的扬声器要么通过你的耳机-使用耳机口连接的.

如果你需要一个示例文件你可以使用以下命令从这里下载一个：

```bash
wget https://goo.gl/XJuOUW -O example.mp3 --no-check-certificate
```

如果你不能听到任何东西, 检查你的耳机或者扬声器是否已经正确地连接。 要注意 omxplayer 不使用 ALSA ，所以忽略这个 [audio configuration](../../configuration/audio-config.md) 搁在一旁 `raspi-config` or `amixer`.

如果 omxplayer的自动检测无法识别正确的声音输出设备，你可以通过HDMI强制输出它：

```bash
omxplayer -o hdmi example.mp3
```

或者通过耳机空强制输出它：

```bash
omxplayer -o local example.mp3
```
