#SSH file transfer protocol
The SSH File Transfer Protocol is a network protocol that provides file access, file transfer, and file management functionalities over SSH.

By using SFTP you can easily change, browse and edit files on your raspberry pi. To do this you need to install Filezilla client (for windows) and enable SSH access on your raspberry pi. SFTP is easier than FTP because the standard Raspberry distributions already have installed a SSH server.

##Windows using Filezilla

Download the latest Filezilla Client version from [filezilla project.org](https://filezilla-project.org/)

When installed the Filezilla Client, go to File> Site manager

Fill in the IP address, user name and password (by default the user name is 'pi' and the password 'raspberry') of your raspberry pi in the dialog and choose SFTP as protocol.

Click connect and you will see the home folder of the user.

##Ubuntu using Nautilus

Open Nautilus on the client machine
Select File > Connect to Server
Type: SSH
Server: Enter your host machine's IP address
Port: port number specified in host machine's sshd_config file
User name: 'pi'
Password: 'raspberry'

##Other platforms
Filezilla is available for every platform so the method for windows can be used for every platform.
