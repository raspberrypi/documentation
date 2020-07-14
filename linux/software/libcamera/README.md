# _libcamera_ installation for Raspberry Pi

## Preparing your Pi

Your Raspberry Pi should be running the latest version of the Raspberry Pi OS (_Buster_ at the time of writing), and the camera and I2C interfaces must both be enabled (check the _Interfaces_ tab of the _Raspberry Pi Configuration_ tool, from the _Preferences_ menu). First ensure your system, firmware and all its applications and repositories are up to date by entering the following commands into a terminal window.

```bash
sudo apt update
sudo apt full-upgrade
```

Currently (May 2020) the necessary _libcamera_ support has not yet been merged into the standard Raspberry Pi OS release, therefore it is necessary to install the latest release candidate. To do this, first reboot your Pi, and then use

```bash
sudo rpi-update
```

**WARNING**: Note that the release candidate is not as thoroughly tested as an official release. If your Raspberry Pi contains important or critical data we would strongly advise that it is backed up first, or that a fresh SD card is used for the purpose of trying _libcamera_.

Next, the `/boot/config.txt` file must be updated to load and use the camera driver, by adding the following lines to the bottom. Currently we also need to update the GPU's `core_freq_min` though this will become unnecessary in due course after further updates.

```bash
dtoverlay=imx219
core_freq_min=250
```

If you are using a sensor other than the `imx219` you will need to supply the alternative name here (for example, `ov5647` for the V1 camera, or `imx477` for the HQ Cam for which support will be available shortly).

**NOTE**: after rebooting, control of the camera system will be passed to the ARM cores, and firmware-based camera functions (such as raspistill and so forth) will no longer work. Setting `/boot/config.txt` back and rebooting will restore the previous behaviour.

## Software Dependencies

The build system and runtime environment of _libcamera_ have a number of dependencies. They can be installed with the following commands.

```bash
sudo apt install libboost-dev
sudo apt install libgnutls28-dev openssl libtiff5-dev
sudo apt install meson
sudo apt install qtbase5-dev libqt5core5a libqt5gui5 libqt5widgets5
sudo pip3 install pyyaml
```

## Building _libcamera_ and _qcam_

We can now check out the code and configure the build for the Raspberry Pi as follows.

```bash
git clone git://linuxtv.org/libcamera.git
cd libcamera
```

and to configure the build (still in the same _libcamera_ directory):

```bash
meson build
cd build
meson configure -Dpipelines=raspberrypi -Dtest=false
cd ..
```

Finally we are ready to build the source code.

```bash
sudo ninja -C build install
```

## Capturing an Image

Images can be captured using the _qcam_ application, which can be started from the _libcamera_ directory by entering:

```bash
build/src/qcam/qcam
```

## Further Documentation

You can find out more in the _Raspberry Pi Camera Algorithm and Tuning Guide_, [here](rpi_SOFT_libcamera_1p0.pdf).

Information on writing your own kernel modules to support new CSI-2 cameras and bridge chips can be found [here](./csi-2-usage.md).
