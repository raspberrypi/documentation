# My official Raspberry Pi camera isn't working

The camera has a number of failure modes, so this guide will try and narrow down what the problem might be. 

- [I've plugged it in what do I do next?](#ive-plugged-it-in-what-do-i-do-next)
- [I get an error message when I run `raspistill`](#i-get-an-error-message-when-i-run-raspistill)
- [Images are blurred!](#images-are_blurred)
- [Colours are a bit off](#colours-are-a-bit-off)

## I've plugged it in what do I do next?

Try running the example camera application, by typing `raspistill -o test.jpg` on the command line. If everything is installed correctly and enabled, a preview will appear on the display, and after 5 seconds (the default value), a picture will be taken and stored in the file `test.jpg`.


## I get an error message when I run `raspistill`

Which error message? Check out the last line of the error report and read the relevent section below.

#### mmal: Camera is not enabled in this build ....

The camera has not been enabled in the software. You need to run `sudo raspi-config` from the command line, or select the ```Preferences/Raspberry Pi Configuration``` option from the desktop menu.

For raspi-config, now select Interfacing Options, then select the Enable Camera option.  
For the graphical interface, select the Interfaces tab and enable the camera.

You will need to reboot for the changes to take effect. 

#### mmal: Camera is not detected...

Although the camera has been enabled, the software has not been able to find one connected to the Raspberry Pi. This can be cause by a number of things, but the usual reason is the camera has not been connected correctly.

Turn the power off, then check both ends of the camera cable to ensure they are the right way round and correct installed. Also, check the small connector on the PCB that connects to the camera module itself. Sometimes these can come loose. You can lever it up with your fingernail, then re-seat it, it should click in to place.

## Images are blurred!

This could be a couple of things, firstly, have you removed the packaging film from the front of the sensor!

Alternatively, occasionally the cameras leave the factory slightly out of focus, or with a focus length that is not suitable for the job in hand. You can adjust the camera focus by rotating the lens. Be careful, as they are fixed with three tiny blobs of glue that need to be cracked. Depending on the supplier, the camera may have come with a tool to help with this.

## Colours are a bit off

Are you using a Pi NoIR camera in daylight? This can produce oddly coloured images. 

Lighting conditions can affect how well balanced the colours are. The Raspberry Pi camera software uses a system called Automatic White Balance, AWB. This system uses a Baysian algorithm to try and determine what the scene being viewed is, and tries to make things that are white, actually look white in the final image. However, this is not an exact science, and sometimes the colours can be balanced incorrectly. Scenes with large amounts of gray for example can cause the system to get confused. Improving the lighting conditions can help, or bypassing the AWB by setting a specific colour balance.






