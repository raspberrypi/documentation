# Access your Raspberry Pi over the internet

You can connect to your Raspberry Pi over the internet from another computer or a mobile device. There are a number of ways to do this, which we cover below.

## Port forwarding

One method is to set up port forwarding on your router. To do this, you must change the configuration of your router to forward all inbound traffic from the internet on a specific port to the local IP address of your Raspberry Pi. Most routers have this feature available. However, every router is different so you will need to consult your router's user manual for instructions. The settings can be tricky if your Pi is behind a firewall or if there is more than one router. One disadvantage of port forwarding is that it exposes a network port on your private LAN to the public internet. This is a known security vulnerability and must be managed carefully.

## Alternatives

Alternative online services are available.

### remot3.it

One secure alternative to port forwarding is [remot3.it](https://www.remot3.it), by Weaved, Inc. remot3.it ("remote it") is software you install on your Raspberry Pi to access a single Pi, or manage a large number of Pis, from anywhere over the internet. Use remot3.it to access any TCP port on your Pi over the web including SSH, VNC, HTTP(S), RDP, and custom TCP services.

From the command line on your Pi, update your Raspbian package lists:

```bash
sudo apt-get update
```

Install the remot3.it package:

```bash
sudo apt-get install weavedconnectd
```

Next, run the remot3.it installer with this command:

```bash
sudo weavedinstaller
```

The remot3.it installer will first ask you to create a user account by entering an email address and a password. Follow the on-screen menus to give your Pi a device name and choose what TCP ports/services to enable.

Now access your Pi over the internet by signing in to www.remot3.it.

For more detailed instructions and examples, see [Getting Started with remot3.it for Pi](http://forum.weaved.com/t/how-to-get-started-with-remot3-it-for-pi/1029).

### Dataplicity

[Dataplicity](https://dataplicity.com) allows you to connect and control your Pi's shell remotely from a web browser and its mobile apps. You can use Dataplicity's Wormhole feature to host a website or API directly from your Pi, and automatically enable HTTPS/SSL with no configuration or certificates.

It uses WebSockets over HTTPS to provide a connection, and requires a single-line install.

Dataplicity provides free support by e-mail and in-app messenger.

For more information, consult the [documentation](https://docs.dataplicity.com/).

### Losant

Losant is an easy-to-use developer platform designed to help you quickly and securely build connected applications. Losant provides powerful data collection, aggregation, and visualization.

With [Losant](https://losant.com), you can easily control and listen to the Raspberry Pi's GPIO. Losant's drag-and-drop workflow editor allows you to trigger actions, notifications, and machine-to-machine communication without programming.

For detailed instructions, check out this [guide](https://www.losant.com/blog/how-to-access-your-raspberry-pis-gpio-over-the-internet).

Losant uses open communication standards like REST and MQTT to provide connectivity to devices.
