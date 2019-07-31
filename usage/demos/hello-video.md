# THIS PAGE IS NOW DEPRECATED

# Hello video

This will play a 15 second long full HD 1080p video clip with no sound. The intention here is to demonstrate video decode and playback capability. You’ll see that the video is very smooth!

![Big Buck Bunny screenshot](images/bbb.jpg)
 
Enter the following commands to navigate to the `hello_video` folder and list the files:

```bash
cd ..
cd hello_video
ls
```

You’ll notice the `.bin` file again. This demo needs to be told what video clip to play when we run it, though, so this must be the `test.h264` file (h264 is a type of video codec).

You'll need the `./` to specify the current directory again:

```bash
./hello_video.bin test.h264
```

You should now see the video clip play. It is taken from the open source film [Big Buck Bunny](https://en.wikipedia.org/wiki/Big_Buck_Bunny).
