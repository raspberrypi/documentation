# Minecraft Pi

Minecraft is a popular sandbox open world-building game. A free version of Minecraft is available for the Raspberry Pi; it is the only edition of the game with a programming interface. This means you can write commands and scripts in Python code to build things in the game, automatically as well as manually.

![Minecraft Pi banner](images/minecraft-pi-banner.png)

## Installation

Currently, Minecraft is not installed by default in Raspbian. To install it, download the files from the web.

Open a terminal window and type the following command:

```bash
wget http://goo.gl/o2aene -O mcpi.tar.gz --no-check-certificate
```

You'll see some information about the downloading file, like so:

![Minecraft Pi downloading](images/mcpi-install.png)

Once you see `'mcpi.tar.gz' saved` and you are returned to the prompt, type the following to extract the files:

```bash
tar xzf mcpi.tar.gz
```

This will create a new directory in your home folder called `mcpi`, which is where the Minecraft installation is stored.

It is safe to delete the `mcpi.tar.gz` file once you have extracted its contents. To do this, enter `rm mcpi.tar.gz`.

## Run

To run Minecraft type:

```bash
cd mcpi
./minecraft-pi
```

When Minecraft Pi has loaded, click on **Start Game**, followed by **Create new**.

You are now in a game of Minecraft! Go walk around, hack things, and build things!

## Programming interface

With Minecraft running, return to your terminal window and open a new tab by clicking **File** and **New Tab**.

In the new tab, navigate to the Python API directory:

```bash
cd ~/mcpi/api/python
```

Now open the Python interpreter by typing `python` and pressing Enter. With the Python interpreter loaded, start by importing the Minecraft library. This is located in the `mcpi/api/python/` directory, which is why you must navigate here to access it.

You can either type commands in Python's interactive mode, or create a file with a list of commands, then execute the file at will. See more about [using Python](../python/README.md).

Next, import the Minecraft library with the following command:

```python
import mcpi.minecraft as minecraft
```

With the library available, you can connect to your game with:

```python
mc = minecraft.Minecraft.create()
```

### Post a message

To post a message to the screen for all players in the game on the network to see, type the following Python command:

```python
mc.postToChat("Type your message here")
```

### Find your location

To find your location, type:

```python
pos = mc.player.getPos()
```

`pos` now contains your location; access each part of the set of coordinates with `pos.x`, `pos.y` and `pos.z`.

Alternatively, a nice way to get the coordinates into separate variables is to use Python's unpacking technique:

```python
x, y, z = mc.player.getPos()
```

Now `x`, `y`, and `z` contain each part of your position coordinates.

### Set blocks

You can set blocks at a given set of coordinates with `mc.setBlock(x, y, z)`:

```python
x, y, z = mc.player.getPos()
mc.setBlock(x + 1, y, z)
```

Now a block should appear beside where you're standing. Note that you should call for your position each time, so you can move about and draw things in different places.

Try this in a loop:

```python
x, y, z = mc.player.getPos()

for dx in range(1, 101):
    for dy in range(1, 101):
        for dz in range(100):
            mc.setBlock(x + dx, y + dy, z + dz)
```

This should draw a 100x100 cube beside you. Try adjusting the ranges to skip every other block:

```python
x, y, z = mc.player.getPos()

for dx in range(1, 101, 2):
    for dy in range(1, 101, 2):
        for dz in range(100, 2):
            mc.setBlock(x + dx, y + dy, z + dz)
```

![Minecraft Pi screenshot](images/steve.png)

## API reference

See an API reference at [stuffaboutcode.com](http://www.stuffaboutcode.com/p/minecraft-api-reference.html).
