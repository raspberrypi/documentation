# _libcamera_ and _libcamera-apps_ installation for Raspberry Pi

## Preparing your Pi

Your Raspberry Pi should be running the latest version of the Raspberry Pi OS (_Buster_ at the time of writing), and the camera and I2C interfaces must both be enabled (check the _Interfaces_ tab of the _Raspberry Pi Configuration_ tool, from the _Preferences_ menu). First ensure your system, firmware and all its applications and repositories are up to date by entering the following commands into a terminal window.

```bash
sudo apt update
sudo apt full-upgrade
```

libcamera is under active development which sometimes means that new features need to be supported in Raspberry Pi OS, even before they are officially released. Therefore we currently recommend updating to the latest release candidate. To do this, first reboot your Pi, and then use

```bash
sudo rpi-update
```

**WARNING**: Note that the release candidate is not as thoroughly tested as an official release. If your Raspberry Pi contains important or critical data we would strongly advise that it is backed up first, or that a fresh SD card is used for the purpose of trying _libcamera_.

Next, the `/boot/config.txt` file must be updated to load and use the camera driver, by adding the following to the bottom.

```bash
dtoverlay=imx219
```

If you are using a sensor other than the `imx219` you will need to supply the alternative name here (for example, `ov5647` for the V1 camera, or `imx477` for the HQ Cam).

**NOTE**: after rebooting, control of the camera system will be passed to the ARM cores, and firmware-based camera functions (such as raspistill and so forth) will no longer work. Setting `/boot/config.txt` back and rebooting will restore the previous behaviour.

## Building _libcamera_ and _qcam_

The build system and runtime environment of _libcamera_ have a number of dependencies. They can be installed with the following commands.

```bash
sudo apt install libboost-dev
sudo apt install libgnutls28-dev openssl libtiff5-dev
sudo apt install qtbase5-dev libqt5core5a libqt5gui5 libqt5widgets5
sudo apt install meson
sudo pip3 install pyyaml ply
```

The Qt libraries are only required for _libcamera_'s _qcam_ demo app.

Unfortunately, at the time of writing, the default version of meson is a little old, so please execute:

```bash
sudo pip3 install --upgrade meson
 ```

We can now check out the code and build _libcamera_ as follows.

```bash
git clone git://linuxtv.org/libcamera.git
cd libcamera
meson build
cd build
meson configure -Dpipelines=raspberrypi -Dtest=false
cd ..
ninja -C build
sudo ninja -C build install
```

At this stage you may wish to check that _qcam_ works. Type `build/src/qcam/qcam` and check that you see a camera image.

*Note*

On some lower memory platforms (e.g. 1GB) there have been cases of ninja exhausting all the system memory and aborting (as it will attempt to use all the CPU cores). If this happens, please try replacing `ninja -C build` by `ninja -C build -j 2` - this will restrict Ninja to only 2 cores.

## Raspberry Pi's _libcamera-apps_

Raspberry Pi's _libcamera-apps_ provide very similar functionality to the _raspistill_ and _raspivid_ applications that use the proprietary firmware-based camera stack. To build them, we must first install _libepoxy_.

```bash
cd
sudo apt install libegl1-mesa-dev
git clone https://github.com/anholt/libepoxy.git
cd libepoxy
mkdir _build
cd _build
meson
ninja
sudo ninja install
```

Finally we can build the _libcamera-apps_.

```bash
cd
sudo apt install cmake libboost-program-options-dev libdrm-dev libexif-dev
git clone https://github.com/raspberrypi/libcamera-apps.git
cd libcamera-apps
mkdir build
cd build
cmake ..
make -j4
```

To check everything is working correctly, type `./libcamera-hello` - you should see a preview window displayed for about 5 seconds.

## Further Documentation

You can find out more in the _Raspberry Pi Camera Algorithm and Tuning Guide_, [here](rpi_SOFT_libcamera_1p1.pdf).

More information on the _libcamera-apps_ is available [here](https://github.com/raspberrypi/libcamera-apps/blob/main/README.md).

Information on writing your own kernel modules to support new CSI-2 cameras and bridge chips can be found [here](./csi-2-usage.md).
