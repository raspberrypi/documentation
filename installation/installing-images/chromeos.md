# Installing operating system images using ChomeOS

Easiest option to write images to an SD card and USB drives with ChromeOS is to use the official [Chromebook Recovery Utility](https://chrome.google.com/webstore/detail/chromebook-recovery-utili/jndclpdbaamdhonoechobihbbiimdgai). It can be used to create Chromebook Recovery media, but it will also accept .zip files containing images.
 
## Recovery Utility

- Download the [Chromebook Recovery Utility](https://chrome.google.com/webstore/detail/chromebook-recovery-utili/jndclpdbaamdhonoechobihbbiimdgai).
- Download the [Raspbian .zip file](https://www.raspberrypi.org/downloads/raspbian/)
- Launch the Recovery Utility
- Click the Settings Gears icon in the upper right next to the window close icon.
- Select the Use Local Image option
- Choose the Downloaded .zip file
- Insert the SD card and click Continue
- Read the warning and click the **Create now** button
- Wait for the progress bar to complete twice (unpacking and writing, might take a couple of minutes).
- A big green checkmark will be shown once done. You can close the utility and eject the card.
