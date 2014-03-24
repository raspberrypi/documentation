# Home

When you log in to a Pi and open a Terminal window (or you booted to the command line instead of the graphical user interface), you start in your home folder, which is located at `/home/pi` (assuming your username is `pi`).

This is where your user's own files are kept. The contents of your user's Desktop is in a directory here called `Desktop` along with other files and folders.

To navigate to your home folder on the command line, simply type `cd` and hit `Enter`. This is the equivalent of typing `cd /home/pi` (where `pi` is your username). You can also use the tilde key (`~`), e.g. `cd ~`, which can be used to relatively link back to your home folder, e.g. `cd ~/Desktop/` is the same as `cd /home/pi/Desktop`.

Navigate to `/home/` and run `ls` and you'll see the home folders of each of the users on the system.

Note that if logged in as the root user, typing `cd` or `cd ~` will take you to the root user's home directory, which - unlike normal users - is located at `/root/` not `/home/root/`. Read more about the [root user](../usage/root.md).

If you have files you would not like to lose, you may want to back up your home folder. Read more about [backing up](backup.md).
