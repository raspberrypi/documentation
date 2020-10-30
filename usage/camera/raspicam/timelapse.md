# Time-lapse

To create a time-lapse video, you simply configure the Raspberry Pi to take a picture at a regular interval, such as once a minute, then use an application to stitch the pictures together into a video. There are a couple of ways of doing this.

## Using raspistill's inbuilt time-lapse mode

The `raspistill` application has a built in time-lapse mode, using the `--timelapse` (or `-tl`) command line switch. The value that follows the switch is the time between shots in milliseconds:
```
raspistill -t 30000 -tl 2000 -o image%04d.jpg
```
Note the `%04d` in the output filename: this indicates the point in the filename where you want a frame count number to appear. So, for example, the command above will produce a capture every two seconds (2000ms), over a total period of 30 seconds (30000ms), named image0001.jpg, image0002.jpg, and so on, through to image0015.jpg.

The `%04d` indicates a four-digit number, with leading zeros added to make up the required number of digits. So, for example, `%08d` would result in an eight-digit number. You can miss out the `0` if you don't want leading zeros.

If a timelapse value of 0 is entered, the application will take pictures as fast as possible. Note that there's an minimum enforced pause of approximately 30 milliseconds between captures to ensure that exposure calculations can be made.

## Using cron

A good way to automate taking a picture at a regular interval is using `cron`. Open the cron table for editing:

```
crontab -e
```

This will either ask which editor you would like to use, or open in your default editor. Once you have the file open in an editor, add the following line to schedule taking a picture every minute (referring to the Bash script from the [raspistill page](raspistill.md)):

```
* * * * * /home/pi/camera.sh 2>&1
```

Save and exit and you should see the message:

```
crontab: installing new crontab
```

Make sure that you use e.g. `%04d` to make `raspistill` output each image to a new file: if you don't, then each time `raspistill` writes an image it will overwrite the same file.

## Stitching images together

Now you'll need to stitch the photos together into a video. You can do this on the Pi using `mencoder` but the processing will be slow. You may prefer to transfer the image files to your desktop computer or laptop and produce the video there.

Navigate to the folder containing all your images and list the file names in to a text file. For example:

```
ls *.jpg > stills.txt
```
### On the Raspberry Pi

Although it will be slow (due to encoding in software rather than using the Raspberry Pi hardware acceleration), you can stitch your JPEG images together using various available tools. This documentation will use `avconv`, which needs to be installed.
```
sudo apt install libav-tools
```
Now you can use the tools to convert your JPEG files in to an H264 video file:
```
avconv -r 10 -i image%04d.jpg -r 10 -vcodec libx264 -vf scale=1280:720 timelapse.mp4
```
On a Raspberry Pi 3, this can encode a little more than one frame per second. The performance of other Pi models will vary. The parameters used are:

 - -r 10 Assume ten frames per second in input and output files.
 - -i image%04.jpg The input file specification (to match the files produced during the capture).
 - -vcodec libx264 Use the software x264 encoder.
 - -vf scale=1280:720 Scale to 720p. You can also use 1920:1080, or lower resolutions, depending on your requirements. Note the Pi can only play back up to 1080p video, but if you are intending to play back at, for example, 4K, you could set that here.
 - timelapse.mp4 The name of the output file.

`avconv` has a comprehensive parameter set for varying encoding options and other settings. These can be listed using `avconv --help`.

### On another Linux computer

You can use the same instructions as for the Raspberry Pi, or an alternative package such as `mencoder`:

```
sudo apt install mencoder
```

Now run the following command:

```
mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 -o timelapse.avi -mf type=jpeg:fps=24 mf://@stills.txt
```

Once that's completed, you should have a video file called `timelapse.avi` containing a time-lapse from your images.
