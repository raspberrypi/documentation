## Getting started with the Raspberry Pi TV HAT

The TV HAT has an on-board DVB-T2 tuner that allows you to receive and decode digital television streams on your Raspberry Pi. Then you can watch these streams on the Pi or on any computer connected to the same network as the Pi.

The software we recommend to decode the streams (known as multiplexes, or muxes for short) and view content is called TVHeadend, and instructions for setting it up are below. The TV HAT can decode one mux at a time, and each mux can contain several channels to choose from. Content can either be viewed on the Raspberry Pi to which the TV-HAT is connected, or sent to another device on the same network.

**You will need:**
* A TV aerial
* A Raspberry Pi TV HAT with its stand-offs, screws, and aerial adaptor
* A Raspberry Pi that is connected to the internet (plus a mouse, keyboard, and display, if
you are not accessing the Pi remotely)
* Optional: another computer connected to the same network

### Setup instructions

**On your Raspberry Pi:**

* Connect the aerial adaptor to the TV HAT:
  * With the adaptor pointing away from the USB ports, press the HAT gently down over the Raspberry Pi’s GPIO pins
  * Place the spacers at two or three of the corners of the HAT, and tighten the screws through the mounting
holes to hold them in place.
* Connect the TV HAT’s aerial adaptor to the cable from your TV aerial.
* Set up the Raspberry Pi with the newest version of the Raspberry Pi OS operating system, which you can download from our [downloads page](https://www.raspberrypi.org/downloads/raspbian/).
 * If you don’t know how to do this, follow our guide [here](https://projects.raspberrypi.org/en/pathways/getting-started-with-raspberry-pi)
* Start up your Pi, open a terminal window, and run the following two commands to install the `tvheadend` software:
```
sudo apt update
sudo apt install tvheadend
```
  * If you don’t know how to do this, follow our guide [here](https://projects.raspberrypi.org/en/projects/raspberry-pi-using/9)
* During the `tvheadend` installation, you will be asked to choose an administrator account name and password. You’ll need these later, so make sure to pick something you can remember.

**In a web browser on a different computer:**

* Type the following into the address bar: `http://raspberrypi.local:9981/extjs.html`
* This should connect to `tvheadend` running on the Raspberry Pi.
  * If the address above doesn't work, you’ll need to find out the IP address of the Pi. Open a terminal window on your Pi, and run the command `hostname -I`
  * You’ll see the IP address in one or two formats: a string of four numbers separated by dots, then, if you are on a IPv6 network, a space, then a long string of numbers and letters separated by colons.
  * Note down everything before the space (the four numbers and dots), and type this into the address bar instead of the raspberrypi.local part of the address.
* Once you have connected to `tvheadend` via the browser, you will be prompted to sign in. Use the account name and password you chose when you installed `tvheadend` on the Pi. A setup wizard should appear.
* First, set the language you want `tvheadend` to use (**English (GB)** worked for us; we have not yet tested other languages).
* Next, set up network, user, and administrator access. If you don’t have specific preferences, leave **Allowed network** blank, and enter an asterisk (*) in the **username** and **password** fields. This will let anyone connected to your local network access `tvheadend`.
* You should see a window titled **Network settings**. Under **Network 2**, you should see `Tuner: Sony CDX2880 #0 : DVB-T #0`. For **Network type**, choose `DVB-T Network`.
* The next window is **Assign predefined muxes to networks**; here, you select the TV stream to receive and decode. Under Network 1, for predefined muxes, select your local TV transmitter.
  * Your local transmitter can be found using the [Freeview website](https://www.freeview.co.uk/help). Enter your postcode to see which transmitter should give you a good signal.
* When you click **Save & Next**, the software will start scanning for the selected mux, and will show a progress bar. After about two minutes, you should see something like:
```
Found muxes: 8
Found services: 172
```
* In the next window, titled **Service mapping**, tick all three boxes: **Map all services**, **Create provider tags**, and **Create network tags**.
* Next you should see a list of TV channels you can watch, along with the programmes they’re currently showing.
* To watch a TV channel in the browser, click the little TV icon to the left of the channel
listing, just to the right of the **i** icon. This brings up an in-browser media player. Depending on the decoding facilities  built into your browser and the type of stream being played, you may find that playback can be jerky. In these cases, we recommend using a local media player as the playback application.
* To watch a TV channel in a local media player, e.g. VLC [www.videolan.org/vlc](https://www.videolan.org/vlc), you’ll need to download it as a stream. Click the `i` icon to the left of a channel listing to bring up the information panel for that channel. Here you can see a stream file that you can download.

`tvheadend` is supported by numerous apps, such as TvhClient for iOS, which will play TV from the Pi. OMXPlayer, supplied with Raspberry Pi OS, also supports viewing TV streams from `tvheadend`. Kodi, available in the Raspberry Pi OS repos, provides excellent facilities for playing live TV, along with previously recorded channels and timed series recording.

To discuss other features or uses of the TV HAT, please visit our [forums](https://www.raspberrypi.org/forums).
