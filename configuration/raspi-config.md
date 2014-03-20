# raspi-config

`raspi-config` is the Raspberry Pi configuration tool written and maintained by [Alex Bradbury](https://github.com/asb).


## The raspi-config script

When you start your Pi the display shows the output from each of the start-up scripts (as lots of scrolling text). If starting for the first time using a new image you are logged in as a root user, and the raspi-config menu will then appear. It can also be started at any time from the command line or from a terminal window (see below).

It has the following entries (this is the layout from the Raspian 2012-12-16 image. It may be different on other images):

```
 Raspi-config
  
 info                Information about this tool
 expand_rootfs       Expand root partition to fill SD card
 overscan            Change overscan
 configure_keyboard  Set keyboard layout
 change_pass         Change password for 'pi' user
 change_locale       Set locale
 change_timezone     Set timezone
 memory_split        Change memory split
 ssh                 Enable or disable ssh server
 boot_behaviour      Start desktop on boot?
 update              Try to upgrade raspi-config
  
     <Select>                    <Finish>
```

###Moving Around the Menu

It looks like its running as a graphical application but in fact it isn't; its using the command line and graphical tools for the layout of the text. Cursor up/down keys move the highlight up and down menus.

At any point from within any of the menu or sub-menu options the Tab key will switch from the selected menu entry and the "buttons" at the bottom (inside angle brackets). So, move the highlight to the menu option you want to use, press Tab, then press Return.

Some of the menu entries take a while to read configuration information before they change what is displayed. Be patient.

###What raspi-config does

Some menu entries modify the file /boot/config.txt. This file, out of the box, contains a number of commented out configuration entries; raspi-config adds entries at the end of this file. You can see what raspi-config has done to the
file by viewing it on the Pi using Leafpad. More information on editing config.txt here [[R-Pi_ConfigurationFile]]

Other entries modify Linux configuration files. Some take effect immediately, others at the next boot.

###Running raspi-config another time 

Following the first boot, your raspberry pi will boot into the command prompt or desktop (you choose in raspi-config). You can run it at any time after that from the command line or in a terminal window by typing (case sensitive):

 sudo raspi-config

The sudo (do as superuser) is necessary because you will be changing files that you as user pi do not own.

## Menu Options

Here is a description of each menu entry.

### info - Information About This Tool

It helpfully advises that it is for initial configuration, and can be run at any time. You may have difficulties if you have heavily customized your installation as the changes it makes might not be correct if what it attempts to change is not what it expects.

### expand_rootfs - Expand root partition to fill SD card

The usual distribution images are 2 GB. When you copy the image to a larger SD card you have a portion of that card unused. This option expands the initial image to expand to fill the rest of the SD card, giving you more space. You need to reboot the Raspberry Pi to make this available. THERE IS NO CONFIRMATION - SELECTING THE OPTION EXPANDS THE PARTITION.

### overscan - Change overscan

Old photographs had a border round the outside to allow for handling and mounting. Old TV sets had a significant variation in the size of the picture it produced; some had cabinets that overlapped the screen. Like the photographs, the TV pictures were given a black border so that none of the picture was lost. This is called overscan. Modern TVs and monitors don't need, and the signal doesn't have, the border. If the initial text shown on the screen disappears off the edge you need to enable overscan to add back the border.

Any changes will take effect after a reboot. You can have greater control over the settings by editing boot/config.txt.

On some displays, particularly monitors, just disabling Overscan will make the picture fill the whole screen and correct the resolution. For other displays it may be necessary to leave overscan enabled and adjust the Overscan values

### configure-keyboard - Set keyboard layout 

This option selects the keyboard being used, so that the characters produced are the same as those typed (important examples are # and /). It is slow to display, while it reads all the keyboard types. Changes usually take effect immediately, but may require a reboot.

Brands of keyboards are chosen first followed by other choices to set up the nationality of the keyboard. The default is a Generic 105-key (Intl) PC. If you cannot find your keyboard on the list then use one of the generic keyboards. Check [http://en.wikipedia.org/wiki/Keyboard_layout | this page] for most keyboard layouts. The next screen gives the keyboard layout. If you are not using the first choice of English UK select Other and you will be faced with a long list of other national keyboards.

You then select specific options:
* No AltGr key
* [[wikipedia:Compose key|Compose key]] — Many people choose not to set up a Compose key, but it can be useful for typing symbols or accented characters on a regular keyboard. If you wish to define a Compose key, instructions on how to do so are here: [[RPi Compose key|Compose key]].
* Shutdown XServer (use [Ctrl][Alt][Backspace] all pressed at the same time)

###change_pass - Change password for ‘pi’ user

The default user for the Raspian install is "pi" and its password is "raspberry". If you change the password, other people will need to know the new password, including you, to logon to the Raspberry Pi. Each user/password combination can be different on each SD card.

###change_locale - Set locale

This option selects the characters and other symbols being displayed on the screen, and is important if you want to use the non-english ones. It is slow to display, while it reads all the locale information. Changes usually take effect immediately, but may require a reboot.

You usually select only the one(s) you want (press space); this will generate the configuration data for all those you select. The default setting is en_GB UTF-8 UTF-8

###change_timezone - Set timezone

This is where you setup your system clock; if it’s wrong it just means the date and time assigned to files you create (automatically when you make them) will be wrong. It is slow to display as there are lots of selections. First you select the continent, then select a City from that continent. You may have to select the one nearest to you.

The Raspberry Pi does not have an onboard clock (you can add one), so the "clock" stops when you power it off. If you are connected to the internet the Raspberry Pi can be set up to get the time from an online time signal.

###memory_split - Change memory split

The Raspberry Pi has two processors, one for calculation tasks (the CPU) and one for graphical tasks (the GPU). The CPU is described as the ARM; the GPU as the VideoCore. This version takes account of the 256 MB or 512 MB boards, and allows a dynamic reallocation of memory, whereas older versions of raspi-config only split the 256 MB and could not set the dynamic option. The best setting will depend on what type of applications you are running on your Raspberry Pi.

###ssh - Enable or disable ssh server

Enabling ssh will allow you to connect to your Raspberry Pi from another device on your network and use a terminal window remotely. You do not need a monitor or keyboard connected to your Raspberry Pi if you do this.

Unless you want to use the Raspberry Pi remotely you can disable this, as it stops the ssh service which takes a small amount of processing resources. If you want to set this up, see the [[RPi_A_Method_for_ssh_blind_login | ssh page]].

###boot_behaviour - Start desktop on boot?

The official images are supplied with the Raspberry Pi booting into a command line, presumably because problems with connecting the display are fewer and simpler. If you think you are ok with the GUI interface you can boot to this. You can change this at any time.

* Desktop (GUI interface) - gives a picture based screen, similar to a Windows, Mac or smartphone, that requires a mouse to select actions (usually). This option also skips the login by using the pi user. Pressing the red Exit button on the right hand side of the screen will give the options to logout, shutdown or reboot. Using logout will give a GUI login screen. Using Ctrl-Alt-Backspace also gives a GUI login screen. To use a command line open the Terminal window. To get back to the command line, logout and press Ctrl-Alt-F1. To permanently get back the command line, run raspi-config and reset the boot behaviour and restart.

* Command line - gives a text based screen that requires the user to type commands on the keyboard only. Usually the mouse is not required, but some command line programs can use mouse control. You can switch to the GUI screen by typing "startx" and pressing 'Enter'. This time the red Exit button on the right hand side of the screen will only give the option to logout. This returns you to the command line. To stop or reboot the Raspberry Pi type "sudo halt" or "sudo reboot" and press 'Enter'.

###update - Try to upgrade raspi-config

The raspi-config utility has changed quite a bit since it started, and is likely to continue to change. Use this option to check if your version of raspi-config is the latest, and if not download the latest version; you will need to be connected to the internet to update it. Once updating is complete, raspi-config will close. You should restart raspi-config with "sudo raspi-config" to make sure that you have completed all the options.

###Finish>

Use this 'button' when you have completed your changes. You will be asked whether you want to reboot or not. When used for the first time its best to reboot. This should restart your Pi. There will be a delay if you have chosen to resize your SD card.


##History

This utility script was first released with the Debian Wheezy image of 18 June 2012. It is expected to continue changing so the number of menu items and the ease of use of those items will increase with time. If anyone feels willing and able to improve raspi-config then please contact Alex Bradbury [https://github.com/asb/raspi-config].

##Is this useful?

This may be just a bit of background information, but it could be useful if you wish to distribute your own SD cards to friends, based on your own configuration. You may have added or removed packages, changed configurations, or any number of things that you and your friends think are useful.

You can create a backup image of your SD card, but that image will not execute the raspi-config script on first boot; your friends may need to run it because they have different hardware. To make that script run automatically, copy the top script to '''/etc/profile.d/raspi-config.sh''' and change the '''/etc/inittab''' script back to the original lines.

_____

Thanks to eLinux.org

