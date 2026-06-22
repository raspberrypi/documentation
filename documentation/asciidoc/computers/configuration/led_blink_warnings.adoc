== LED behaviour
On-board LEDs on Raspberry Pi devices provide a simple way to monitor system status and diagnose issues. Depending on the model, these LEDs indicate power state, SD card activity, and fault conditions, with some offering additional configurability for custom use.

[[prerequisite-led]]
=== Prerequisite information

Different Raspberry Pi models use different LED hardware configurations, and their exact behaviour and configurability differs accordingly.

The following table provides a high-level summary of power and activity LEDs, organised by Raspberry Pi model. Raspberry Pi 400 and 500 have two additional LEDs, described in more detail after this table.

[[power-leds]]
.Power and activity LEDs by Raspberry Pi model
[cols="1,1,1,1",options="header"]
|===
| Models
| LED count
| LED colours
| MicroSD card activity indication


| Raspberry Pi 1, 2, 3, and 4
| 2 (1 power LED and 1 activity LED)
| Red and green
| Green LED flashes during activity

| Raspberry Pi Zero series
| 1
| Green
| LED flashes off during activity

| Raspberry Pi 400
| 1
| Green
| No activity indication

| Raspberry Pi 5, 500, 500+
| 1 bi-colour power and activity LED
| Red or green depending on activity
| Green LED flashes off during microSD activity

|===

==== Raspberry Pi 1, 2, 3, and 4 LEDs

Raspberry Pi 1, 2, 3, and 4 use two distinct LEDs:

* Red for power (`PWR`), indicating normal operation with a stable 5 V power supply. The red LED is off or flickering when there is undervoltage.
* Green for microSD card activity (`ACT`), indicating no storage activity when off and microSD card access in progress when flashing.

When shutting down one of these Raspberry Pi models, the green activity LED briefly displays a series of short flashes to indicate that it's now safe to remove the USB PSU cable.

==== Raspberry Pi Zero LEDs

Raspberry Pi Zero, Zero W, and Zero 2 W use one green LED, which represents both power and microSD card activity. You can configure the LED to either:

** Flash off briefly when there is microSD card activity. This is the default behaviour.
** Remain lit when the board is powered on regardless of microSD card activity.

For instructions, see <<led-zero>>.

==== Raspberry Pi 400 LEDs

Raspberry Pi 400 has a single green power LED alongside two keyboard-specific indicator lights in the following order:

* A num-lock LED, indicated on the keyboard with the number *1* inside a square.
* A caps-lock LED, indicated on the keyboard with the capital letter *A* inside a square.
* A power LED (described in <<power-leds>>), indicated on the keyboard with a power symbol. This LED illuminates when power is applied and remains lit while the system is powered on. After the system has been shut down, all LEDs turn off.

For more detailed information about Raspberry Pi 400, see xref:keyboard-computers.adoc[Keyboard computers].

==== Raspberry Pi 500 LEDs

Raspberry Pi 500 uses a bi-colour (red and green) LED located above and to the left of the power key to indicate power and activity. It is located alongside two other indicator lights in the following order:

* A user-programmable LED, indicated on the keyboard with an icon consisting of a circle, square, and triangle. Its function isn't hardwired to system events, which means you can use the LED as a status light for your custom projects, for example, notification alerts and process indicators. For instructions, see <<led-keyboard>>.
* A caps-lock LED, indicated on the keyboard with the capital letter *A* inside a square.
* A bi-colour power LED (described in <<power-leds>>), indicated on the keyboard with a power symbol. This LED:
    ** Illuminates red when power is first applied.
    ** Changes to green as firmware startup progresses.
    ** Remains green while the system is running.
    ** Flashes off to indicate storage activity when booting from the microSD card.

After the operating system has been shut down, the LED changes to red to indicate the low-power standby state.

NOTE: The power key on Raspberry Pi 500 allows the computer to enter a soft-off state. In this state, the CPU and most system activity stops, but the power rails remain active and the system can be restarted by pressing the power key again, or by removing and restoring power as normal.

For more detailed information about Raspberry Pi 500, see xref:keyboard-computers.adoc[Keyboard computers].

==== Raspberry Pi 5 and 500+ LEDs

Raspberry Pi 5 and 500+ use a bi-colour (red and green) LED to indicate power and activity.

On Raspberry Pi 5, the power LED is located next to the power button; if assembled into a Raspberry Pi 5 case, the power button and LED appear integrated behind a single pressable lens.

On Raspberry Pi 500+, the power LED is located underneath the power key.

On both Raspberry Pi 5 and 500+, the bi-colour power LED (described in <<power-leds>>):

    ** Illuminates red when power is first applied.
    ** Changes to green as firmware startup progresses.
    ** Remains green while the system is running.
    ** Flashes off to indicate microSD card activity. It doesn't flash if you're booting from the internal SSD on a Raspberry Pi 500+, or from an SSD on an M.2 HAT+ on a Raspberry Pi 5.

After the operating system has been shut down, the LED changes to red to indicate the low-power standby state.

NOTE: The power button on Raspberry Pi 5 and the power key on Raspberry Pi 500+ allows the computer to enter a soft-off state. In this state, the CPU and most system activity stops, but the power rails remain active and the system can be restarted by pressing the power button or key again, or by removing and restoring power as normal.

For more detailed information about Raspberry Pi 500+, see xref:keyboard-computers.adoc[Keyboard computers].

[[led-zero]]
=== Change LED behaviour on Raspberry Pi Zero
Raspberry Pi Zero, Zero W, and Zero 2 W have a single power LED for indicating power and storage activity.

You can use the interactive `raspi-config` TUI to change the behaviour of the power LED on your Raspberry Pi Zero, Zero W, or Zero 2 W:

. Open the Terminal and run `sudo raspi-config`.
. Use the keyboard to navigate to and select `1 System Options > S8 Power LED`.
. Select `Yes` or `No` in response to the question *Would you like the power LED to flash during disk activity?*
** Selecting `Yes` configures the LED to flash when there's storage activity.
** Selecting `No` keeps the LED lit when the board is powered on.
. Select `<OK>` to confirm this choice and then `<Finish>` when you're done.

[[led-keyboard]]
=== Configure Raspberry Pi 500 LEDs

The user-configurable LED on Raspberry Pi 500 can be controlled through the `pinctrl` tool, which is used to interact with GPIO pins and peripherals.

* `pinctrl USER_LED op dh` turns the user LED on.
* `pinctrl USER_LED op dl` turns the user LED off.

You can also use Python to call `pinctrl`:

[source,python]
----
import subprocess
from time import sleep

while True:
    subprocess.run(['pinctrl', 'USER_LED', 'op', 'dh'])
    print("On")
    sleep(1)
    subprocess.run(['pinctrl', 'USER_LED', 'op', 'dl'])
    print("Off")
    sleep(1)
----

[[led-warning-flash-codes]]
=== Check LED warning codes
If a Raspberry Pi device fails to boot or shuts down unexpectedly, the on-board LED often provides a diagnostic signal in the form of a specific flashing pattern. Long flashes always occur before short ones that indicate the exact issue; sometimes there are no long flashes at all. In most cases, the pattern repeats after a two-second pause.


[cols="1,1,4",options="header"]
|===
| Long flashes | Short flashes | Status

| 0
| 3
| Generic failure to boot

| 0
| 4
| `start*.elf` not found

| 0
| 7
| Kernel image not found

| 0
| 8
| SDRAM failure

| 0
| 9
| Insufficient SDRAM

| 0
| 10
| In HALT state

| 1
| 2
| SD card overcurrent detected

| 2
| 1
| Partition not FAT

| 2
| 2
| Failed to read from partition

| 2
| 3
| Extended partition not FAT

| 2
| 4
| File signature/hash mismatch (Raspberry Pi 4 and 5)

| 3
| 1
| SPI EEPROM error (Raspberry Pi 4 and 5)

| 3
| 2
| SPI EEPROM is write protected (Raspberry Pi 4 and 5)

| 3
| 3
| I2C error (Raspberry Pi 4 and 5)

| 3
| 4
| Secure-boot configuration isn't valid

| 4
| 3
| RP1 not found

| 4
| 4
| Unsupported board type

| 4
| 5
| Fatal firmware error

| 4
| 6
| Power failure type A

| 4
| 7
| Power failure type B
|===
