# Industrial use of the Raspberry Pi

The Raspberry Pi is often used as part of another product. This documentation describes some extra facilities available to use other capabilities of the Pi.

## Customer OTP settings

There are a number of OTP values that can be used. To see a list of all the [OTP values](../raspberrypi/otpbits.md), you can use:

```
pi@raspberrypi:~ $ vcgencmd otp_dump
```

Some interesting lines from this dump are:

* 28 - Serial number
* 29 - Ones complement of serial number
* 30 - Revision number

Also, from 36 to 43 (inclusive), there are eight rows of 32 bits available for the customer

To program these bits, you will need to use the vcmailbox. This is a Linux driver interface to the firmware which will handle the programming of the rows. To do this, please refer to the documentation [here](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface), and the vcmailbox example application [here](https://github.com/raspberrypi/userland/blob/master/host_applications/linux/apps/vcmailbox/vcmailbox.c).

The vcmailbox application can be used directly from the command line on a Raspberry Pi Raspberry Pi OS build. An example usage would be:

```
pi@raspberrypi:~ $ /opt/vc/bin/vcmailbox 0x00010004 8 8 0 0
0x00000020 0x80000000 0x00010004 0x00000008 0x800000008 0xnnnnnnnn 0x00000000 0x00000000
```

The above uses the [mailbox property interface](https://github.com/raspberrypi/firmware/wiki/Mailbox-property-interface) `GET_BOARD_SERIAL` with a request size of 8 bytes and response size of 8 bytes (sending two integers for the request 0, 0). The response to this will be two integers (0x00000020 and 0x80000000) followed by the tag code, the request length, the response length (with the 31st bit set to indicate that it is a response) then the 64 bit serial number (where the MS 32bits are always 0).

To set the customer OTP values you will need to use the `SET_CUSTOMER_OTP` (0x38021) tag as follows:
```
pi@raspberrypi:~ $ /opt/vc/bin/vcmailbox 0x00038021 [8 + number * 4] [8 + number * 4] [start_num] [number] [value] [value] [value] ...
```

- `start_num` = the first row to program from 0-7
- `number` = number of rows to program
- `value` = each value to program

So, to program OTP customer rows 4, 5, and 6 to 0x11111111, 0x22222222, 0x33333333 respectively, you would use:

```
pi@raspberrypi:~ $ /opt/vc/bin/vcmailbox 0x00038021 20 20 4 3 0x11111111 0x22222222 0x33333333
```

This will then program rows 40, 41, and 42.

To read the values back, you can use:

```
pi@raspberrypi:~ $ /opt/vc/bin/vcmailbox 0x00030021 20 20 4 3 0 0 0
0x0000002c 0x80000000 0x00030021 0x00000014 0x80000014 0x00000000 0x00000003 0x11111111 0x22222222 0x33333333
```

If you'd like to integrate this functionality into your own code, you should be able to achieve this by using the vcmailbox.c code as an example.

## Locking the OTP changes

It is possible to lock the OTP changes to avoid them being edited again. This can be done using a special argument with the OTP write mailbox:

```
pi@raspberrypi:~ $ /opt/vc/bin/vcmailbox 0x00038021 8 8 0xffffffff 0xaffe0000
```

Once locked, the customer OTP values can no longer be altered. Note that this locking operation is irreversible.

## Making Customer OTP bits unreadable

It is possible to prevent the customer OTP bits from being read at all. This can be done using a special argument with the OTP write mailbox:

```
pi@raspberrypi:~ $ /opt/vc/bin/vcmailbox 0x00038021 8 8 0xffffffff 0xaffebabe
```

 This operation is unlikely to be useful for the vast majority of users, and is irreversible.
