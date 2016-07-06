# Linux commands

Here are some fundamental and common Linux commands with example usage:

## Filesystem

### ls

Lists the content of the current directory (or one that is specified). Can be used with the `-l` flag to display additional information (permissions, owner, group, size, date and timestamp of last edit) about each file and directory in a list format. The `-a` flag allows you to view files beginning with `.` (i.e. dotfiles).

### cd

Changes the current directory to the one specified. Can use relative (i.e. `cd directoryA`) or absolute (i.e. `cd /home/pi/directoryA`) paths.

### pwd

Displays the name of the current working directory, i.e. `pwd` will output something like `/home/pi`.

### mkdir

Makes a new directory, e.g. `mkdir newDir` would create the directory `newDir` in the present working directory.

### rmdir

Remove empty directories, e.g. `rmdir oldDir` will remove the directory `oldDir` only if it is empty.

### rm

Removes the specified file (or recursively from a directory when used with `-r`). Be careful with this! Files deleted in this way are mostly gone for good!

### cp

Makes a copy of a file and places it at the specified location (essentially doing a 'copy-paste'), for example - `cp ~/fileA /home/otherUser/` would copy the file `fileA` from your home directory to that of the user `otherUser` (assuming you have permission to copy it there!). This command can either take `FILE FILE` (`cp fileA fileB`), `FILE DIR` (`cp fileA /directoryB/`) or `-r DIR DIR` (which recursively copies the contents of directories) as arguments.

### mv

Moves a file and places it at the specified location (so where `cp` performs a 'copy-paste', `mv` performs a 'cut-paste'). The usage is similar to `cp`, so `mv ~/fileA /home/otherUser/` would move the file `fileA` from your home directory to that of the user otherUser. This command can either take `FILE FILE` (`mv fileA fileB`), `FILE DIR` (`mv fileA /directoryB/`) or `DIR DIR` (`mv /directoryB /directoryC`) as arguments. This command is also useful as a method to rename files and directories after they've been created.

### touch

Either sets the last modified time-stamp of the specified file(s) or creates it if it does not already exist.

### cat

Lists the contents of file(s), e.g. `cat thisFile` will display the contents of `thisFile`. Can be used to list the contents of multiple files, i.e. `cat *.txt` will list the contents of all `.txt` files in the current directory.

### head

Displays the beginning of a file. Can be used with `-n` to specify the number of lines to show (by default 10), or with `-c` to specify the number of bytes.

### tail

Displays the end of a file. The starting point in the file can be specified either through `-b` for 512 byte blocks, `-c` for bytes, or `-n` for number of lines.

### chmod

Normally used to change the permissions for a file. The `chmod` command can use symbols `u` (user that owns the file), `g` (the files group) , `o` (other users) and the permissions r (read), w (write) and x (execute). Using `chmod u+x *filename*` will add execute permission for the owner of the file.

### chown

Changes the user and/or group that owns a file. It normally needs to be run as root using sudo e.g. `sudo chown pi:root *filename*` will change the owner to pi and the group to root. 

### ssh

Secure shell. Connect to another computer using an encrypted network connection.
For more details see [SSH (secure shell)](../../remote-access/ssh/)

### scp

Copies a file from one computer to another using ssh.
For more details see [SCP (secure copy)](../../remote-access/ssh/scp.md)

### sudo

Run a command as a superuser, or another user. Use `sudo -s` for a superuser shell.
For more details see [Root user / sudo](root.md)

### dd

Copies a file converting the file as specified. It is often used to copy an entire disk to a single file or back again eg. `dd if=/dev/sdd of=backup.img` will create a backup image from an SD card or USB disk drive at /dev/sdd. Make sure to use the correct drive when copying an image to the SD card as it can overwrite the entire disk.

### df

Display the disk space available and used on the mounted filesystems. Use `df -h` to see the output in a human readable format using M for MBs rather than showing number of bytes. 

### unzip

Extracts the files from a compressed zip file. 

### tar

Store or extract files from a tape archive file. It can also reduce the space required by compressing the file similar to a zip file. 

To create a compressed file use `tar -cvzf *filename.tar.gz* *directory/*`
To extract the contents of a file use `tar -xvzf *filename.tar.gz*`


### pipes

A pipe allows the output from one command to be used as the input for another command. The pipe symbol is a vertical line `|`. For example to only show the first 10 entries of the ls command it can be piped through the head command `ls | head`

### tree

Show a directory and all subdirectories and files indented as a tree structure.

### &

Run a command in the background freeing up the shell for future commands. 

### wget

Download a file from the web directly to the computer e.g. `wget http://www.raspberrypi.org/documentation/linux/usage/commands.md` will download this file to your computer as `commands.md`

### curl

Download or upload a file to/from a server. By default it will output the file contents of the file to the screen.


### man

Show the manual page for a file. To find out more run `man man` to view the manual page of the man command. 


## Search

### grep

Search inside files for certain search patterns e.g. `grep "search" *.txt` will look in all the files in the current directory ending with .txt for the string search.

Supports regular expressions which allows special letter combinations to be included in the search.

### awk

Programming language useful for searching and manipulating text files.

### find

Searches a directory and subdirectories for files matching certain patterns. 


### whereis

Finds the location of a command. Looks through standard program locations until it finds the requested command.



## Networking

### ping

Utility usually used to check if communication can be made with another host. Can be used with default settings by just specifying a hostname (e.g. `ping raspberrypi.org`) or an IP address (e.g. `ping 8.8.8.8`). Can specify the number of packets to send with the `-c` flag.

### nmap

Network exploration and scanning tool. Can return port and OS information about a host or a range of hosts. Running just `nmap` will display the options available as well as example usage.

### hostname

Displays the current hostname of the system. A privileged (super) user can set the hostname to a new one by supplying it as an argument (e.g. `hostname new-host`).

### ifconfig

Displays the network configuration details for the interfaces on the current system when run without any arguments (i.e. `ifconfig`). By supplying the command with the name of an interface (e.g. `eth0` or `lo`) you can then alter the configuration (check the man-page for more details).
