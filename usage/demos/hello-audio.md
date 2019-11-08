# THIS PAGE IS NOW DEPRECATED

# Hello Audio

This demo just demonstrates audio output. It plays a sine wave, which makes a kind of 'WOO WOO WOO' sound.

```bash
cd ..
cd hello_audio
ls
```

Notice the green `.bin` file? Run it. Are you getting the hang of this now?

```bash
./hello_audio.bin
```

This will play the sound over the headphone jack on the Pi. If you're using a HDMI monitor you can make it output over HDMI by adding a `1` to the command:

```bash
./hello_audio.bin 1
```

The demo will run forever until you quit. To exit the demo press `Ctrl + C`.
