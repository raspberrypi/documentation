# systemd

Raspberry Pi OS uses [`systemd`](https://www.freedesktop.org/wiki/Software/systemd/) to manage the running of services, including controlling what starts when Linux boots.

## `rc.local` and service dependencies
Unlike on older versions of Linux, `systemd` starts services based on their dependencies: services are no longer started in a predefined order. This means it is no longer guaranteed that `rc.local` will run after all other services have started. You should therefore not use `rc.local` to start programs at boot: instead, create a `systemd` service, specifying which other services it depends on.

## Service definitions
`Systemd` defines each service in a separate file. Under `systemd` services are a type of 'unit': units are system resources under the control of `systemd`. The basic format of a service definition is as follows:

```
[Unit]
Description=...
...

[Service]
...

[Install]
...
```

User services should be placed in `/etc/systemd/user`: the filename dictates the service name. For example, a file named `monitoring.service` would define a service named `monitoring`.

### Example - one-time service
One-time services are used when you wish to run a program which does some work, then exits: this is in contrast to a service which stays running all the time. Consider the following service definition:

```
[Unit]
Description=Run my program once at boot time
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
ExecStart=/home/pi/myprogram.sh

[Install]
WantedBy=multi-user.target graphical.target
```

Let's say the above file is `/etc/systemd/user/myprogram.service`: this defines a new one-shot service named `myprogram`. The `myprogram` service will wait until `network-online.target` has been reached, then run `/home/pi/myprogram.sh`.

### Example - simple service
A simple service runs continuously for as long as its dependencies are met. We define `/etc/systemd/user/netmusicplayer.service` as follows:

```
[Unit]
Description=Network music player
Wants=network-online.target
After=network-online.target
Requires=mpd.target

[Service]
Type=simple
ExecStart=/home/pi/nmp.sh
ExecStop=/home/pi/nmp.sh stop

[Install]
WantedBy=multi-user.target graphical.target
```

Our `netmusicplayer` service is started up using the script `/home/pi/nmp.sh`. The service also passes the `stop` parameter to that same script to stop the network music player. Because the network music player uses [`mpd`](https://www.musicpd.org/), we use the `Requires=` directive to specify that `mpd` must be running before `netmusicplayer` starts up.

## Enable and disable a service
To enable a service, use the `systemctl enable` command as follows:

```
sudo systemctl enable <service file>
```

For example:

```
sudo systemctl enable /etc/systemd/user/netmusicplayer.service
```

Once a service has been enabled, it will run the next time the system boots. To run the service immediately, start it using `systemctl start` - see the following section.

To disable a service, use the `systemctl disable` command:

```
sudo systemctl disable <service name>
```

For example:

```
sudo systemctl disable netmusicplayer
```

## Start and stop a service
To start a service, use the `systemctl start` command:

```
sudo systemctl start <name of service>
```

For example:

```
sudo systemctl start netmusicplayer
```

To stop a service, use the `systemctl stop` command:

```
sudo systemctl stop <name of service>
```

For example:

```
sudo systemctl stop netmusicplayer
```
