# rc.local

In order to have a command or program run when the Pi boots, you can add commands to the `rc.local` file. This is especially useful if you want to be able to plug your Pi in to power headless, and have it run a program without configuration or a manual start.

**Note:** [`rc.local`](https://en.wikipedia.org/wiki/Init) finds its origins in the early days of unix, in the 1980's:
 * On Linux systems, `rc.local`, when included, is usually there as a courtesy to the user. It is only suited to execute *simple tasks* that just need to be started and do not need to be stopped in orderly fashion, e.g. when the system shuts down.
 * On Jessie, Stretch and Buster (which use systemd), not all programs will run reliably from `rc.local`, because not all services may be available when it runs. See [systemd](./systemd.md) for a reliable way to have a command or program run when Raspberry Pi boots. A typical systemd unit file will handle starting, stopping a program and also restarting it if it fails.
 * An alternative for scheduled task management is [cron](cron.md).

## Editing rc.local

On your Pi, edit the file `/etc/rc.local` using the editor of your choice. You must edit with super-user (root) access rights, for example:

```
sudo nano /etc/rc.local
```

Add commands below the comment, be sure to leave the line `exit 0` at the end, then save the file and exit. 

## Important considerations

* If your command runs continuously (perhaps runs an infinite loop) or is likely not to quickly exit, you must be sure to fork the process by adding an ampersand to the end of the command, like so:

  ```
  python3 /home/pi/myscript.py &
  ```

  Otherwise, the script will not end and the Pi will not finish booting. The ampersand allows the command to run in a separate process and booting to continue with the process running. Remember that a long-running process started via `rc.local` is unmanaged and will be merely terminated when the system shuts down.

* At boot, commands in `rc.local` are *executed by the system's super-user (root):*
  * This can lead to unexpected behaviour: for example, if a folder is created by a `mkdir` command in the script, the folder would have root ownership and would not be accessible by anyone other than the root user.
  * There is no need to use the [`sudo`](root.md) command to elevate the execution privileges of your program. On the contrary using `sudo` is likely to make execution of your command within `rc.local` fail.
  * Be sure to reference absolute filenames rather than relative to your home folder; for example, `/home/pi/myscript.py` rather than `myscript.py`.
