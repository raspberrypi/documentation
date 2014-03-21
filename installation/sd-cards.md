# SD Cards

The Raspberry Pi should be able to work with any SD compatible cards, although there are some guidelines
that should be followed:

* SD card size.  For installation of NOOBS the minimum card size is recommended as 8GB.  For image installations we recommend minimum 4GB although some distributions can run on much smaller cards (OpenElec and Arch specifically)
* SD card class.  The card class determines the sustained write speed for the card, a class 4 card will be able to write at 4MB/s whereas a class 10 should be able to attain 10 MB/s.  But it should be noted this does not mean a class 10 card will outperform a class 4 card for general usage because often this write speed is achieved at the cost of read speed and increased seek times.

Our recommendation is to buy the Raspberry Pi SD card, this is an 8GB class 6 SD card that outperforms almost all of the other SD cards on the market!  It is also the cheapest SD card solution since we've made that possible for you!

If you are having trouble with corruption of your SD cards make sure you follow these steps:

1. Make sure you are using a genuine SD card.  There are many SD cards that can be bought very cheaply that are actually smaller than advertised or will not last very long!
2. Make sure you are using a good quality power supply.  You can check your power supply by measuring the voltage between TP1 and TP2 on the Raspberry Pi, if this drops below 4.75V when doing hard tasks then all bets are off!
3. Make sure you are using a good quality USB cable for the power.  Often people complain that they are using a high quality power supply but the TP1->TP2 voltage drops below 4.75V.  This is generally due to the resistance of the wires in the USB power cable, to save money USB cables have a little copper in them as possible and you can easily drop as much as 1V over the length of the cable (that's as much as a watt lost in the cable!)
4. Make sure you are properly shutting down your Raspberry Pi before powering off. Type ```sudo halt``` and wait for the Pi to signal it is ready to be powered off by flashing the activity LED.
5. Finally if you are overclocking the Pi corruption has been seen...  This problem has previously been fixed although the workaround used may mean that it can still happen we'd be very interested to know after checking all the above you are still getting corruption.

