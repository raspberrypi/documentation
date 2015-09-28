#Camera Troubleshooting

If the camera is not working correctly, there are number of things to try:

*   Is the ribbon cable attached to the Camera Serial Interface (CSI), not the Display Serial Interface (DSI)?  The ribbon connector will fit into either port.  The Camera port is located near the HDMI connector.

*   Are the ribbon connectors all firmly seated, and are they the right way round? They must be straight in their sockets.

*   Is the camera module connector, between the smaller black camera module itself and the camera PCB, firmly attached? Sometimes this connection can come loose during transit or when putting the camera module in a case. Using a fingernail, flip up the connector on the PCB, then reseat it with gentle pressure. It engages with a very slight click. Don't force it; if it doesn't engage, it's probably slightly misaligned. 

*   Have `sudo apt-get update`, `sudo apt-get upgrade` been run?

*   Has `raspi-config` been run and the camera enabled?

*   Is your power supply sufficient? The camera adds about 200-250mA to the power requirements of your Raspberry Pi.

If things are still not working, try the following:

*   Error : raspistill/raspivid not found. This probably means your update/upgrade failed in some way. Try it again.

*   Error : ENOMEM displayed. Camera is not starting up. Check all connections again. 

*   Error : ENOSPC displayed. Camera is probably running out of GPU memory. Check `config.txt` in the /boot/ folder. The gpu_mem option should be at least 128. Alternatively, use the Memory Split option in the Advanced section of `raspi-config` to set this.

*   If after all the above the camera is still not working, you may need to upgrade the firmware on the Raspberry Pi. Use the following command to get the very latest (but experimental) firmware.

```
sudo rpi-update
```
*   If after trying all the above the camera still does not work, it may be defective; have you been careful not to expose it to static shock? Try posting on the [Raspberry Pi forum (Camera section)](http://www.raspberrypi.org/forum/viewforum.php?f=43) to see if there is any more help available there. Failing that, it may need replacing. 
