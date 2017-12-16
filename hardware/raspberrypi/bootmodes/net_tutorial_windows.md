# Network boot using a Windows Server

This is a summary of the steps needed to set up a Windows Server to act as the DHCP/TFTP server 
so that a Raspberry Pi 3 can boot over the network.

We use the Windows DHCP services, Windows Deployment Services to act as a TFTP server and the Windows 
NFS services to supply the file system for the booted image. My particular server is a HP Proliant 
Microserver running Windows 2008 R2.

## _Disclaimer_

These steps may omit detail as I was working this out as I went along and I don't have another Windows 2008 Server 
with which to start again.  I'm also no networking or WDS expert so feel free to correct this.

A lot of this document was written after the fact so there may be the odd step that I've missed out.  Hopefully it is enough to get an experienced Windows Administrator heading in the right direction.


## DHCP settings

This is an area that could be improved.  I have my Windows 2008 Server set up as DHCP server for my network, 
however for the Raspberry Pi to boot from the network it needs to receive a specific BOOTP option back from the DHCP Server.
This is '043 Vendor Specific Info'.  I used the DHCP MMC plugin to add the this option to my DHCP scope.  The data for this option I set to :

2B 20 06 01 03 0A 04 00 50 58 45 14 00 00 11 52 61 73 70 62 65 72 72 79 20 50 69 20 42 6F 6F 74 FF

I determined this string by running a trace of a successful boot when using a Pi as a DHCP server.  I've noticed that WireShark complains about 
the structure of this option so I may have not get it set perfectly but it was enough for the Pi to recognise the DHCP server as one
from which it could try to network boot.

One thing that troubled me is that this Vendor option will be sent to all of the DHCP clients and not just Pis.  I think that
this can be resolved by defining of Vendor Classes on the server and recognising the client as a Pi but I have not had time to fully explore this.

## Windows Deployment Service

Windows Deployment Services is the server role that supports TFTP.  For Windows clients it support a rich set of functionality 
but we only need its TFTP services.  You are may have to add the WDS role to your server.

WDS creates a REMINST share where the TFTP files will be located.  I used Windows explore to navigate to \\servername\REMINST
and then copied on the boot directory (including sub-directories) for the Pi into that location (including the updated bootcode.bin and start.elf).

As with DHCP I'm not sure how adding the Pi contents to the WDS folders may impact normal Windows operation of WDS as
I don't use that on my network.

## Windows NFS services

The steps above should allow the Pi to at least boot but won't have the rest of the file system.
We now need add the Services for NFS role to our server.  Once they are installed we can create NFS shares that the Pi can use.

I created a folder to contain the Pi's file system and then right-click the folder and choose properties and go to the 
'NFS Sharing' tab and click on the button 'Manage NFS Sharing'.  I called the share 'PiRoot' and chose the 'No server authentication [Auth_Sys]', 'Enable unmapped user access', 'Allow unmapped User Unix access' options.
I believe these allow user permissions and ownerships to work in the best way.

I then booted up a normal Pi and copied the whole file system across to the newly created PiRoot share on the Windows server.

## cmdline.txt

Lastly I modified the cmdline.txt to point to the PiRoot NFS folder

    root=/dev/nfs rootfstype=nfs nfsroot=192.168.10.200:/PiRoot/ rw ip=dhcp rootwait

	
