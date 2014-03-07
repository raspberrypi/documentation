#Setting up the Camera hardware


**Warning**. Cameras are static sensitive. Earth yourself prior to handling the PCB, a sink tap/faucet or similar should suffice if you don’t have an earthing strap.

The camera board attaches to the Raspberry Pi via a 15 way ribbon cable. There are only two connections to make, the ribbon cable need to be attached to the camera PCB and the Raspberry Pi itself. You need to get it the right way round or the camera will not work. On the camera PCB, the blue backing on the cable should be away from the PCB, and on the Raspberry Pi it should be towards the Ethernet connection (or where the Ethernet connector would be if you are using a model A).

Although the connectors on the PCB and the Pi are different, they work in a similar way. On the Raspberry Pi, pull up the tabs on each end of the connector. It should slide up easily, and be able to pivot around slightly. Fully insert the ribbon cable into the slot, ensuring it is straight, then gently press down the tabs to clip it into place. The camera PCB itself also requires you to pull the tabs away from the board, gently insert the cable, then push the tabs back. The PCB connector is a little more awkward than the one on the Pi itself. 

#Setting up the Camera software

Execute the following instructions on the command line to download and install the latest kernel,  GPU firmware and applications. You will need a internet connection for this to work correctly.
```
sudo apt-get update
sudo apt-get upgrade
```
Now you need to enable camera support using the raspi-config program you will have used when you first set up your Raspberry Pi.
```
sudo raspi-config
```
Use the cursor keys to move to the camera option and select enable. On exiting raspi-config it will ask to reboot. The enable option will ensure that on reboot the correct GPU firmware will be running (with the camera driver and tuning), and the GPU memory split is sufficient to allow the camera to acquire enough memory to run correctly. 

To test that the system is installed and working, try the following command : 
```
raspistill -v -o test.jpg
```
The display should show a 5 second preview from the camera and then take a picture, saved to the file test.jpg, whilst display various informational messages.

#Troubleshooting

If the camera is not working correctly, there are number of things to try. 
Are the ribbon connectors all firmly seated and the right way round? They must be straight in their sockets.
Is the camera module connector firmly attached to the camera PCB? This is the connection from the smaller black camera module itself to the camera PCB. Sometimes this connection can come loose. Using a fingernail, flip up the connector on the PCB, then reseat it with gentle pressure, it engages with a very slight click.
Have sudo apt-get update, sudo apt-get upgrade been run?
Has raspi-config been run and the camera enabled?
Is your power supply sufficient? The camera adds about 200-250mA to the power requirements of the Raspberry Pi.

So, if things are still not working, try the following:

Error : raspistill/raspivid not found. This probably means your update/upgrade failed in some way. Try it again.

Error : ENOMEM displayed. Camera is not starting up. Check all connections again. 

Error : ENOSPC displayed. Camera is probably running out of GPU memory. Check config.txt in the /boot/ folder. The gpu_mem option should be at least 128.

If after all the above, the camera is still not working, it may be defective. Try posting on the Raspberry Pi forum (Camera section) to see if there is any more help available there.
