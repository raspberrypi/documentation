# Using a standard USB webcam

Rather than using the Raspberry Pi [camera module](../camera/README.md), you can use a standard USB webcam to take pictures and video on the Raspberry Pi.

Note that the quality and configurability of the camera module is highly superior to a standard USB webcam.

## Install fswebcam

First, install the `fswebcam` package:

```bash
sudo apt install fswebcam
```

## Add your user to `video` group

If you are not using the default `pi` user account, you need to add your username to the `video` group, otherwise you will see 'permission denied' errors.

```bash
sudo usermod -a -G video <username>
```

To check that the user has been added to the group correctly, use the `groups` command. 

## Basic usage

Enter the command `fswebcam` followed by a filename and a picture will be taken using the webcam, and saved to the filename specified:

```bash
fswebcam image.jpg
```

This command will show the following information:

```
--- Opening /dev/video0...
Trying source module v4l2...
/dev/video0 opened.
No input was specified, using the first.
Adjusting resolution from 384x288 to 352x288.
--- Capturing frame...
Corrupt JPEG data: 2 extraneous bytes before marker 0xd4
Captured frame in 0.00 seconds.
--- Processing captured image...
Writing JPEG image to 'image.jpg'.
```

![Basic image capture](images/image.jpg)

Note the small default resolution used, and the presence of a banner showing the timestamp.

### Specify resolution

The webcam used in this example has a resolution of `1280 x 720` so to specify the resolution I want the image to be taken at, use the `-r` flag:

```bash
fswebcam -r 1280x720 image2.jpg
```

This command will show the following information:

```
--- Opening /dev/video0...
Trying source module v4l2...
/dev/video0 opened.
No input was specified, using the first.
--- Capturing frame...
Corrupt JPEG data: 1 extraneous bytes before marker 0xd5
Captured frame in 0.00 seconds.
--- Processing captured image...
Writing JPEG image to 'image2.jpg'.
```

![Full resolution image](images/image2.jpg)

Picture now taken at the full resolution of the webcam, with the banner present.

### Specify no banner

Now add the `--no-banner` flag:

```bash
fswebcam -r 1280x720 --no-banner image3.jpg
```

which shows the following information:

```
--- Opening /dev/video0...
Trying source module v4l2...
/dev/video0 opened.
No input was specified, using the first.
--- Capturing frame...
Corrupt JPEG data: 2 extraneous bytes before marker 0xd6
Captured frame in 0.00 seconds.
--- Processing captured image...
Disabling banner.
Writing JPEG image to 'image3.jpg'.
```

![Full resolution image with no banner](images/image3.jpg)

Now the picture is taken at full resolution with no banner.

## Bad Pictures

You may experience poor quality pictures with a USB webcam, such as this accidentally artistic piece:

![Bad webcam picture](images/jack.jpg)

Some webcams are more reliable than others, but this sort of issue may occur with poor quality webcams. If the problem persists, ensure your system is [up to date](../../raspbian/updating.md). Also try other webcams, but you'll get the best performance from the Raspberry Pi [camera module](https://www.raspberrypi.org/help/camera-module-setup/).

## Bash script

You can write a Bash script which takes a picture with the webcam. The script below saves the images in the `/home/pi/webcam` directory, so create the `webcam` subdirectory first with:

```bash
mkdir webcam
```

To create a script, open up your editor of choice and write the following example code:

```bash
#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

fswebcam -r 1280x720 --no-banner /home/pi/webcam/$DATE.jpg
```

This script will take a picture and name the file with a timestamp. Say we saved it as `webcam.sh`, we would first make the file executable:

```bash
chmod +x webcam.sh
```

Then run with:

```bash
./webcam.sh
```

Which would run the commands in the file and give the usual output:

```
--- Opening /dev/video0...
Trying source module v4l2...
/dev/video0 opened.
No input was specified, using the first.
--- Capturing frame...
Corrupt JPEG data: 2 extraneous bytes before marker 0xd6
Captured frame in 0.00 seconds.
--- Processing captured image...
Disabling banner.
Writing JPEG image to '/home/pi/webcam/2013-06-07_2338.jpg'.
```

## Time-lapse using cron

You can use `cron` to schedule taking a picture at a given interval, such as every minute to capture a time-lapse.

First open the cron table for editing:

```
crontab -e
```

This will either ask which editor you would like to use, or open in your default editor. Once you have the file open in an editor, add the following line to schedule taking a picture every minute (referring to the Bash script from above):

```bash
* * * * * /home/pi/webcam.sh 2>&1
```

Save and exit and you should see the message:

```bash
crontab: installing new crontab
```

Ensure your script does not save each picture taken with the same filename. This will overwrite the picture each time.

## Other Useful tools

Other tools are available that may come in handy when using the camera or a webcam:

- [SSH](../../remote-access/ssh/README.md)
    - Use SSH to remotely access the Raspberry Pi over your local network
- [SCP](../../remote-access/ssh/scp.md)
    - Copy files over SSH to get copies of pictures taken on the Pi on your main computer
- [rsync](../../remote-access/ssh/rsync.md)
    - Use `rsync` to synchronise the folder of pictures taken in a folder between your Pi to your computer
- [cron](../../linux/usage/cron.md)
    - Use `cron` to schedule taking a picture at a given interval, such as every minute to capture a time-lapse
