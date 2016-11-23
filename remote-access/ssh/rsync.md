# rsync

You can use the tool `rsync` to synchronise folders between computers. You might want to transfer some files from your desktop computer or laptop to your Pi, for example, and for them to be kept up to date, or you might want the pictures taken by your Pi transferred to your computer automatically.

Using `rsync` over SSH allows you to transfer files to your computer automatically.

Here is an example of how to set up the sync of a folder of pictures on your Pi to your computer:

On your computer, create a folder called `camera`:

```
mkdir camera
```

Look up the Pi's IP address by logging in to it and running `hostname -I`. In this example, the Pi is creating a timelapse by capturing a photo every minute, and saving the picture with a timestamp in the local folder `camera` on its SD card.

Now run the following command (substituting your own Pi's IP address):

```
rsync -avz -e ssh pi@192.168.1.10:camera/ camera/
```

This will copy all files from the Pi's `camera` folder to your computer's new `camera` folder.

In order to keep the folders in sync, run this command in [cron](../../linux/usage/cron.md).
