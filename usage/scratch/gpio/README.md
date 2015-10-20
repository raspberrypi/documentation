# Scratch GPIO

The September 2015 release of Scratch for the Pi (included in the Raspbian Jessie release) introduces a new GPIO server to make driving LEDs, buzzers, HATS and other devices and components easier.

## GPIO Server

### Usage and basic capabilities

Before you can use the GPIO pins you *must* start the GPIO server. There are several ways to do this:

- Choose *Start GPIO server* from the *Edit* menu to turn it on. If the server is running then *Stop GPIO server* will turn it off.
- A Scratch broadcast of `gpioserveron` or `gpioserveroff` will have the obvious effect.
- Projects saved when the GPIO server is running will have that status recorded and on loading will try to start the server if it is enabled.

Without any further setup you now have access to the basics of the GPIO system. This currently uses the Broadcast blocks. For instance, to configure GPIO pin 4 as an out put and turn it on you create the two following broadcasts:

![broadcast config4 out gpio4on](images/config-on.png)

As always you can assemble this text with normal join or pick or list handling blocks. For example if `foo` = 17, then

![broadcast join gpio join foo 17](images/broadcastgpio17on.png)   

would broadcast `gpio17on` and thus set the GPIO pin number 17 (under the BCM numbering) to on.

However, the pins need configuring before you can meaningfully use them to do anything. We can set the direction of the pin (in, out, outputpwm) and for input pins the pull-up mode (up, down, none). Currently the pins are only configurable via broadcasts.
For example -     

![broadcast config 11 inpulldown](images/broadcastconfig11inpulldown.png)  

Pins set to be inputs are connected to the Scratch sensor variable system, and so they appear in the list of possible values in the sensor blocks.  

![sensor block gpio11](images/sensorgpio11.png)  

and can be used in the same manner  
![if gpio11 sensor value](images/ifgpio11sensorvalue.png)  

With these very simple commands you can build fairly complex gpio handling scripts.
As an example of how not everything has to be strictly gpio connected to be used from this system, we also have commands to

- return the time
- return the machine ip address
- take a photo with an attached Pi camera and set it as the current costume.

This script -  

![gpio-demo script](images/gpio-demo.gif)  

illustrates most of the above by providing (along with a suitably configured breadboard) the ability to turn leds on and off according to a button, to take a photo with a countdown provide by a progressively brightening led, and ways to check the time etc. Note that we can have a single broadcast that includes several messages ie `gpio24on gpio18pwm400` above. The text will be split on the spaces and be treated as a list of independent broadcasts.

### Basic commands

In the command listings below we use
`[comm] + pin number + [ on | off]`  
to indicate a command of the form   
`comm17off` or `comm7on`  
For a variable  
`led + light number (1..5) =  ( 0 .. 100)`  
indicates a variable named `led5` may have a value from 0 to 100  
or  
`foo = ( 1 | 4 | 7 )`  
indicates variable `foo` may be set to 1 or 4 or 7.

The basic gpio layer command list is

- config + pin number +
    + in, input, inpullup or inputpullup to set as input with pull-up
    +  inpulldown or inputpulldown
    + inpullnone or inputpulldown
    + out or output to set as digital output
    + outputpwm to set as a pwm pin
example `config12in`  
- gpio + pin number + [ on | high | off | low ]
example `gpio17on`
- gpio + pin number + pwm + [ 0..1024 ] \(we can use the software driven pwm output facility)
example `gpio22pwm522`
- gettime
- getip
- photo

### Add-on hardware

We can also plug in Pi add-on cards such as the PiGlow, Pibrella, Explorer Hat etc.
To set up a card we need to first inform the gpio server what card it is and this is done by creating and setting a variable `AddOn`, like this -  

![set addon to piglow](images/setaddonpiglow.png)

Each card has its own set of commands layered on top of the basic gpio facilities described above. In principle the driver for a card could usurp a basic command such as ‘gpio’ and there may need to be some mechanism added to prevent this if simple common sense is not in sufficient supply.
Many cards can also make sensible use of the Scratch variable broadcast facility, whereby a suitably named variable is created and its value gets broadcast when it changes. For example, for a PiGlow board it makes sense to have variables named for each led or ring of leds and to set the value as a way of controlling the brightness. It is quite possible to cause confusion with ill-considered use of both forms of control at the same time; broadcasting `myCommand400` in the same script as setting `myValue` to 200 might well result in flickering or apparent non-function or perhaps even hardware failure in extreme cases. All you need to do to use this is create a variable of the appropriate name and set its value.
Some cards provide inputs that can be accessed via the sensor variables as shown above in the example usage of pin 11.

#### PiFace

The Piface Digital card provides 8 digital inputs and 8 digital outputs, with the first 4 inputs having parallel switches and the first 2 outputs having 20v/5A relays. There is an observed problem with the inputs being flighty to say the least, and merely holding a finger near the input terminal blocks appears to cause flickering of the read values.
PiFace has just two commands -

- `all + [ on | off]`
- `output + output number + [ on | high | off | low ]`

and one variable command  
- `output + [ 0 .. 7 ] = (0 |1 )` - the value is rounded and subjected to max/min  limiting so -1 rounds up to 0, 400000000 rounds down to 1

There are also the 8 input sensor variables named `Input1` to `Input8` which have possible values (0|1)

#### Pibrella

This provides a nice big red button, three large LEDs, four digital inputs, four digital outputs and a loudly obnoxious buzzer. The commands are

- `[ red | yellow | green ] + [ on | high | off | low ]`
- `Buzzer + (0 .. 4000)`
- `Output + [ E | F | G | H ] + [ on | high | off | low ]`

Variables offered are

- `Buzzer = (0..10000)`
- `[ red | green | yellow ]  = (0 |1 )`
- `Output + [ E | F | G | H ]  = (0 |1 )`

The inputs A,B,C,D, and of course the fabulous BigRedButton are provided as sensor variables all having possible values (0|1).

#### Explorer HAT Pro

This card is a bit more of a challenge to drive since it has  parts that are plain gpio connected and parts that are i2c connected.

- LEDs
- Output connectors
- Input connectors
- Motor driver (2 off)
- ADCs (4 off)

The commands currently operational are

- `led + led number ( 1 .. 3) +  [ on | high | off | low ]`
- `output + input number ( 1 .. 3) +  [ on | high | off | low ]`
- `motor + motor number (1|2) + speed + (0..100)` - motor speed is set as a percentage.

They have matching variable forms

- `led + led number  = (0 |1 )`
- `output + led number  = (0 |1 )`
- `motor + motor number (0|1) = (0..100)`

and sensor variables `Input1` to `Input4` with values (0|1) and the four ADC pins (1..4) with values +-6.1V - if the signal is derived from a pot connected to the ExplorerHAT 5v/gnd then obviously the range is (0..~5)

NB The capacitive input pads are not yet operational, requiring some library level support.

#### Sense HAT (as used in the Astro Pi)

This foundation built card provides a range of unusual sensors and a big 8 by 8 array of rgb LEDs.
The sensors measure

- temperature
- humidity
- pressure
- accelerometer/gyro
- magnetometer/compass
- mini-joystick actions left/right/up/down/return

Commands supported

- `clearleds` - sets all LEDs to background colour
- `ledbackground`
- `ledforeground` - set the background & foreground colours for the string & graph commands to use. Colour is specified with either
    + a name from the list `red cyan blue gray black white green brown orange yellow magenta palered paletan lightred paleblue palebuff darkgray lightblue…`
    + an html style six hex digit number `#RRGGBB`
- `ledscrollspeed` - number of milliseconds delay per step of scrolling a string
- `ledscrollstring` - scroll the following string with the previously set foreground & background colours
- `ledshowchar` - show just a single character with the previously set foreground & background colours
- `ledbargraph12345678` - make a simple bar graph of up to 8 digits (values 0..8) with the previously set foreground & background colours
- `ledshowsprite+name of sprite` - display the named sprite on the LEDs; the sprite is centred over the 8x8 array and so you may see very little of a large sprite.

The accelerometer, gyro & compass raw & scaled X,Y,Z values are available as sensor variables but are not at all well calibrated as yet. The maths to convert them to useful integrated values remains to be done.

#### PiLite

This card provides a simple array of while LEDs that can be addressed individually or treated as a scrolling text display, a bargraph or a vu meter. It works via the gpio serial port and presents some interesting challenges despite its apparent simplicity.

Commands currently supported

- `allon`, `alloff`
- `scrollstringABCDEF` to display ABCDEF.
- `bargraph[1..14],[1-100]` sets the bar shown on one of the 14 columns of leds to represent the percentage.
- `vumeter[1|2],[1…100]`

#### RyanTeck & Pololu motor controller

Both of these little cards can drive two DC motors. Though they work quite differently they share the same commands.

- `motor + motor number (1|2) + speed + value (-100..100)`

And matching variable forms

- `motor + motor number (0|1) = (-100..100)`

### Demo project scripts

In the Scratch `Examples` directory (found via the `File->open` dialogue and the `Examples` shortcut) you will find a `Motors and Sensors` directory; several new gpio scripts are included.

- `gpio-demo` - shown above, this is a test of all the basics.
    + Connect a breadboard to your Pi.
    + connect an led to gpio 18 with a 220ohm resistor to ground
    + connect an led to gpio 24 with a 220ohm resistor to ground
    + connect a normally open button to gpio 22 and ground
    + start the gpio server
    + click on the green Go button to initalise pin config
    + ‘o’ will loop and if the button is pressed it should turn on the led attached to gpio 24 and dimly light the other led, otherwise both should be off
    + ‘p’ will gradually brighten the led attached to gpio 18, then make it fully bright and take a photo with an attached Pi camera module.
    + other blocks show how to read the time, find the machine IP number, etc
- `gpio-PiGlow` - this demo connects the brightness of the PiGlow colour rings to the x,y & heading values of the wildly bouncing sprite.
- `gpio-PiBrella` - press the BigRedButton and the buzzer sounds. Keep pressing it and more leds light up. Uses broadcasts to trigger events, by way of illustration.
- `gpio-PiFace` - there isn’t a lot to do with a PiFace other than turn out outputs when inputs turn on. You can waggle the sliders for each of the outputs to make the relays click.
- `gpio-ExplorerHAT` - currently we can use the inputs, outputs, motors, ADCs and leds. This demo script shows using an input to turn on an output and a cyclic wave of the leds.
    + connect a normally open button to input 1 and 5v
    + connect an led to output 1 and 5v
- `gpio-SenseHAT` - some snippets to show displaying & clearing the LEDs and reading one of the sensor variables.

## Appendix: Enabling and disabling the GPIO server

In normal use you shouldn't need to enable the GPIO server as by default it is enabled but stopped. We can change this by adding  a line to the init file (in the HOME directory we can have a file named `.scratch.ini` - the initial dot is important to make it a hidden unix file)
Simply add a line
`gpioserver=X`
to the file, where X is:
   - `0` - to disable the GPIO server, preventing users or loaded projects from using it.
   - `1` - to enable the GPIO server but leave it turned off; this is the default when there is no .scratch.ini file
   - `2` - to both enable and start the server, perhaps useful in a classroom when the lesson will be about GPIO use

Note that the older mesh/network server setup is currently semi-hidden under the Share menu - you have to hold down the shift key whilst opening that menu.
