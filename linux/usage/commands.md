# Linux commands

Here are some fundamental and common Linux commands with example usage:

## Filesystem

### ls

The `ls` command lists the content of the current directory (or one that is specified). It can be used with the `-l` flag to display additional information (permissions, owner, group, size, date and timestamp of last edit) about each file and directory in a list format. The `-a` flag allows you to view files beginning with `.` (i.e. dotfiles).

### cd

Using `cd` changes the current directory to the one specified. You can use relative (i.e. `cd directoryA`) or absolute (i.e. `cd /home/pi/directoryA`) paths.

### pwd

The `pwd` command displays the name of the present working directory: on a Raspberry Pi, entering `pwd` will output something like `/home/pi`.

### mkdir

You can use `mkdir` to create a new directory, e.g. `mkdir newDir` would create the directory `newDir` in the present working directory.

### rmdir

To remove empty directories, use `rmdir`. So, for example, `rmdir oldDir` will remove the directory `oldDir` only if it is empty.

### rm

The command `rm`removes the specified file (or recursively from a directory when used with `-r`). Be careful with this command: files deleted in this way are mostly gone for good!

### cp

Using `cp` makes a copy of a file and places it at the specified location (this is similar to copying and pasting). For example, `cp ~/fileA /home/otherUser/` would copy the file `fileA` from your home directory to that of the user `otherUser` (assuming you have permission to copy it there). This command can either take `FILE FILE` (`cp fileA fileB`), `FILE DIR` (`cp fileA /directoryB/`) or `-r DIR DIR` (which recursively copies the contents of directories) as arguments.

### mv

The `mv` command moves a file and places it at the specified location (so where `cp` performs a 'copy-paste', `mv` performs a 'cut-paste'). The usage is similar to `cp`. So `mv ~/fileA /home/otherUser/` would move the file `fileA` from your home directory to that of the user otherUser. This command can either take `FILE FILE` (`mv fileA fileB`), `FILE DIR` (`mv fileA /directoryB/`) or `DIR DIR` (`mv /directoryB /directoryC`) as arguments. This command is also useful as a method to rename files and directories after they've been created.

### touch

The command `touch` sets the last modified time-stamp of the specified file(s) or creates it if it does not already exist.

### cat

You can use `cat` to list the contents of file(s), e.g. `cat thisFile` will display the contents of `thisFile`. Can be used to list the contents of multiple files, i.e. `cat *.txt` will list the contents of all `.txt` files in the current directory.

### head

The `head` command displays the beginning of a file. Can be used with `-n` to specify the number of lines to show (by default ten), or with `-c` to specify the number of bytes.

### tail

The opposite of `head`, `tail` displays the end of a file. The starting point in the file can be specified either through `-b` for 512 byte blocks, `-c` for bytes, or `-n` for number of lines.

### chmod

You would normally use `chmod` to change the permissions for a file. The `chmod` command can use symbols `u` (user that owns the file), `g` (the files group) ,  and `o` (other users) and the permissions `r` (read), `w` (write), and `x` (execute). Using `chmod u+x *filename*` will add execute permission for the owner of the file.

### chown

The `chown` command changes the user and/or group that owns a file. It normally needs to be run as root using sudo e.g. `sudo chown pi:root *filename*` will change the owner to pi and the group to root. 

### ssh

`ssh` denotes the secure shell. Connect to another computer using an encrypted network connection.
For more details see [SSH (secure shell)](../../remote-access/ssh/)

### scp

The `scp` command copies a file from one computer to another using `ssh`.
For more details see [SCP (secure copy)](../../remote-access/ssh/scp.md)

### sudo

The `sudo` command enables you to run a command as a superuser, or another user. Use `sudo -s` for a superuser shell.
For more details see [Root user / sudo](root.md)

### dd

The `dd` command copies a file converting the file as specified. It is often used to copy an entire disk to a single file or back again. So, for example, `dd if=/dev/sdd of=backup.img` will create a backup image from an SD card or USB disk drive at /dev/sdd. Make sure to use the correct drive when copying an image to the SD card as it can overwrite the entire disk.

### df

Use `df` to display the disk space available and used on the mounted filesystems. Use `df -h` to see the output in a human-readable format using M for MBs rather than showing number of bytes. 

### unzip

The `unzip` command extracts the files from a compressed zip file. 

### tar

Use `tar` to store or extract files from a tape archive file. It can also reduce the space required by compressing the file similar to a zip file. 

To create a compressed file, use `tar -cvzf *filename.tar.gz* *directory/*`
To extract the contents of a file, use `tar -xvzf *filename.tar.gz*`


### pipes

A pipe allows the output from one command to be used as the input for another command. The pipe symbol is a vertical line `|`. For example, to only show the first ten entries of the `ls` command it can be piped through the head command `ls | head`

### tree

Use the `tree` command to show a directory and all subdirectories and files indented as a tree structure.

### &

Run a command in the background with `&`, freeing up the shell for future commands. 

### wget

Download a file from the web directly to the computer with `wget`. So `wget https://www.raspberrypi.org/documentation/linux/usage/commands.md` will download this file to your computer as `commands.md`

### curl

Use `curl` to download or upload a file to/from a server. By default, it will output the file contents of the file to the screen.


### man

Show the manual page for a file with `man`. To find out more, run `man man` to view the manual page of the man command. 


## Search

### grep

Use `grep` to search inside files for certain search patterns. For example, `grep "search" *.txt` will look in all the files in the current directory ending with .txt for the string search.

The `grep` command supports regular expressions which allows special letter combinations to be included in the search.

### awk

`awk` is a programming language useful for searching and manipulating text files.

### find

The `find` command searches a directory and subdirectories for files matching certain patterns. 


### whereis

Use `whereis` to find the location of a command. It looks through standard program locations until it finds the requested command.


## Networking

### ping

The `ping` utility is usually used to check if communication can be made with another host. It can be used with default settings by just specifying a hostname (e.g. `ping raspberrypi.org`) or an IP address (e.g. `ping 8.8.8.8`). It can specify the number of packets to send with the `-c` flag.

### nmap

`nmap` is a network exploration and scanning tool. It can return port and OS information about a host or a range of hosts. Running just `nmap` will display the options available as well as example usage.

### hostname

The `hostname` command displays the current hostname of the system. A privileged (super) user can set the hostname to a new one by supplying it as an argument (e.g. `hostname new-host`).

### ifconfig

Use `ifconfig` to display the network configuration details for the interfaces on the current system when run without any arguments (i.e. `ifconfig`). By supplying the command with the name of an interface (e.g. `eth0` or `lo`) you can then alter the configuration: check the manual page for more details.
