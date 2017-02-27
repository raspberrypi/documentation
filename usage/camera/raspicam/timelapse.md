# Timelapse

To create a timelapse video, you simply configure the Raspberry Pi to take a picture at a regular interval, such as every minute, then use an application to stitch the pictures together in a video.

There are a couple of ways of doing this.

## Using Raspistill's inbuilt Timelapse Mode

The raspstill application has a built in timelapse mode, using the `--timelapse` (or `-tl`) command line switch.

The value that follows the switch is the time between shots in milliseconds.
```
raspistill -t 30000 -tl 2000 -o image%04d.jpg
```
Note the `%04d` in the output filename: this indicates the point in the filename where you want a frame count number to appear. So, for example, the command above will produce a capture every two seconds (2000ms), over a total period of 30 seconds (30000ms), named image0001.jpg, image0002.jpg, and so on, through to image0015.jpg.

The `%04d` indicates a four-digit number, with leading zeroes added to make up the required number of digits. So, for example, `%08d` would result in an eight-digit number. You can miss out the `0` if you don't want leading zeroes.

If a timelapse value of 0 is entered, the application will take pictures as fast as possible. Note that there's an minimum enforced pause of approximately 30 milliseconds between captures to ensure that exposure calculations can be made.

## Using Cron

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
