## OTP register and bit definitions

All SoCs used by the Raspberry Pi range have a inbuilt One-Time Programmable (OTP) memory block. 

It is 66 32-bit values long, although only a few locations have factory-programmed data.

The `vcgencmd` to display the contents of the OTP is:

```vcgencmd otp_dump```

### OTP registers

This list contains the publicly available information on the registers. If a register or bit is not defined here, then it is not public.

17 – bootmode register
   - Bit 1: sets the oscillator frequency to 19.2MHz
   - Bit 3: enables pull ups on the SDIO pins
   - Bit 19: enables GPIO bootmode
   - Bit 20: sets the bank to check for GPIO bootmode
   - Bit 21: enables booting from SD card
   - Bit 22: sets the bank to boot from
   - Bit 28: enables USB device booting
   - Bit 29: enables USB host booting (ethernet and mass storage)

18 – copy of bootmode register   
28 – serial number   
29 – ~(serial number)   
30 – [revision code](./revision-codes/README.md)<sup>1</sup>   
36-43 - [customer OTP values](../industrial/README.md)   
45 - MPG2 decode key   
46 - WVC1 decode key   
64/65 – MAC address; if set, system will use this in preference to the automatically generated address based on the serial number    
66 – advanced boot register
   - Bits 0-6: GPIO for ETH_CLK output pin
   - Bit 7: enables ETH_CLK output
   - Bits 8-14: GPIO for LAN_RUN output pin
   - Bit 15: enables LAN_RUN output
   - Bit 24: extends USB HUB timeout parameter
   - Bit 25: ETH_CLK frequency:
      - 0 - 25MHz
      - 1 - 24MHz  

<sup>1</sup>Also contains bits to disable overvoltage, OTP programming, and OTP reading.
