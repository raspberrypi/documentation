# Installing the Raspberry Pi cameras

## Connecting the cameras

The flex cable inserts into the connector situated between the Ethernet and HDMI ports, with the silver connectors facing the HDMI port. The flex cable connector should be opened by pulling the tabs on the top of the connector upwards then towards the Ethernet port. The flex cable should be inserted firmly into the connector, with care taken not to bend the flex at too acute an angle. The top part of the connector should then be pushed towards the HDMI connector and down, while the flex cable is held in place.

Watch the following video to see a demonstration of the camera being connected. This is the original camera on the original Pi 1, but the principle is the same for all camera boards:

[![Camera connection screenshot](https://img.youtube.com/vi/GImeVqHQzsE/0.jpg)](http://www.youtube.com/watch?v=GImeVqHQzsE)

Depending on the model, the camera may come with a small piece of translucent blue plastic film covering the lens. This is only present to protect the lens while it is being mailed to you, and needs to be removed by gently peeling it off.

## Enabling the camera

### Using the desktop

Select `Preferences` and `Raspberry Pi Configuration` from the desktop menu. A window will appear, select the `Interfaces` tab, then clik on the enable camera option. Click `OK`. You will need to reboot for the changes to take effect.

### Using the command line

Open the `raspi-config` tool from the Terminal:

```bash
sudo raspi-config
```

Select `Interfacing Options` then `Camera` and hit `Enter`. Choose `Yes` then `Ok`. Go to `Finish` and you'll be prompted to reboot.
