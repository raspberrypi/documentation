# Camera Module

The Raspberry Pi camera module is capable of taking full HD 1080p photo and video and can be controlled programmatically.

## Connecting the camera

The flex cable inserts into the connector situated between the Ethernet and HDMI ports, with the silver connectors facing the HDMI port. The flex cable connector should be opened by pulling the tabs on the top of the connector upwards then towards the Ethernet port. The flex cable should be inserted firmly into the connector, with care taken not to bend the flex at too acute an angle. The top part of the connector should then be pushed towards the HDMI connector and down, while the flex cable is held in place.

Watch the following video to see a demonstration of the camera being connected:

[![Camera connection screenshot](https://img.youtube.com/vi/GImeVqHQzsE/0.jpg)](http://www.youtube.com/watch?v=GImeVqHQzsE)

The camera may come with a small piece of translucent blue plastic film covering the lens. This is only present to protect the lens while it is being mailed to you, and needs to be removed by gently peeling it off.

## Enabling the camera

Open the `raspi-config` tool from the Terminal:

```bash
sudo raspi-config
```

Select `Enable camera` and hit `Enter`, then go to `Finish` and you'll be prompted to reboot.

## Using the camera

Libraries for using the camera are available in:

- [Shell](raspicam/README.md) (Linux command line)
- [Python](python/README.md)

See detailed [technical specs](../../hardware/camera/README.md) of the camera hardware and software.
