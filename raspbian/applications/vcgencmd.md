## VCGENCMD

`vcgencmd` is a command line application that provides a set of commands for communicating with the VideoCore GPU. The application is very simple, redirecting the command line to the VideoCore which then acts on the information and returns back the results.

The source for the application can be found on our github page [here](https://github.com/raspberrypi/userland/tree/master/host_applications/linux/apps/gencmd).

### Usage

To get a list of available commands, use `vcgencmd commands`.

Some of the more useful  commands are described below.


### Commands 

#### vcos

The `vcos` cammand has a number of sub commands

`version` Displays the build date and version of the firmware on the VideoCore.
`log status` Displays the error log status of the various VideoCore software areas.

#### version

Displays the build date and version of the firmware on the VideoCore.

#### get_camera

Displays the supported and deected state of the official camera. 1 means yes, 0 means no.

#### get_throttled

Returns the throttled state of the system. This is a bit pattern.

| Bit | Meaning |
|:---:|---------|
| 0   | under-voltage |
| 1   | arm frequency capped |
| 2   | currently throttled |
| 16  | under-voltage has occurred |
| 17  | arm frequency capped has occurred |
| 18  |throttling has occurred |

#### measure_temp

Returns the temperature of the SoC as measured by the on board temperature sensor

