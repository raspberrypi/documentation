# NFS - Network File System

The "Network File System" allows you to share a directory located on one networked computer with other computers/devices on that network. The computer where directory located is called the server and computers or devices connecting to that server are called clients. Clients usually 'mount' the shared directory to make it a part of their own directory structure.

For smaller networks it is perfect for creating a simple NAS (Networked Attached Storage) in a Linux/Unix environment.

It is perhaps suited for more permanent network mounted directories such as `/home` directories or regularly accessed shared resources. If you want a network share that guest users can easily connect to, Samba is more suited. This is because tools exist more readily across old and proprietary operating systems to temporarily mount and detach from Samba shares.

Ubuntu Before deploying NFS you should be familiar with:

1. Linux file and directory permissions
1. Mounting and unmounting filesystems

### Setup a basic NFS server

Install the below packages:

```bash
sudo apt install nfs-kernel-server
```

For easier maintenance we will isolate all NFS exports in single directory, where the real directories will be mounted with the --bind option.

Suppose we want to export our users' home directories in /home/users. First we create the export filesystem:

```bash
sudo mkdir -p /export/users
```

Note that /export and /export/users will need 777 permissions as we will be accessing the NFS share from the client without LDAP/NIS authentication. This will not apply if using authentication (see below). Now mount the real users directory with:

```bash
sudo mount --bind /home/users /export/users
```

To save us from retyping this after every reboot we add the following line to `/etc/fstab` like so:

```
/home/users    /export/users   none    bind  0  0
```

There are three configuration files that relate to an NFS server:

1. `/etc/default/nfs-kernel-server`
1. `/etc/default/nfs-common`
1. `/etc/exports`

The only important option in `/etc/default/nfs-kernel-server` for now is `NEED_SVCGSSD`. It is set to "no" by default, which is fine, because we are not activating NFSv4 security this time.

In order for the ID names to be automatically mapped, both the client and server require the `/etc/idmapd.conf` file to have the same contents with the correct domain names. Furthermore, this file should have the following lines in the Mapping section:

```
[Mapping]

Nobody-User = nobody
Nobody-Group = nogroup
```

Please note that the client may have different requirements for the Nobody-User and Nobody-Group. On RedHat variants, it is nfsnobody for both. So to ensure that these are actually present, check via the following commands to see if `nobody` is there:

```bash
cat /etc/passwd
cat /etc/group
```

This way, server and client do not need the users to share same UID/GUID. For those who use LDAP-based authentication, add the following lines to the idmapd.conf of your clients:

```
[Translation]

Method = nsswitch
```

This will cause idmapd to know to look at nsswitch.conf to determine where it should look for credential information. If you have LDAP authentication already working, nsswitch shouldn't require further explanation.

To export our directories to a local network 192.168.1.0/24 we add the following two lines to `/etc/exports`:

```
/export       192.168.1.0/24(rw,fsid=0,insecure,no_subtree_check,async)
/export/users 192.168.1.0/24(rw,nohide,insecure,no_subtree_check,async)
```

#### Portmap lockdown - optional

Add the following line to `/etc/hosts.deny`:

```
rpcbind mountd nfsd statd lockd rquotad : ALL
```

By blocking all clients first, only clients in `/etc/hosts.allow` below will be allowed to access the server.

Now add the following line to `/etc/hosts.allow`:

```
rpcbind mountd nfsd statd lockd rquotad : <list of IPv4s>
```

Where "list of IPv4" is a list of IP addresses that consists of the server and all clients. These have to be IP addresses because of a limitation in rpcbind, which it doesn't like hostnames. Note that if you have NIS set up, just add these to the same line.

Please ensure that the list of authorised IP addresses includes the localhost address (127.0.0.1) as the startup scripts in recent versions of Ubuntu use the rpcinfo command to discover NFSv3 support, and this will be disabled if localhost is unable to connect.

Afterwards, go ahead and restart the service:

```bash
sudo systemctl restart nfs-kernel-server
```

### Setup a NFSv4 client

Install the required packages:

```bash
sudo apt install nfs-common
```

On the client we can mount the complete export tree with one command:

```bash
mount -t nfs -o proto=tcp,port=2049 <nfs-server-IP>:/ /mnt
```

You can also specify the NFS server hostname instead of its IP, but in this case you need to assure the hostname can be resolved to an IP on the client side. A robust way of ensuring this will always resolve is to use `/etc/hosts` file.

Note that `<nfs-server-IP>:/export` is not necessary in NFSv4, as it was in NFSv3. The root export :/ defaults to export with fsid=0.

We can also mount an exported subtree with:

```bash
mount -t nfs -o proto=tcp,port=2049 <nfs-server-IP>:/users /home/users
```

To ensure this is mounted on every reboot, add the following line to `/etc/fstab`:

```
<nfs-server-IP>:/   /mnt   nfs    auto  0  0
```

If after mounting, the entry in `/proc/mounts appears` as `<nfs-server-IP>://` (with two slashes), then you might need to specify two slashes in `/etc/fstab`, or else umount might complain that it cannot find the mount.

#### Portmap lockdown - optional

Add the following line to `/etc/hosts.deny`:

```
rpcbind : ALL
```

By blocking all clients first, only clients in `/etc/hosts.allow` below will be allowed to access the server.

Now add the following line to `/etc/hosts.allow`:

```
rpcbind : <NFS server IP address>
```

Where "NFS server IP address" is the IP address of the server.

### NFS Server with complex user permissions

NFS user permissions are based on user ID (UID). UIDs of any users on the client must match those on the server in order for the users to have access. The typical ways of doing this are:

1. Manual password file synchronization

1. Use of LDAP

1. Use of DNS

1. Use of NIS

Note that you have to be careful on systems where the main user has root access - that user can change UID's on the system to allow themselves access to anyone's files. This page assumes that the administrative team is the only group with root access and that they are all trusted. Anything else represents a more advanced configuration, and will not be addressed here.

#### Group permissions

File access is determined by his/her membership of groups on the client, not on the server. However, there is an important limitation: a maximum of 16 groups are passed from the client to the server, and, if a user is member of more than 16 groups on the client, some files or directories might be unexpectedly inaccessible.

#### DNS - optional, only if using DNS

Add any client name and IP addresses to `/etc/hosts`. The IP address of the server should already be here. This ensures that NFS will still work even if DNS goes down. You could rely on DNS if you wanted, it's up to you.

#### NIS - optional, only if using NIS

This applies to clients utilizing NIS. Otherwise you can't use netgroups and should specify individual IPs or hostnames in `/etc/exports`. Read the BUGS section in man netgroup.

Edit `/etc/netgroup` and add a line to classify your clients. (This step is not necessary, but is for convenience).

```
myclients (client1,,) (client2,,)
```

Where `myclients` is the netgroup name

Run this command to rebuild the YP database:

```bash
sudo make -C /var/yp
```

#### Portmap Lockdown - optional

Add the following line to `/etc/hosts.deny`:

```
rpcbind mountd nfsd statd lockd rquotad : ALL
```

By blocking all clients first, only clients in `/etc/hosts.allow` below will be allowed to access the server. Consider adding the following line:

```
rpcbind mountd nfsd statd lockd rquotad : <list of IPs>
```

Where the "list of IPs" is a list of IP addresses that consists of the server and all clients. These have to be IP addresses because of a limitation in rpcbind. Note that if you have NIS set up, just add these to the same line.

#### Package installation and configuration

Install the necessary packages:

```bash
sudo apt install rpcbind nfs-kernel-server
```

Edit `/etc/exports` and add the shares:

```
/home @myclients(rw,sync,no_subtree_check)
/usr/local @myclients(rw,sync,no_subtree_check)
```

The above shares `/home` and `/usr/local` to all clients in the `myclients` netgroup.

```
/home 192.168.0.10(rw,sync,no_subtree_check) 192.168.0.11(rw,sync,no_subtree_check)
/usr/local 192.168.0.10(rw,sync,no_subtree_check) 192.168.0.11(rw,sync,no_subtree_check)
```

Where the above shares `/home` and `/usr/local` are on two clients with static IP addresses. If you wanted instead allow to all clients in the private network falling within the designated ip address range, consider the following:

```
/home 192.168.0.0/255.255.255.0(rw,sync,no_subtree_check)
/usr/local 192.168.0.0/255.255.255.0(rw,sync,no_subtree_check)
```

Where `rw` makes the share read/write, and `sync` requires the server to only reply to requests once any changes have been flushed to disk. This is the safest option; async is faster, but dangerous. It is strongly recommended that you read man exports if you are considering other options.

After setting up `/etc/exports`, export the shares:

```bash
sudo exportfs -ra
```

You'll want to do this command whenever `/etc/exports` is modified.

#### Restart Services

By default, rpcbind only binds to the loopback interface. To enable access to rpcbind from remote machines, you need to change `/etc/conf.d/rpcbind` to get rid of either `-l` or `-i 127.0.0.1`.

If any changes were made, rpcbind and NFS will need to be restarted:

```bash
sudo systemctl restart rpcbind
sudo systemctl restart nfs-kernel-server
```

#### Security items to consider

Aside from the UID issues discussed above, it should be noted that an attacker could potentially masquerade as a machine that is allowed to map the share, which allows them to create arbitrary UIDs to access your files. One potential solution to this is IPSec, see also the NFS and IPSec section below. You can set up all your domain members to talk only to each other over IPSec, which will effectively authenticate that your client is who it says it is.

IPSec works by encrypting traffic to the server with the server's key, and the server sends back all replies encrypted with the client's key. The traffic is decrypted with the respective keys. If the client doesn't have the keys that the client is supposed to have, it can't send or receive data.

An alternative to IPSec is physically separate networks. This requires a separate network switch and separate ethernet cards, and physical security of that network.

### Troubleshooting

Mounting an NFS share inside an encrypted home directory will only work after you are successfully logged in and your home is decrypted. This means that using /etc/fstab to mount NFS shares on boot will not work - because your home has not been decrypted at the time of mounting. There is a simple way around this using Symbolic links:

1. Create an alternative directory to mount the NFS shares in:

```bash
sudo mkdir /nfs
sudo mkdir /nfs/music
```

1. Edit /etc/fstab to mount the NFS share into that directory instead:

```
nfsServer:music    /nfs/music    nfs    auto    0 0
```

Create a symbolic link inside your home, pointing to the actual mount location. For example, in our case delete the 'Music' directory already existing there first:

```bash
rmdir /home/user/Music
ln -s /nfs/music/ /home/user/Music
```

### Author Information

This guide is based on a documents located on the official Ubuntu wiki:

1. https://help.ubuntu.com/community/SettingUpNFSHowTo
1. https://help.ubuntu.com/stable/serverguide/network-file-system.html
