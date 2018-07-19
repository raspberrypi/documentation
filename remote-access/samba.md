## Samba/CIFS

Samba is a re-implementation of the SMB/CIFS networking protocol, which is used by Wi ndows devices to providing shared access to files, printers, and serial ports etc. There is a comprehensive [Wikipedia page](https://en.wikipedia.org/wiki/Samba_(software)) for Samba.

This page will explain how to 'mount' a shared folder on a Windows device so it appears on your Raspberry Pi, or to share a folder on your Raspberry Pi so it can be accessed by a Windows Client.

### Installing CIFS/Samba support

By default, Raspbian does not include CIFS/Samba support, but it can easily be added. The following commmand will install all the required components for using Samba as a server or a client.
```
sudo apt-get update
sudo apt-get install -y samba samba-common-bin smbclient cifs-utils
```

### Using a shared Windows folder

First, you need to share a folder on your windows device. This is quite a convoluted process!

#### Turn on sharing

1. Open the Networking and Sharing Centre by right clicking on the system tray and selecting.
2. Click on `Change advanced sharing settings`
3. Select Turn on network discovery
4. Select Turn on  file and printer sharing
5. Save changes

#### Share the folder

You can share any folder you want, but for this example simply create a folder called share. 

1. Create the folder `share` on your desktop.
2. Right click on the new folder, and select Properties.
3. Click on the Sharing tab, and then the Advanced Sharing button
4. Select `Share this folder`. By defual the share name is the name of the folder.
5. Click on the Permissions button.
6. For this example, select Everyone and click Full Control. You can limit access to specific users if required.


### Sharing a folder for use by Windows

Firstly, create a folder to share, this example creates a folder called shared in the home folder of the current user, this page assumes the current user is the `pi`.
```
cd ~
mkdir shared
```

Now we need to tell Samba to share this folder, using the samba configuration file.
```
sudo nano /etc/samba/smb.conf
```
At the end of the file, add the following to share the folder, giving the remote user read/write permissions.
```
[share]
    path = /home/pi/shared
    available = yes
    valid users = pi
    read only = no
    browsable = yes
    public = yes
    writable = yes
```
In the same file, find the `workgroup` line, and if necessary change it to the name of the workgroup of your local Windows network.
```
workgroup = <your workgroup name here>
```

That should be enough to share the folder. On your windows device, when you browse the network, the folder should appear and you should be able to connect to it.



