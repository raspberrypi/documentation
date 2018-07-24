## OTP Register and bit definitions

All SoC's used by the Raspberry Pi range have a inbuilt One Time Programmable (OTP) memory block. 

It is 66 32 bit values long, although only a few locations have factory programmed data.

There is a vcgencmd to display the contects of the OTP

```vcgencmd otp_dump```

### OTP Registers

This list contains publicly available information on the registers. If a register or bit is not defined here, then it is not public.

17 The bootmode register
   - Bit 1 sets the oscillator frequency to 19.2MHz
   - Bit 3 enables pull ups on the SDIO pins
   - Bit 19 enabled GPIO bootmode
   - Bit 20 sets the bank to check for GPIO bootmode
   - Bit 21 enabled booting from SD card
   - Bit 22 sets the bank to boot from
   - Bit 28 enables USB device booting
   - Bit 29 enables USB host booting (ethernet and mass storage)

18 - Copy of bootmode register   
28 - Serial Number   
29 - ~(Serial Number)   
30 - Revision Number   
64/65 - MAC address. System will use this, if set, in preference to the automatically generated address based on the serial number.   
66 - Advanced boot register
   - Bits 0-6: gpio for ETH CLK output pin
   - Bit 7: enable ETH_CLK output
   - Bits 8-14: gpio for LAN_RUN output pin
   - Bit 15: enable LAN_RUN output
   - Bit 24: Extend USB HUB timeout parameter
   - Bit 25: ETH_CLK frequency:
      - 0 - 25MHz
      - 1 - 24MHz  
