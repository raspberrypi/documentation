# Network File System (NFS)

A **Network File System** (NFS) allows you to share a directory located on one networked computer with other computers or devices on the same network. The computer where the directory is located is called the **server**, and computers or devices connecting to that server are called **clients**. Clients usually `mount` the shared directory to make it a part of their own directory structure. The shared directory is an example of a shared resource or network share.

For smaller networks, an NFS is perfect for creating a simple NAS (Network-attached storage) in a Linux/Unix environment.

An NFS is perhaps best suited to more permanent network-mounted directories, such as `/home` directories or regularly-accessed shared resources. If you want a network share that guest users can easily connect to, Samba is better suited to the task. This is because tools to temporarily mount and detach from Samba shares are more readily available across old and proprietary operating systems.

Before deploying an NFS, you should be familiar with:

* Linux file and directory permissions
* mounting and unmounting filesystems

## Set up a basic NFS server

Install the packages required using the command below:

```bash
sudo apt install nfs-kernel-server
```

For easier maintenance, we will isolate all NFS exports in single directory, into which the real directories will be mounted with the `--bind` option.

Suppose we want to export our users' home directories, which are in `/home/users`. First we create the export filesystem:

```bash
sudo mkdir -p /export/users
```

Note that `/export` and `/export/users` will need 777 permissions, as we will be accessing the NFS share from the client without LDAP/NIS authentication. This will not apply if using authentication (see below). Now mount the real `users` directory with:

```bash
sudo mount --bind /home/users /export/users
```

To save us from retyping this after every reboot, we add the following line to `/etc/fstab`:

```
/home/users    /export/users   none    bind  0  0
```

There are three configuration files that relate to an NFS server:

1. `/etc/default/nfs-kernel-server`
1. `/etc/default/nfs-common`
1. `/etc/exports`

The only important option in `/etc/default/nfs-kernel-server` for now is `NEED_SVCGSSD`. It is set to `"no"` by default, which is fine, because we are not activating NFSv4 security this time.

In order for the ID names to be automatically mapped, the file `/etc/idmapd.conf` must exist on both the client and the server with the same contents and with the correct domain names. Furthermore, this file should have the following lines in the `Mapping` section:

```
[Mapping]

Nobody-User = nobody
Nobody-Group = nogroup
```

However, note that the client may have different requirements for the Nobody-User and Nobody-Group. For example, on RedHat variants, it is `nfsnobody` for both. If you're not sure, check via the following commands to see if `nobody` and `nogroup` are there:

```bash
cat /etc/passwd
cat /etc/group
```

This way, server and client do not need the users to share same UID/GUID. For those who use LDAP-based authentication, add the following lines to the `idmapd.conf` of your clients:

```
[Translation]

Method = nsswitch
```

This will cause `idmapd` to know to look at `nsswitch.conf` to determine where it should look for credential information. If you have LDAP authentication already working, `nsswitch` shouldn't require further explanation.

To export our directories to a local network `192.168.1.0/24`, we add the following two lines to `/etc/exports`:

```
/export       192.168.1.0/24(rw,fsid=0,insecure,no_subtree_check,async)
/export/users 192.168.1.0/24(rw,nohide,insecure,no_subtree_check,async)
```

### Portmap lockdown (optional)
The files on your NFS are open to anyone on the network. As a security measure, you can restrict access to specified clients.

Add the following line to `/etc/hosts.deny`:

```
rpcbind mountd nfsd statd lockd rquotad : ALL
```

By blocking all clients first, only clients in `/etc/hosts.allow` (added below) will be allowed to access the server. 

Now add the following line to `/etc/hosts.allow`:

```
rpcbind mountd nfsd statd lockd rquotad : <list of IPv4s>
```

where `<list of IPv4s>` is a list of the IP addresses of the server and all clients. (These have to be IP addresses because of a limitation in `rpcbind`, which doesn't like hostnames.) Note that if you have NIS set up, you can just add these to the same line.

Please ensure that the list of authorised IP addresses includes the `localhost` address (`127.0.0.1`), as the startup scripts in recent versions of Ubuntu use the `rpcinfo` command to discover NFSv3 support, and this will be disabled if `localhost` is unable to connect.

Finally, to make your changes take effect, restart the service:

```bash
sudo systemctl restart nfs-kernel-server
```

## Set up an NFSv4 client

Now that your server is running, you need to set up any clients to be able to access it. To start, install the required packages:

```bash
sudo apt install nfs-common
```

On the client, we can mount the complete export tree with one command:

```bash
mount -t nfs -o proto=tcp,port=2049 <nfs-server-IP>:/ /mnt
```

You can also specify the NFS server hostname instead of its IP address, but in this case you need to ensure that the hostname can be resolved to an IP on the client side. A robust way of ensuring that this will always resolve is to use the `/etc/hosts` file.

Note that `<nfs-server-IP>:/export` is not necessary in NFSv4, as it was in NFSv3. The root export `:/` defaults to export with `fsid=0`.

We can also mount an exported subtree with:

```bash
mount -t nfs -o proto=tcp,port=2049 <nfs-server-IP>:/users /home/users
```

To ensure this is mounted on every reboot, add the following line to `/etc/fstab`:

```
<nfs-server-IP>:/   /mnt   nfs    auto  0  0
```

If, after mounting, the entry in `/proc/mounts appears` as `<nfs-server-IP>://` (with two slashes), then you might need to specify two slashes in `/etc/fstab`, or else `umount` might complain that it cannot find the mount.

### Portmap lockdown (optional)

Add the following line to `/etc/hosts.deny`:

```
rpcbind : ALL
```

By blocking all clients first, only clients in `/etc/hosts.allow` (added below) will be allowed to access the server.

Now add the following line to `/etc/hosts.allow`:

```
rpcbind : <NFS server IP address>
```

where `<NFS server IP address>` is the IP address of the server.

## NFS server with complex user permissions

NFS user permissions are based on user ID (UID). UIDs of any users on the client must match those on the server in order for the users to have access. The typical ways of doing this are:

* Manual password file synchronisation
* Use of LDAP
* Use of DNS
* Use of NIS

Note that you have to be careful on systems where the main user has root access: that user can change UIDs on the system to allow themselves access to anyone's files. This page assumes that the administrative team is the only group with root access and that they are all trusted. Anything else represents a more advanced configuration, and will not be addressed here.

### Group permissions

A user's file access is determined by their membership of groups on the client, not on the server. However, there is an important limitation: a maximum of 16 groups are passed from the client to the server, and if a user is member of more than 16 groups on the client, some files or directories might be unexpectedly inaccessible.

### DNS (optional, only if using DNS)

Add any client name and IP addresses to `/etc/hosts`. (The IP address of the server should already be there.) This ensures that NFS will still work even if DNS goes down. Alternatively you can rely on DNS if you want - it's up to you.

### NIS (optional, only if using NIS)

This applies to clients using NIS. Otherwise you can't use netgroups, and should specify individual IPs or hostnames in `/etc/exports`. Read the BUGS section in `man netgroup` for more information.

First, edit `/etc/netgroup` and add a line to classify your clients (this step is not necessary, but is for convenience):

```
myclients (client1,,) (client2,,) ...
```

where `myclients` is the netgroup name.

Next run this command to rebuild the NIS database:

```bash
sudo make -C /var/yp
```

The filename `yp` refers to Yellow Pages, the former name of NIS.

### Portmap lockdown (optional)

Add the following line to `/etc/hosts.deny`:

```
rpcbind mountd nfsd statd lockd rquotad : ALL
```

By blocking all clients first, only clients in `/etc/hosts.allow` (added below) will be allowed to access the server.

Consider adding the following line to `/etc/hosts.allow`:

```
rpcbind mountd nfsd statd lockd rquotad : <list of IPs>
```

where `<list of IPs>` is a list of the IP addresses of the server and all clients. These have to be IP addresses because of a limitation in `rpcbind`. Note that if you have NIS set up, you can just add these to the same line.

### Package installation and configuration

Install the necessary packages:

```bash
sudo apt install rpcbind nfs-kernel-server
```

Edit `/etc/exports` and add the shares:

```
/home @myclients(rw,sync,no_subtree_check)
/usr/local @myclients(rw,sync,no_subtree_check)
```

The example above shares `/home` and `/usr/local` to all clients in the `myclients` netgroup.

```
/home 192.168.0.10(rw,sync,no_subtree_check) 192.168.0.11(rw,sync,no_subtree_check)
/usr/local 192.168.0.10(rw,sync,no_subtree_check) 192.168.0.11(rw,sync,no_subtree_check)
```

The example above shares `/home` and `/usr/local` to two clients with static IP addresses. If you want instead to allow access to all clients in the private network falling within a designated IP address range, consider the following:

```
/home 192.168.0.0/255.255.255.0(rw,sync,no_subtree_check)
/usr/local 192.168.0.0/255.255.255.0(rw,sync,no_subtree_check)
```

Here, `rw` makes the share read/write, and `sync` requires the server to only reply to requests once any changes have been flushed to disk. This is the safest option; `async` is faster, but dangerous. It is strongly recommended that you read `man exports` if you are considering other options.

After setting up `/etc/exports`, export the shares:

```bash
sudo exportfs -ra
```

You'll want to run this command whenever `/etc/exports` is modified.

### Restart services

By default, `rpcbind` only binds to the loopback interface. To enable access to `rpcbind` from remote machines, you need to change `/etc/conf.d/rpcbind` to get rid of either `-l` or `-i 127.0.0.1`.

If any changes are made, rpcbind and NFS will need to be restarted:

```bash
sudo systemctl restart rpcbind
sudo systemctl restart nfs-kernel-server
```

### Security items to consider

Aside from the UID issues discussed above, it should be noted that an attacker could potentially masquerade as a machine that is allowed to map the share, which allows them to create arbitrary UIDs to access your files. One potential solution to this is IPSec. You can set up all your domain members to talk to each other only over IPSec, which will effectively authenticate that your client is who it says it is.

IPSec works by encrypting traffic to the server with the server's public key, and the server sends back all replies encrypted with the client's public key. The traffic is decrypted with the respective private keys. If the client doesn't have the keys that it is supposed to have, it can't send or receive data.

An alternative to IPSec is physically separate networks. This requires a separate network switch and separate Ethernet cards, and physical security of that network.

## Troubleshooting

Mounting an NFS share inside an encrypted home directory will only work after you are successfully logged in and your home is decrypted. This means that using /etc/fstab to mount NFS shares on boot will not work, because your home has not been decrypted at the time of mounting. There is a simple way around this using symbolic links:

1. Create an alternative directory to mount the NFS shares in:

```bash
sudo mkdir /nfs
sudo mkdir /nfs/music
```

2. Edit `/etc/fstab` to mount the NFS share into that directory instead:

```
nfsServer:music    /nfs/music    nfs    auto    0 0
```

3. Create a symbolic link inside your home, pointing to the actual mount location. For example, and in this case deleting the `Music` directory already existing there first:

```bash
rmdir /home/user/Music
ln -s /nfs/music/ /home/user/Music
```

## Author information

This guide is based on documents on the official Ubuntu wiki:

1. https://help.ubuntu.com/community/SettingUpNFSHowTo
1. https://help.ubuntu.com/stable/serverguide/network-file-system.html
