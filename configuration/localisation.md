# Localisation

Set your Raspberry Pi up to match your regional settings.


## Language

### NOOBS

To change the language used by NOOBS, you can either press the `L` key on your keyboard, press the up/down arrows to choose the language you want, and then press `Enter`; or you can do the same thing using the mouse. NOOBS will remember your selection, and will use the same language again next time.

Alternatively, you can pre-select the language before booting NOOBS for the first time. See [here](https://github.com/raspberrypi/noobs/blob/master/README.md#how-to-change-the-default-language-keyboard-layout-display-mode-or-boot-partition).

### Raspberry Pi OS

If you've installed Raspberry Pi OS using NOOBS, it should automatically pick up the same language you were using within NOOBS. But if you want to select a different language, or if you've installed Raspberry Pi OS from a standalone image, use [raspi-config](raspi-config.md#change-locale).


## Keyboard

### NOOBS

To change the keyboard layout used by NOOBS, you can either press the `9` key on your keyboard, press the up/down arrows to choose the keyboard you want, and then press `Enter`; or you can do the same thing using the mouse. Note that changing the language (as described above) may automatically change the keyboard layout as appropriate too. NOOBS will remember your selection and use the same keyboard layout again next time.

Alternatively, you can pre-select the keyboard before booting NOOBS for the first time. See [here](https://github.com/raspberrypi/noobs/blob/master/README.md#how-to-change-the-default-language-keyboard-layout-display-mode-or-boot-partition).

### Raspberry Pi OS

If you've installed Raspberry Pi OS using NOOBS, it should automatically pick up the same keyboard you were using in NOOBS. But if you want to select a different keyboard, or if you've installed Raspberry Pi OS from a standalone image, use [raspi-config](raspi-config.md#change-keyboard-layout).


## Timezone

### NOOBS

No part of NOOBS uses the time; consequently there is no option for changing the timezone.

### Raspberry Pi OS

Once again, this is something you can change using the [raspi-config](raspi-config.md#change-timezone) tool.
