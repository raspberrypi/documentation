# USB Issues

USB ports on all RPis (including Model B+) is unable to source sufficient current for powerful USB devices, such as WiFi doungles. Using external hub lowering advantages of 4-ports Model B+. The simple solution is delivering +5V to powerful devices bypassing Pi.

```
                   +-----------------------+
-----------+       |      +-----------+    |
           |-(+5V)-+   x--|           |    |
 500 mA    |-( D-)--------|    RPi    |----*--(+5V)
USB device |-( D+)--------|           |-------(GND)
           |-(GND)--------|           |
-----------+              +-----------+

```
