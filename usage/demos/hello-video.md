# Hello video

This will play a 15 second long full HD 1080p video clip with no sound, the intention here is to demonstrate video decode and playback capability. You'll see it's very smooth!

![](./images/bbb.jpg)
 
 Enter the following commands to navigate to the `hello_video` folder and list the files.

 ```
 cd ..
 cd hello_video
 ls
 ```

 You'll notice the `.bin` file again. This demo needs to be told what video clip to play when we run it though, so this must be the `test.h264` file (h264 is a type of video codec).

 You'll need the `./` to specify the current directory again.

 ```
 ./hello_video.bin test.h264
 ```
