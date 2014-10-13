# Changing the default pin configuration
*This feature is intended for advanced users.*

As of July 15th 2014, the Raspberry Pi firmware supports custom default pin configurations through a user-provided device tree blob file. In order to ensure that your firmware is recent enough, please run `vcgencmd version`.
## Providing a custom device tree blob
In order to compile a device tree source (*dts*) file into a device tree blob (*dtb*) file, the device tree compiler must be installed by running `sudo apt-get install device-tree-compiler`.
 The `dtc` command can then be used as follows:
```
sudo dtc -I dts -O dtb -i dt-blob.dts -o /boot/dt-blob.bin
```
**NOTE:** In the case of NOOBS installs, the dtb file should be placed on the recovery partition instead.

Similarly, a dtb file can be converted back to a dts file, if required.
```
dtc -I dtb -O dts -i /boot/dt-blob.bin -o dt-blob.dts
```
# Sections of the dt-blob
The dt-blob.bin is used to configure the binary blob (Videocore) at boot time.  It is not something that the linux kernel
uses (at the moment) although a kernel section will be added at a later stage when we move the Raspberry Pi kernel to use
a dt-blob for configuration.  The dt-blob is capable of configuring each of the different versions of the Raspberry Pi
including the Compute Module to set up the alternate settings correctly. The following sections are valid in the dt-blob.

1. `videocore`

   This section contains the whole videocore blob information, all subsequent sections must be enclosed within this section

2. `pins_*`

   There are up to four separate pins_* sections these are:
   1. **pins_rev1** Rev1 pin setup.  There are some difference because of the moved I2C pins
   2. **pins_rev2** Rev2 pin setup.  This includes the additional codec pins on P5
   3. **pins_bplus** B+ revision including the full 40pin connector
   4. **pins_cm** The Compute Module, note the default for this is the default for the chip so can be a useful source of information about default pullups / downs on the chip.
   
   Each `pins_*` section can contain `pin_config` and `pin_defines` sections.

3. `pin_config`

   The `pin_config` section is used to configure the individual pins, each item in this section must be a named pin section, such as `pin@p32` meaning GPIO32.  There is a special section `pin@default` which has the default settings for anything not specifically named in the pin_config section.
   
4. `pin@pinname`

   This section can contain any combination of the following items
   1. `polarity`
      * `active_high`
      * `active_low`
   2. `termination`
      * `pull_up`
      * `pull_down`
      * `no_pulling`
   3.`startup_state`
      * `active`
      * `inactive`
   4.`function`
      * `input`
      * `output`
      * `sdcard`
      * `i2c0`
      * `i2c1`
      * `spi`
      * `spi1`
      * `spi2`
      * `smi`
      * `dpi`
      * `pcm`
      * `pwm`
      * `uart0`
      * `uart1`
      * `gp_clk`
      * `emmc`
      * `arm_jtag`
   5. `drive_strength_ma`
      The drive strength is used to set a strength for the pins, please note you can only set the bank to a single drive strength. <8> <16> are valid values
5. `pin_defines`

   This section is used to set specific videocore functionality to particular pins, this enables the user to move the camera power enable pin to somewhere different or the hdmi hotplug postion (i.e. things that linux have no control over).  Please refer to the example dts file below

## Clock configuration

It is possible to change the configuration of the clocks through this interface, although very difficult to predict the results!  The configuration of the clocking system is very very complex, there are five separate PLLs each one has its own fixed (or variable in the case of PLLC) VCO frequency.  Each VCO then has a number of different channels which can be set up with a different division of the VCO frequency.  Then each of the clock destinations can then be configured to come from one of the clock channels (although there is a restricted mapping of source to destination so not all channels can be routed to all clock destinations).

For this reason I'll just add here a couple of example configurations that you can use to alter very specific clocks.  Beyond this it is something we'll add to when requests for clock configurations are made.

```
clock_routing {
   vco@PLLA  {    freq = <1966080000>; };
   chan@APER {    div  = <4>; };
   clock@GPCLK0 { pll = "PLLA"; chan = "APER"; };
};

clock_setup {
   clock@PWM { freq = <2400000>; };
   clock@GPCLK0 { freq = <12288000>; };
   clock@GPCLK1 { freq = <25000000>; };
};
```

The above will set the PLLA to a source VCO running at 1.96608GHz (the limits for this VCO are 600MHz - 2.4GHz), the APER channel to /4 and configures GPCLK0 to be sourced from PLLA through APER.  This is used specifically to give an audio codec the 12288000Hz it needs to do the 48000 range of frequencies.
## Sample device tree source file
**NOTE:** As this is a new feature, there is no reference dts file which is guaranteed to be supported by future firmware revisions.

The dts file below is used for the dtb compiled into the August 1st 2014 firmware.
```
    /dts-v1/;

    / {
       videocore {
                pins_rev1 {
                   pin_config {
                      pin@default {
                         polarity = "active_high";
                         termination = "pull_down";
                         startup_state = "inactive";
                         function = "input";
                      }; // pin
                      pin@p2  { function = "i2c1";   termination = "pull_up"; }; // I2C 1 SDA
                      pin@p3  { function = "i2c1";   termination = "pull_up"; }; // I2C 1 SCL
                      pin@p5  { function = "output"; termination = "pull_down"; }; // CAM_LED
                      pin@p6  { function = "output"; termination = "pull_down"; }; // LAN NRESET
                      pin@p14 { function = "uart0";  termination = "no_pulling"; drive_strength_mA = < 8 >; }; // TX uart0
                      pin@p15 { function = "uart0";  termination = "pull_up"; drive_strength_mA = < 8 >; }; // RX uart0
                      pin@p16 { function = "output"; termination = "pull_up"; polarity="active_low"; }; // activity LED
                      pin@p27 { function = "output"; termination = "no_pulling";    }; // Camera shutdown
                      pin@p40 { function = "pwm";    termination = "no_pulling"; drive_strength_mA = < 16 >; }; // Left audio
                      pin@p45 { function = "pwm";    termination = "no_pulling"; drive_strength_mA = < 16 >; }; // Right audio
                      pin@p46 { function = "input";  termination = "no_pulling";    }; // Hotplug
                      pin@p47 { function = "input";  termination = "no_pulling";    }; // SD card detect
                      pin@p48 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD CLK
                      pin@p49 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD CMD
                      pin@p50 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D0
                      pin@p51 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D1
                      pin@p52 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D2
                      pin@p53 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D3

                   }; // pin_config
                   pin_defines {
                      pin_define@HDMI_CONTROL_ATTACHED {
                         type = "internal";
                         number = <46>;
                      };
                      pin_define@NUM_CAMERAS {
                         type = "internal";
                         number = <1>;
                      };
                      pin_define@CAMERA_0_UNICAM_PORT {
                         type = "internal";
                         number = <1>;
                      };
                      pin_define@CAMERA_0_I2C_PORT {
                         type = "internal";
                         number = <1>;
                      };
                      pin_define@CAMERA_0_SDA_PIN {
                         type = "internal";
                         number = <2>;
                      };
                      pin_define@CAMERA_0_SCL_PIN {
                         type = "internal";
                         number = <3>;
                      };
                      pin_define@CAMERA_0_SHUTDOWN {
                         type = "internal";
                         number = <27>;
                      };
                      pin_define@CAMERA_0_LED {
                         type = "internal";
                         number = <5>;
                      };
                      pin_define@FLASH_0_ENABLE {
                         type = "absent";
                      };
                      pin_define@FLASH_0_INDICATOR {
                         type = "absent";
                      };
                      pin_define@FLASH_1_ENABLE {
                         type = "absent";
                      };
                      pin_define@FLASH_1_INDICATOR {
                         type = "absent";
                      };
                      pin_define@POWER_LOW {
                         type = "absent";
                      };
                      pin_define@LEDS_DISK_ACTIVITY {
                         type = "internal";
                         number = <16>;
                      };
                      pin_define@LAN_RESET {
                         type = "internal";
                         number = <6>;
                      };
                   }; // pin_defines
                }; // pins_rev1

                pins_rev2 {
                   pin_config {
                      pin@default {
                         polarity = "active_high";
                         termination = "pull_down";
                         startup_state = "inactive";
                         function = "input";
                      }; // pin
                      pin@p0  { function = "i2c0";   termination = "pull_up"; }; // I2C 0 SDA
                      pin@p1  { function = "i2c0";   termination = "pull_up"; }; // I2C 0 SCL
                      pin@p5  { function = "output"; termination = "pull_down"; }; // CAM_LED
                      pin@p6  { function = "output"; termination = "pull_down"; }; // LAN NRESET
                      pin@p14 { function = "uart0";  termination = "no_pulling"; drive_strength_mA = < 8 >; }; // TX uart0
                      pin@p15 { function = "uart0";  termination = "pull_up"; drive_strength_mA = < 8 >; }; // RX uart0
                      pin@p16 { function = "output"; termination = "pull_up"; polarity = "active_low"; }; // activity LED
                      pin@p21 { function = "output"; termination = "no_pulling";    }; // Camera shutdown
                      pin@p40 { function = "pwm";    termination = "no_pulling"; drive_strength_mA = < 16 >; }; // Left audio
                      pin@p45 { function = "pwm";    termination = "no_pulling"; drive_strength_mA = < 16 >; }; // Right audio
                      pin@p46 { function = "input";  termination = "no_pulling";    }; // Hotplug
                      pin@p47 { function = "input";  termination = "no_pulling";    }; // SD card detect
                      pin@p48 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD CLK
                      pin@p49 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD CMD
                      pin@p50 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D0
                      pin@p51 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D1
                      pin@p52 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D2
                      pin@p53 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D3

                   }; // pin_config
                   pin_defines {
                      pin_define@HDMI_CONTROL_ATTACHED {
                         type = "internal";
                         number = <46>;
                      };
                      pin_define@NUM_CAMERAS {
                         type = "internal";
                         number = <1>;
                      };
                      pin_define@CAMERA_0_I2C_PORT {
                         type = "internal";
                         number = <0>;
                      };
                      pin_define@CAMERA_0_SDA_PIN {
                         type = "internal";
                         number = <0>;
                      };
                      pin_define@CAMERA_0_SCL_PIN {
                         type = "internal";
                         number = <1>;
                      };
                      pin_define@CAMERA_0_SHUTDOWN {
                         type = "internal";
                         number = <21>;
                      };
                      pin_define@CAMERA_0_UNICAM_PORT {
                         type = "internal";
                         number = <1>;
                      };
                      pin_define@CAMERA_0_LED {
                         type = "internal";
                         number = <5>;
                      };
                      pin_define@FLASH_0_ENABLE {
                         type = "absent";
                      };
                      pin_define@FLASH_0_INDICATOR {
                         type = "absent";
                      };
                      pin_define@FLASH_1_ENABLE {
                         type = "absent";
                      };
                      pin_define@FLASH_1_INDICATOR {
                         type = "absent";
                      };
                      pin_define@POWER_LOW {
                         type = "absent";
                      };
                      pin_define@LEDS_DISK_ACTIVITY {
                         type = "internal";
                         number = <16>;
                      };
                      pin_define@LAN_RESET {
                         type = "internal";
                         number = <6>;
                      };
                    }; // pin_defines
                }; // pins

                pins_bplus {
                   pin_config {
                      pin@default {
                         polarity = "active_high";
                         termination = "pull_down";
                         startup_state = "inactive";
                         function = "input";
                      }; // pin
                      pin@p14 { function = "uart0";  termination = "no_pulling"; drive_strength_mA = < 8 >; }; // TX uart0
                      pin@p15 { function = "uart0";  termination = "pull_up"; drive_strength_mA = < 8 >; }; // RX uart0
                      pin@p28 { function = "i2c0";   termination = "pull_up";    }; // I2C 0 SDA
                      pin@p29 { function = "i2c0";   termination = "pull_up";    }; // I2C 0 SCL
                      pin@p31 { function = "output"; termination = "pull_down"; }; // LAN NRESET
                      pin@p32 { function = "output"; termination = "pull_down"; }; // Camera LED
                      pin@p35 { function = "input";  termination = "no_pulling"; polarity = "active_low"; }; // Power low
                      pin@p38 { function = "output"; termination = "no_pulling";    }; // USB current limit (0=600mA, 1=1200mA)
                      pin@p40 { function = "pwm";    termination = "no_pulling"; drive_strength_mA = < 16 >; }; // Left audio
                      pin@p41 { function = "output"; termination = "no_pulling";    }; // Camera enable
                      pin@p44 { function = "gp_clk"; termination = "pull_down"; }; // Ethernet 25MHz output
                      pin@p45 { function = "pwm";    termination = "no_pulling"; drive_strength_mA = < 16 >; }; // Right audio
                      pin@p46 { function = "input";  termination = "no_pulling"; polarity = "active_low"; }; // Hotplug
                      pin@p47 { function = "output"; termination = "pull_down"; }; // activity LED
                      pin@p48 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD CLK
                      pin@p49 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD CMD
                      pin@p50 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D0
                      pin@p51 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D1
                      pin@p52 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D2
                      pin@p53 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D3

                   }; // pin_config
                   pin_defines {
                      pin_define@HDMI_CONTROL_ATTACHED {
                         type = "internal";
                         number = <46>;
                      };
                      pin_define@NUM_CAMERAS {
                         type = "internal";
                         number = <1>;
                      };
                      pin_define@CAMERA_0_I2C_PORT {
                         type = "internal";
                         number = <0>;
                      };
                      pin_define@CAMERA_0_SDA_PIN {
                         type = "internal";
                         number = <28>;
                      };
                      pin_define@CAMERA_0_SCL_PIN {
                         type = "internal";
                         number = <29>;
                      };
                      pin_define@CAMERA_0_SHUTDOWN {
                         type = "internal";
                         number = <41>;
                      };
                      pin_define@CAMERA_0_UNICAM_PORT {
                         type = "internal";
                         number = <1>;
                      };
                      pin_define@CAMERA_0_LED {
                         type = "internal";
                         number = <32>;
                      };
                      pin_define@FLASH_0_ENABLE {
                         type = "absent";
                      };
                      pin_define@FLASH_0_INDICATOR {
                         type = "absent";
                      };
                      pin_define@FLASH_1_ENABLE {
                         type = "absent";
                      };
                      pin_define@FLASH_1_INDICATOR {
                         type = "absent";
                      };
                      pin_define@POWER_LOW {
                         type = "internal";
                         number = <35>;
                      };
                      pin_define@LEDS_DISK_ACTIVITY {
                         type = "internal";
                         number = <47>;
                      };
                      pin_define@LAN_RESET {
                         type = "internal";
                         number = <31>;
                      };
                    }; // pin_defines
                }; // pins

                pins_cm {
                   pin_config {
                      pin@default {
                         polarity = "active_high";
                         termination = "pull_down";
                         startup_state = "inactive";
                         function = "input";
                      }; // pin
                      pin@p14 { function = "uart0";  termination = "no_pulling";    }; // TX uart0
                      pin@p15 { function = "uart0";  termination = "pull_up"; }; // RX uart0
                      pin@p48 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD CLK
                      pin@p49 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD CMD
                      pin@p50 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D0
                      pin@p51 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D1
                      pin@p52 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D2
                      pin@p53 { function = "sdcard"; termination = "pull_up";    drive_strength_mA = < 8 >; }; // SD D3

                   }; // pin_config
                   pin_defines {
                   }; // pin_defines
                }; // pins_cm
       };
    };
```
