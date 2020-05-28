## Samba/CIFS

Samba is a implementation of the SMB/CIFS networking protocol that is used by Windows devices to provide shared access to files, printers, and serial ports etc. There is a comprehensive [Wikipedia page](https://en.wikipedia.org/wiki/Samba_%28software%29) about Samba and its capabilities.

This page will explain how to use a subset of the Samba system to 'mount' a shared folder on a Windows device so it appears on your Raspberry Pi, or to share a folder on your Raspberry Pi so it can be accessed by a Windows client.

### Installing CIFS/Samba support

By default, Raspberry Pi OS does not include CIFS/Samba support, but this can easily be added. The following commmands will install all the required components for using Samba as a server or a client.

```bash
sudo apt update
sudo apt install samba samba-common-bin smbclient cifs-utils
```

### Using a shared Windows folder

First, you need to share a folder on your Windows device. This is quite a convoluted process!

#### Turn on sharing

1. Open the Networking and Sharing Centre by right-clicking on the system tray and selecting it
1. Click on **Change advanced sharing settings**
1. Select **Turn on network discovery**
1. Select **Turn on file and printer sharing**
1. Save changes

#### Share the folder

You can share any folder you want, but for this example, simply create a folder called `share`. 

1. Create the folder `share` on your desktop.
1. Right-click on the new folder, and select **Properties**.
1. Click on the **Sharing** tab, and then the **Advanced Sharing** button
1. Select **Share this folder**; by default, the share name is the name of the folder
1. Click on the **Permissions** button
1. For this example, select **Everyone** and **Full Control** (you can limit access to specific users if required); click **OK** when done, then **OK** again to leave the **Advanced Sharing** page
1. Click on the **Security** tab, as we now need to configure the same permissions
1. Select the same settings as the **Permissions** tab, adding the chosen user if necessary
1. Click **OK**

The folder should now be shared.

#### Windows 10 Sharing Wizard

On Windows 10 there is a Sharing Wizard that helps with some of these steps.

1. Run the Computer Management application from the Start Bar
1. Select **Shared Folders**, then **Shares**
1. Right-click and select **New Share**, which will start up the Sharing Wizard; click **Next**
1. Select the folder you wish to share, and click **Next**
1. Click **Next** to use all the sharing defaults
1. Select **Custom** and set the required permissions, and click **OK**, then **Finish**

#### Mount the folder on the Raspberry Pi

**Mounting** in Linux is the process of attaching a folder to a location, so firstly we need that location.

```bash
mkdir windowshare
```

Now, we need to mount the remote folder to that location. The remote folder is the host name or IP address of the Windows PC, and the share name used when sharing it. We also need to provide the Windows username that will be used to access the remote machine.

```bash
sudo mount.cifs //<hostname or IP address>/share /home/pi/windowshare -o user=<name>
```

You should now be able to view the content of the Windows share on your Raspberry Pi.

```bash
cd windowshare
ls
```

### Sharing a folder for use by Windows

Firstly, create a folder to share. This example creates a folder called `shared` in the `home` folder of the current user, and  assumes the current user is `pi`.

```bash
cd ~
mkdir shared
```

Now we need to tell Samba to share this folder, using the Samba configuration file.

```bash
sudo nano /etc/samba/smb.conf
```

At the end of the file, add the following to share the folder, giving the remote user read/write permissions:

```
[share]
    path = /home/pi/shared
    read only = no
    public = yes
    writable = yes
```

In the same file, find the `workgroup` line, and if necessary, change it to the name of the workgroup of your local Windows network.

```bash
workgroup = <your workgroup name here>
```

That should be enough to share the folder. On your Windows device, when you browse the network, the folder should appear and you should be able to connect to it.
