# raspi-config

`raspi-config` is the Raspberry Pi configuration tool written and maintained by [Alex Bradbury](https://github.com/asb). It targets Raspbian.

<a name="usage"></a>
## Usage

You will be shown `raspi-config` on first booting into Raspbian. To open the configuration tool after this, simply run the following from the command line:

```
sudo raspi-config
```

The `sudo` is required because you will be changing files that you do not own as the `pi` user.

You should see a blue screen with options in a grey box in the centre, like so:

![raspi-config main screen](images/raspi-config.png)

It has the following options available:

```
                        Raspberry Pi Software Configuration Tool (raspi-config)

Setup Options

    1 Expand Filesystem              Ensures that all of the SD card storage is available to the OS
    2 Change User Password           Change password for the default user (pi)
    3 Enable Boot to Desktop/Scratch Choose whether to boot into a desktop environment, Scratch, or the command line
    4 Internationalisation Options   Set up language and regional settings to match your location
    5 Enable Camera                  Enable this Pi to work with the Raspberry Pi camera
    6 Add to Rastrack                Add this Pi to the online Raspberry Pi Map (Rastrack)
    7 Overclock                      Configure overclocking for your Pi
    8 Advanced Options               Configure advanced settings
    9 About `raspi-config`           Information about this configuration tool

                                   <Select>                                  <Finish>
```

<a name="moving-around-the-menu"></a>
### Moving around the menu

Use the up and down arrow keys to move the highlighted selection between the options available. Pressing the right arrow key will jump out of the options menu and take you to the `<Select>` and `<Finish>` buttons. Pressing left will take you back to the options. Alternatively, use the `Tab` key to switch between these.

Note that in long lists of option values (like the list of timezone cities), you can also type a letter to skip to that section of the list. For example, entering `L` will skip you to Lisbon, just two options away from London, to save you scrolling all the way through the alphabet.

<a name="what-raspi-config-does"></a>
### What raspi-config does

Generally speaking, `raspi-config` aims to provide the functionality to make the most common configuration changes. This may result in automated edits to `/boot/config.txt` and various standard Linux configuration files. Some options require a reboot to take effect. If you changed any of those, raspi-config will ask if you wish to reboot now when you select the `<Finish>` button.

<a name="menu-options"></a>
## Menu options

<a name="expand-filesystem"></a>
### Expand filesystem

If you installed Raspbian using NOOBS, you can ignore this section as the file system was expanded automatically during installation. However, if you wrote the image to an SD card yourself, then a portion of the card will be unused; this can be any amount over 3GB. Choosing this option will expand your installation to fill the rest of the SD card, giving you more space to use for files. You will need to reboot the Raspberry Pi to make this available. Note there is no confirmation; selecting the option begins the partition expansion immediately.

<a name="change-user-password"></a>
### Change user password

The default user on Raspbian is `pi` with the password `raspberry`. You can change that here. Read about other [users](../linux/usage/users.md).

<a name="change-boot-to-desktop"></a>
### Enable boot to desktop or Scratch

You can change what happens when your Pi boots. Use this option to change your boot preference to command line, desktop, or straight to Scratch.

<a name="internationalisation-options"></a>
### Internationalisation options

Select `Internationalisation Options` and press `Enter` to be taken to a sub-menu containing the following options:

<a name="change-locale"></a>
#### Change locale

Select a locale, for example `en_GB.UTF-8 UTF-8`.

<a name="change-timezone"></a>
#### Change timezone

Select your local timezone, starting with the region such as `Europe`, then selecting a city, for example `London`. Type a letter to skip down the list to that point in the alphabet.

<a name="change-keyboard-layout"></a>
#### Change keyboard layout

This option opens another menu which allows you to select your keyboard layout. It will take a long time to display while it reads all the keyboard types. Changes usually take effect immediately, but may require a reboot.

<a name="enable-camera"></a>
### Enable camera

In order to use the Raspberry Pi camera module, you must enable it here. Select the option and proceed to `Enable`. This will make sure at least 128MB of RAM is dedicated to the GPU.

<a name="add-to-rastrack"></a>
### Add to Rastrack

Rastrack is a user-contributed Google Map to which Pi users in the community have added their location; it shows a heat map of where Pi users are known to be around the world. This was set up by young Pi enthusiast [Ryan Walmsley](https://ryanteck.uk/) in 2012. Rastrack is located at [rastrack.co.uk](http://rastrack.co.uk/).

You can use this option to add your location to the map.

<a name="overclock"></a>
### Overclock

It is possible to overclock your Raspberry Pi's CPU. The default is 700MHz but it can be set up to 1000MHz. The overclocking you can achieve will vary; overclocking too high may result in instability. Selecting this option shows the following warning:

```
Be aware that overclocking may reduce the lifetime of your Raspberry Pi. If overclocking at a certain level causes system instability, try a more modest overclock. Hold down `shift` during boot to temporarily disable overclock.
```

<a name="advanced-options"></a>
### Advanced options

<a name="overscan"></a>
#### Overscan

Old TV sets had a significant variation in the size of the picture they produced; some had cabinets that overlapped the screen. TV pictures were therefore given a black border so that none of the picture was lost; this is called overscan. Modern TVs and monitors don't need the border, and the signal doesn't allow for it. If the initial text shown on the screen disappears off the edge, you need to enable overscan to bring the border back.

Any changes will take effect after a reboot. You can have greater control over the settings by editing [config.txt](config-txt.md).

On some displays, particularly monitors, disabling overscan will make the picture fill the whole screen and correct the resolution. For other displays, it may be necessary to leave overscan enabled and adjust its values.

<a name="hostname"></a>
#### Hostname

Set the visible name for this Pi on a network.

<a name="memory-split"></a>
#### Memory split

Change the amount of memory made available to the GPU.

<a name="ssh"></a>
#### SSH

Enable/disable remote command line access to your Pi using SSH.

SSH allows you to remotely access the command line of the Raspberry Pi from another computer. Disabling this ensures the SSH service does not start on boot, freeing up processing resources. Read more about using SSH on the [SSH documentation page](../remote-access/ssh/README.md). Note that SSH is enabled by default. If connecting your Pi directly to a public network, you should disable SSH unless you have set up secure passwords for all users.

<a name="device-tree"></a>
#### Device Tree

Enable/Disable the use of Device Tree. Read more about Device Trees config on the [Device Trees documentation page](device-tree.md).

<a name="spi"></a>
#### SPI

Enable/Disable SPI interfaces and automatic loading of the SPI kernel module, needed for products such as PiFace.

<a name="i2c"></a>
#### I2C

Enable/Disable I2C interfaces and automatic loading of the I2C kernel module.

<a name="serial"></a>
#### Serial

Enable/Disable shell and kernel messages on the serial connection.

<a name="audio"></a>
#### Audio

Force audio out through HDMI or a 3.5mm jack. Read more on the [audio configuration documentation page](audio-config.md).

<a name="update"></a>
#### Update

Update this tool to the latest version.

<a name="about"></a>
### About raspi-config

Selecting this option shows the following text:

```
This tool provides a straightforward way of doing initial configuration of the Raspberry Pi. Although it can be run at any time, some of the options may have difficulties if you have heavily customised your installation.
```

<a name="finish"></a>
### Finish

Use this button when you have completed your changes. You will be asked whether you want to reboot or not. When used for the first time, it's best to reboot. There will be a delay in rebooting if you have chosen to resize your SD card.

<a name="development-of-this-tool"></a>
## Development of this tool

See this tool's source at [github.com/RPi-Distro/raspi-config](https://github.com/RPi-Distro/raspi-config), where you can open issues and create pull requests.

---

*This article uses content from the eLinux wiki page [RPi raspi-config](http://elinux.org/RPi_raspi-config), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*

