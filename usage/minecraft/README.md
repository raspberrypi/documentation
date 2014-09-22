# Minecraft Pi

Minecraft is a popular sandbox open world-building game. A free version of Minecraft is available for the Raspberry Pi; it is the only edition of the game with a programming interface. This means you can write commands and scripts in Python code to build things in the game, automatically as well as manually.

![Minecraft Pi banner](images/minecraft-pi-banner.png)

## Installation

Minecraft has been installed by default in Raspbian since September 2014.

![Minecraft Pi shortcut icon](images/minecraft-pi-shortcut.png)

If you're using an older version of Raspbian, open a terminal window and type the following commands (you must be online):

```bash
sudo apt-get update
sudo apt-get install minecraft-pi
```

Once that finishes, Minecraft Pi and the Python library should be installed.

## Run

To run Minecraft double click on the desktop icon.

When Minecraft Pi has loaded, click on **Start Game**, followed by **Create new**.

You are now in a game of Minecraft! Go walk around, hack things, and build things!

## Programming interface

With Minecraft running, open IDLE (not IDLE3) and open a new file with `File > New window`. You'll probably want to save this in your home folder or a new project folder.

Start by importing the Minecraft library with the following command:

```python
from mcpi import minecraft
```

With the library available, make a connection to your game with:

```python
mc = minecraft.Minecraft.create()
```

### Post a message

To post a message to the screen for all players in the game on the network to see, type the following Python command:

```python
mc.postToChat("Hello world")
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

You can set blocks at a given set of coordinates with `mc.setBlock()`:

```python
x, y, z = mc.player.getPos()
mc.setBlock(x + 1, y, z, 1)
```

Now a stone block should appear beside where you're standing. The arguments passed the `set block` are `x`, `y`, `z` and `id`. `(x, y, z)` refer to the position in the world (we specified one block away from where the player is standing with `x + 1`) and the `id` refers to the type of block we'd like to place. `1` is stone.

Other blocks you can try:

```
Air:   0
Grass: 2
Dirt:  3
```

Note that `getPos()` returns the location of the player at the time, and if you move position you have to call the function again or use the stored location.

![Minecraft Pi screenshot](images/steve.png)

## API reference

For a more extensive documentation of functions and a full list of block IDs see an API reference at [stuffaboutcode.com](http://www.stuffaboutcode.com/p/minecraft-api-reference.html).

---

Note: Minecraft was previously installed by downloading the files with `wget`. These instructions has been updated as the installation is now possible with Raspbian's package manager.

Previously any Python code accessing the API had to be saved in the `api/python` folder. Now you can save the Python code wherever you like.

If you installed Minecraft the old way, you should delete the folder with `rm -rf mcpi` from the home folder, and follow the instructions above to install the new way.
