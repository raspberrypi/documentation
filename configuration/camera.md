# Camera configuration

## Setting up the camera hardware

**Warning**: Cameras are sensitive to static. Earth yourself prior to handling the PCB. A sink tap or similar should suffice if you don’t have an earthing strap.

The camera board attaches to the Raspberry Pi via a 15-way ribbon cable. There are only two connections to make: the ribbon cable needs to be attached to the camera PCB, and to the Raspberry Pi itself. You need to get the cable the right way round, or the camera will not work. On the camera PCB, the blue backing on the cable should face away from the PCB, and on the Raspberry Pi it should face towards the Ethernet connection (or where the Ethernet connector would be if you're using a model A).

Although the connectors on the PCB and the Pi are different, they work in a similar way. On the Raspberry Pi itself, pull up the tabs on each end of the connector. It should slide up easily, and be able to pivot around slightly. Fully insert the ribbon cable into the slot, ensuring it is set straight, then gently press down the tabs to clip it into place. The camera PCB connector also requires you to pull the tabs away from the board, gently insert the cable, then push the tabs back. The PCB connector can be a little more awkward than the one on the Pi itself.

## Setting up the camera software

Execute the following instructions on the command line to download and install the latest kernel, GPU firmware, and applications. You'll need an internet connection for this to work correctly.

```bash
sudo apt update
sudo apt full-upgrade
```

Now you need to enable camera support using the `raspi-config` program you will have used when you first set up your Raspberry Pi.

```bash
sudo raspi-config
```

Use the cursor keys to select and open *Interfacing Options*, and then select *Camera* and follow the prompt to enable the camera. 

Upon exiting `raspi-config`, it will ask to reboot. The enable option will ensure that on reboot the correct GPU firmware will be running with the camera driver and tuning, and the GPU memory split is sufficient to allow the camera to acquire enough memory to run correctly.

To test that the system is installed and working, try the following command:

```bash
raspistill -v -o test.jpg
```

The display should show a five-second preview from the camera and then take a picture, saved to the file `test.jpg`, whilst displaying various informational messages.

## More Information

See [Camera Software](../raspbian/applications/camera.md).
