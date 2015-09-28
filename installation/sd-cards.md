# SD Cards

The Raspberry Pi should work with any SD-compatible cards, although there are some guidelines that should be followed:

- SD card size (capacity). For installation of NOOBS, the minimum recommended card size is 8GB. For image installations we recommend a minimum of 4GB; some distributions can run on much smaller cards, specifically OpenElec and Arch.
- SD card class. The card class determines the sustained write speed for the card; a class 4 card will be able to write at 4MB/s, whereas a class 10 should be able to attain 10 MB/s. However it should be noted that this does not mean a class 10 card will outperform a class 4 card for general usage, because often this write speed is achieved at the cost of read speed and increased seek times.
- SD card physical size. The original [Raspberry Pi Model A](https://www.raspberrypi.org/products/model-a/) and [Raspberry Pi Model B](https://www.raspberrypi.org/products/model-b/) require full-size SD cards. The newer [Raspberry Pi Model A+](https://www.raspberrypi.org/products/model-a-plus/), [Raspberry Pi Model B+](https://www.raspberrypi.org/products/model-b-plus/) and [Raspberry Pi 2 Model B](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/) require micro-SD cards.

We recommend buying the [Raspberry Pi SD card](http://swag.raspberrypi.org/products/noobs-8gb-sd-card); this is an 8GB class 6 microSD card (with a full-size SD adaptor) that outperforms almost all other SD cards on the market and is a good value solution.

If you are having trouble with corruption of your SD cards, make sure you follow these steps:

1. Make sure you are using a genuine SD card. There are many cheap SD cards available that are actually smaller than advertised or will not last very long.
2. Make sure you are using a good quality power supply. You can check your power supply by measuring the voltage between TP1 and TP2 on the Raspberry Pi; if this drops below 4.75V when doing complex tasks then it is most likely unsuitable.
3. Make sure you are using a good quality USB cable for the power supply. When using a high quality power supply, the TP1->TP2 voltage can drop below 4.75V. This is generally due to the resistance of the wires in the USB power cable; to save money USB cables have as little copper in them as possible, and as much as 1V (or one watt) can be lost over the length of the cable.
4. Make sure you are properly shutting down your Raspberry Pi before powering it off. Type `sudo halt` and wait for the Pi to signal it is ready to be powered off by flashing the activity LED.
5. Finally, corruption has been observed if you are overclocking the Pi. This problem has previously been fixed, although the workaround used may mean that it can still happen. If after checking the steps above you are still having problems with corruption, please let us know.
