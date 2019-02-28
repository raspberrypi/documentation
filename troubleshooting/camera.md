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

### mmal: Camera is not enabled in this build ....

The camera has not been enabled in the software. You need to run `sudo raspi-config` on from the command line, or select the Preferences/Raspberry Pi Configuration option from the desktop menu.

For raspi-config, now selcect Interfacing Options, then select the Enable Camera option.
For the graphical interface, select the interfaces tab and enable the camera.

### mmal: Camera is not detected...

Although the camera has been enabled, the software has not been able to find one connected to the Raspberry Pi. This can be cause by a number of things, but the usual reason is the camera has not been connected correctly.

Check both ends of the camera cable to ensure they are the right way rounbd and correct installed. Also, check the small connected on the PCB that connects to the camera module itself. Sometimes these can come loose. You can lever it up, then re-seat it, with a slight click.

## Images are blurred!

This could be a couple of things, firstly, have you removed the packaging film from the front of the sensor!

Alternatively, occasionally the cameras leave the factory slightly out of focus, or with a focus length that is not suitable for the job in hand. You can adjust the camera focus by rotating the lens. Be careful, as they are fixed with three tiny blobs of glue that need to be cracked. Depending on the supplier, the camera may have come with a tool to help with this.

## Colours are a bit off

Are you using a Pi NoIR camera in daylight? This can produce oddly coloured images. 






