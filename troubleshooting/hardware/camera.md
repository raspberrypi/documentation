#Camera Troubleshooting

If the camera is not working correctly, there are number of things to try.

Are the ribbon connectors all firmly seated and the right way round? They must be straight in their sockets.

Is the camera module connector firmly attached to the camera PCB? This is the connection from the smaller black camera module itself to the camera PCB. Sometimes this connection can come looseduring transit or when putting the camera module in a case. Using a fingernail, flip up the connector on the PCB, then reseat it with gentle pressure, it engages with a very slight click. Don't force it - if it doesn't engage, it's probably slightly misaligned. 

Have sudo apt-get update, sudo apt-get upgrade been run?

Has raspi-config been run and the camera enabled?

Is your power supply sufficient? The camera adds about 200-250mA to the power requirements of the Raspberry Pi.

So, if things are still not working, try the following:

Error : raspistill/raspivid not found. This probably means your update/upgrade failed in some way. Try it again.

Error : ENOMEM displayed. Camera is not starting up. Check all connections again. 

Error : ENOSPC displayed. Camera is probably running out of GPU memory. Check config.txt in the /boot/ folder. The gpu_mem option should be at least 128.

If after all the above, the camera is still not working, you may need to upgrade the firmware on the Raspberry Pi. Use the following command to get the very latest (but bleeding edge) firmware.

```
sudo rpi-update
```
If after trying all the above, the camera still does not work it may be defective. Try posting on the Raspberry Pi forum (Camera section) to see if there is any more help available there, dailing that, it may need replacement. 

