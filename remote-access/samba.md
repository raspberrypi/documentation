## Samba/CIFS

Samba is a implementation of the SMB/CIFS networking protocol which is used by Windows devices to providing shared access to files, printers, and serial ports etc. There is a comprehensive [Wikipedia page](https://en.wikipedia.org/wiki/Samba_(software)) which describes Samba and its capabilities.

This page will explain how to use a subset of the Samba system to 'mount' a shared folder on a Windows device so it appears on your Raspberry Pi, or to share a folder on your Raspberry Pi so it can be accessed by a Windows Client.

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
6. For this example, select Everyone and click Full Control. You can limit access to specific users if required. Click OK when done, then OK again to leave the Advanced Sharing page.
7. Click on the security tab, as we now need to configure the same permissions.
8. Select the same settings as the Permissions tab, adding the user used if necessary.
9. Click OK. The folder should now be shared.

#### Windows 10 Share Wizard

On Windows 10 there is a Sharing Wizard which helps with some of these steps.

1. Run the Computer Management application, from the Start Bar
2. Select Shared Folders then Shares
3. Right click and select New Share, this will bring up a Sharing Wizard, click Next
4. Select the folder you wish to share, click Next
5. Click Next to use all the defaults
6. Select Custom and set the required permissions, click OK then Finish

#### Mount the folder on the Raspberry Pi

'Mounting' in Linux is the process of attaching a folder to a location, so firstly we need that location. 
```mkdir windowshare```

Now, we need to mount the remote folder to that location. The remote folder is the hostname or IP address of the Windows PC, and the share name used when sharing it. We also need to provide the Windows username that will be used to access the remote machine.

```sudo mount.cifs //<hostname or IP address>/share /home/pi/windowshare -o user=<name>```

You should now be able to view the content of the Windows share on your Raspberry Pi.

```
cd windowshare
ls
```

### Sharing a folder for use by Windows

Firstly, create a folder to share, this example creates a folder called shared in the home folder of the current user, this page assumes the current user is `pi`.
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



