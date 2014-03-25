# Time-lapse

To create a time-lapse video, you simply configure the Raspberry Pi to take a picture at a regular interval, such as every minute, then use an application to stitch the pictures together in a video.

A good way to automate taking a picture at a regular interval is using `cron`.

Open the cron table for editing:

```
crontab -e
```

This will either ask which editor you would like to use, or open in your default editor. Once you have the file open in an editor, add the following line to schedule taking a picture every minute (referring to the Bash script from the [previous page](raspistill.md)):

```
* * * * * /home/pi/camera.sh 2>&1
```

Save and exit and you should see the message:

```
crontab: installing new crontab
```

Ensure your scipt does not save each picture taken with the same filename. This will overwrite the picture each time.

## Stitching images together

Now you'll need to stitch the photos together in to a video.

You can do this on the Pi using `mencoder` but the processing will be slow. You may prefer to transfer the image files to your desktop computer or laptop and processing the video there.

Navigate to the folder containing all your images and list the file names in to a text file. For example:

```
ls *.jpg > stills.txt
```

### On Raspberry Pi or other Linux computer

Install the package `mencoder`:

```
sudo apt-get install mencoder
```

Now run the following command:

```
mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 -o timelapse.avi -mf type=jpeg:fps=24 mf://@stills.txt
```

Once that's completed, you should have a video file called `timelapse.avi` containing a time-lapse from your images.

### On Mac OS



### On Windows
