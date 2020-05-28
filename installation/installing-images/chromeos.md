# Installing operating system images using Chrome OS

The easiest way to write images to an SD card and USB drives with Chrome OS is to use the official [Chromebook Recovery Utility](https://chrome.google.com/webstore/detail/chromebook-recovery-utili/jndclpdbaamdhonoechobihbbiimdgai). It can be used to create Chromebook Recovery media, and it will also accept .zip files containing images.
 
## Using the Recovery Utility

- Download the [Chromebook Recovery Utility](https://chrome.google.com/webstore/detail/chromebook-recovery-utili/jndclpdbaamdhonoechobihbbiimdgai).
- Download the [Raspberry Pi OS .zip file](https://www.raspberrypi.org/downloads/raspbian/).
- Launch the **Recovery Utility**
- Click on the **Settings Gears** icon in the upper right-hand corner, next to the window close icon.
- Select the **Use Local Image** option.
- Choose the .zip file you downloaded.
- Insert the SD card and click **Continue**.
- Read the warning and click the **Create now** button.
- Wait for the progress bar to complete twice (for unpacking and writing). This might take a few minutes. Once the process is complete, a big green checkmark will be shown.
- Close the program and eject the card.
