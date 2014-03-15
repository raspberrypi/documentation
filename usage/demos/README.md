# Demo Programs

Here are some example programs to demonstrate the Pi's capabilities.

In order to run these programs you need to be at the command line. Your Pi may boot to the command line (requiring you to enter `startx` to get to the Desktop) - if so, go straight ahead. Otherwise, use the start button to logout of the Desktop.

```
pi@raspberrypi ~ $
```

This (above) is the command prompt, try not to be afraid of it. A CLI (command line interface) is actually a very quick and efficient way to use a computer.

Firstly navigate to the `hello_pi` folder where all the demos are stored. Enter the command below to do this.

TIP: You can use the TAB key to auto-complete commands to save typing them in full.

```
cd /opt/vc/src/hello_pi
```

The command prompt should now look like this, the blue part shows where you are in the file system of the Pi.

```
pi@raspberrypi /opt/vc/src/hello_pi $
```

If you enter `ls` and press enter you'll see a list of folders. One for each demo. Before you can run them though they must be compiled. Don't worry if you don't understand why you need to do this, just take it on faith for now.

There is a small shell script supplied in the `hello_pi` folder called `rebuild.sh` which will do the compile for you, enter the following command to run it. Ignore the Gobbledygook for now!

```
./rebuild.sh
```

A lot of text will scroll up the screen now, you can ignore it. It is just the output of the compiler as it works through the demo code. Wait for the command prompt to return before you continue.

Demo programs:

- [Hello world](hello-world.md)
- [Hello video](hello-video.md)
- [Hello triangle](hello-triangle.md)
- [Hello triangle 2](hello-triangle2.md)
- [Hello teapot](hello-teapot.md)
- [Hello audio](hello-audio.md)

Try more demos in the `hello_pi` folder!
