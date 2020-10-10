# SD cards

The Raspberry Pi should work with any compatible SD card, although there are some guidelines that should be followed:

## SD card size (capacity) 

For installation of Raspberry Pi OS with desktop and recommended software (Full) via NOOBS the minimum card size is 16GB. For the image installation of Raspberry Pi OS with desktop and recommended software, the minimum card size is 8GB. For Raspberry Pi OS Lite image installations we recommend a minimum of 4GB. Some distributions, for example LibreELEC and Arch, can run on much smaller cards. If you're planning to use a card of 64GB or more with NOOBS, see [this page](sdxc_formatting.md) first.

**Note:** Because of a constraint in versions of SoC's used in the Raspberry Pi Zero, 1 and 2, the SD card partition size limit is 256GB. From the Raspberry Pi 3 onwards this limitation does not apply. 

## SD card class

The card class determines the sustained write speed for the card; a class 4 card will be able to write at 4MB/s, whereas a class 10 should be able to attain 10 MB/s. However, it should be noted that this does not mean a class 10 card will outperform a class 4 card for general usage, because often this write speed is achieved at the cost of read speed and increased seek times.

## SD card physical size

The original Raspberry Pi Model A and Raspberry Pi Model B require full-size SD cards. From the Model B+ (2014) onwards, a micro SD card is required.

## Troubleshooting

We recommend buying the Raspberry Pi SD card which is available [here](https://shop.pimoroni.com/products/noobs-8gb-sd-card), as well as from other retailers; this is an 8GB class 6 micro SD card (with a full-size SD adapter) that outperforms almost all other SD cards on the market and is a good value solution.

If you are having trouble with corruption of your SD cards, make sure you follow these steps:

1. Make sure you are using a genuine SD card. There are many cheap SD cards available which are actually smaller than advertised or which will not last very long.
2. Make sure you are using a good quality power supply. You can check your power supply by measuring the voltage between TP1 and TP2 on the Raspberry Pi; if this drops below 4.75V when doing complex tasks then it is most likely unsuitable.
3. Make sure you are using a good quality USB cable for the power supply. When using a lower quality power supply, the TP1->TP2 voltage can drop below 4.75V. This is generally due to the resistance of the wires in the USB power cable; to save money, USB cables have as little copper in them as possible, and as much as 1V (or 1W) can be lost over the length of the cable.
4. Make sure you are shutting your Raspberry Pi down properly before powering it off. Type `sudo halt` and wait for the Pi to signal it is ready to be powered off by flashing the activity LED.
5. Finally, corruption has been observed if you are overclocking the Pi. This problem has been fixed previously, although the workaround used may mean that it can still happen. If after checking the steps above you are still having problems with corruption, please let us know.
