# THIS PAGE IS NOW DEPRECATED

# Demo programs

Here are some example programs to demonstrate the Pi's capabilities. Note that not all the demo applications will run on a Pi 4 due to the way the new 3D libraries work; the non-working ones will report an error message if run on a Pi 4. 

![Mandelbrot fractal](images/mandelbrot.jpg)

In order to run these programs you need to be at the command line. Your Pi may boot to the command line (requiring you to enter `startx` to get to the desktop); if so, go straight ahead. Otherwise, use the start button to log out of the desktop.

```bash
pi@raspberrypi ~ $
```

This (above) is the command prompt. It looks difficult to use, but try not to be afraid of it! A CLI or command line interface is actually a very quick and efficient way to use a computer.

To start, navigate to the `hello_pi` folder where all the demos are stored. Enter the command below to do this. **TIP**: You can use the `TAB` key for auto-complete as you enter commands.

```bash
cd /opt/vc/src/hello_pi
```

The command prompt should now look like the text below. The blue part shows where you are in the file system of the Pi.

```bash
pi@raspberrypi /opt/vc/src/hello_pi $
```

If you enter `ls` and press Enter, you’ll see a list of folders; there is one for each demo. Before you can run them, though, they must be compiled. Don’t worry if you don’t understand what this is or why you need to do it; just follow the instructions for now, and we'll learn more about it later on.

There is a small shell script supplied in the `hello_pi` folder called rebuild.sh which will do the compiling for you. Enter the following command to run it; ignore the gobbledygook for now!

```bash
./rebuild.sh
```

A lot of text will scroll up the screen now, but for this exercise you can ignore it. It is just the output of the compiler as it works through the demo code. Wait for the command prompt to return before you continue.

Now we’re finally ready to run some demos!

Demo programs:

- [Hello world](hello-world.md)
- [Hello video](hello-video.md)
- [Hello triangle](hello-triangle.md) (not Pi 4)
- [Hello fractal](hello-fractal.md)
- [Hello teapot](hello-teapot.md) (not Pi 4)
- [Hello audio](hello-audio.md)

Try more demos in the `hello_pi` folder!
