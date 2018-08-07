# rc.local

In order to have a command or program run when the Pi boots, you can add commands to the `rc.local` file. This is especially useful if you want to be able to plug your Pi in to power headless, and have it run a program without configuration or a manual start.

An alternative for scheduled task management is [cron](cron.md).

## Editing rc.local

On your Pi, edit the file `/etc/rc.local` using the editor of your choice. You must edit with root, for example:

```bash
sudo nano /etc/rc.local
```

Add commands below the comment, but leave the line `exit 0` at the end, then save the file and exit.

### Warning

If your command runs continuously (perhaps runs an infinite loop) or is likely not to exit, you must be sure to fork the process by adding an ampersand to the end of the command, like so:

```
python3 /home/pi/myscript.py &
```

Otherwise, the script will not end and the Pi will not boot. The ampersand allows the command to run in a separate process and continue booting with the process running.

Also, be sure to reference absolute filenames rather than relative to your home folder; for example, `/home/pi/myscript.py` rather than `myscript.py`.
