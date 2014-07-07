# Attaching a Raspberry Pi Camera to the Compute Module IO Board

The 15-way 1mm FFC camera connector on the Raspberry Pi model A and B is attached to the CAM1 interface (though only uses 2 of the 4 available lanes).

The Compute Module IO Board has a 22-way 0.5mm FFC for each camera port, with CAM0 being a 2-lane interface and CAM1 being the full 4-lane interface.

To attach a standard Raspberry Pi Camera to the Compute module IO Board a small adaptor board is available that adapts the 22W FFC to the Pi 15W FFC.

To make the Raspberry Pi Camera work with a standard Raspian OS the same GPIOs and I2C interface that are used on the Raspberry Pi must be wired to the CAM1 connector. This is done by bridging the correct GPIOs from the J6 GPIO connector to the CD1_SDA/SCL and CAM1_IO0/1 pins on the J5 connector using jumper wires.

## Steps to attach a Raspberry Pi Camera (to CAM1)

1.  Attach the 0.5mm 22W FFC flexi (included with the adaptor board) to the CAM1 connector (flex contacts face down).
2.  Attach the camera adaptor board to the other end of the 0.5mm flex (flex contacts face down).
3.  Attach a Raspberry Pi Camera to the other, larger 15W 1mm FFC on the camera adaptor board (**contacts on the Raspberry Pi Camera flex must face up**).
4.  Attach CD1_SDA (J6 pin 37) to GPIO0 (J5 pin 1).
5.  Attach CD1_SCL (J6 pin 39) to GPIO1 (J5 pin 3).
6.  Attach CAM1_IO1 (J6 pin 41) to GPIO5 (J5 pin 11).
7.  Attach CAM1_IO0 (J6 pin 43) to GPIO 21 (J5 pin 43).

The camera should now work in exactly the same way as a Raspberry Pi Model A/B.

## How to attach 2 cameras

Attaching a second camera is a repeat of the above steps 1-3 for the second (CAM0) connector.

The difference is that the second I2C interface must be used for CD0_SDA and CD0_SCL (you can't put both cameras on the same I2C bus as they have the same address) as well as 2 different GPIOs for CAM0_IO0 and CAM0_IO1.

**TODO**


