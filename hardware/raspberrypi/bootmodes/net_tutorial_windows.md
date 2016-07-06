# Network boot using a Windows Server

This is a summary of the steps needed to set up a Windows Server to act as the DHCP/TFTP server 
so that a Raspberry Pi 3 can boot over the network.

We use the Windows DHCP services, Windows Deplotement Services to act as a TFTP server and the Windows NFS services to 
supply the file system for the booted image.

## _Disclaimer_

These steps may omit detail as I was working this out as I went along and I don't have another Windows 2008 Server 
with which to start again.  I'm also no networking or WDS expert so feel free to correct this.

## DHCP settings

- Setting up of Vendor Option 43.

## Windows Deployment Server

Setting of contents of REMINST share (have to be in root folder)

## Windows NFS services

Appropriate security mode for user mapping

## config.txt

