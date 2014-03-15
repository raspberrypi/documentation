# Hello Teapot

This displays a spinning teapot with the video clip from `hello_video` texture-mapped onto its surface. Impressive. You may recognise the teapot model if you're familiar with a piece of software called Blender. This demonstrates Open GL ES rendering and video decode/playback at the same time.

![](./images/teapot.jpg)

```
cd ..
cd hello_teapot
ls
```

Now run the green `.bin` file:

```
./hello_teapot.bin
```

You may receive the following error when you try to run this demo. Don't worry though, you just need to alter one configuration setting to make it work. See below.

```
Note: ensure you have sufficient gpu_mem configured
eglCreateImageKHR: failed to create image for buffer 0x1 target 12465 error 0x300c
eglCreateImageKHR failed.
```

The error means the GPU (graphics processing unit) does not have enough memory to run the demo. It's the GPU that does all the heavy lifting when drawing 3D graphics to the screen (a bit like a graphics card found in a gaming PC). The Raspberry Pi shares its memory/RAM between the CPU and GPU and by default is configured to only give 64 MB of RAM to the GPU. If we increase this to 128 that should do it.

Here is how to do that. Enter the following command:

```
sudo raspi-config
```

This will open up a menu on a blue background. Perform the following actions.
- Go to Advanced Options
- Go to Memory Split
- Delete back 64 and enter 128, press enter
- Go down to Finish
- Say Yes to reboot

After you have logged back in enter the following command to get back to the `hello_teapot` demo.

```
cd /opt/vc/src/hello_pi/hello_teapot
```

Now try and run it again and it should work:

```
./hello_teapot.bin
```

The demo will run forever until you quit. To exit the demo press `Ctrl + C`.
