# Installing a Raspberry Pi camera

## Connecting the camera

The flex cable inserts into the connector labelled CAMERA on the Raspberry Pi, which is located between the Ethernet and HDMI ports. The cable must be inserted with the silver contacts facing the HDMI port. To open the connector, pull the tabs on the top of the connector upwards, then towards the Ethernet port. The flex cable should be inserted firmly into the connector, with care taken not to bend the flex at too acute an angle. To close the connector, push the top part of the connector towards the HDMI port and down, while holding the flex cable in place.

We have created a video to illustrate the process of connecting the camera. Although the video shows the original camera on the original Raspberry Pi 1, the principle is the same for all camera boards:

[![Camera connection screenshot](https://img.youtube.com/vi/GImeVqHQzsE/0.jpg)](http://www.youtube.com/watch?v=GImeVqHQzsE)

Depending on the model, the camera may come with a small piece of translucent blue plastic film covering the lens. This is only present to protect the lens while it is being mailed to you, and needs to be removed by gently peeling it off.

## Enabling the camera

### Using the desktop

Select `Preferences` and `Raspberry Pi Configuration` from the desktop menu: a window will appear. Select the `Interfaces` tab, then click on the `enable camera` option. Click `OK`. You will need to reboot for the changes to take effect.

### Using the command line

Open the `raspi-config` tool from the terminal:

```bash
sudo raspi-config
```

Select `Interfacing Options` then `Camera` and press `Enter`. Choose `Yes` then `Ok`. Go to `Finish` and you'll be prompted to reboot.
