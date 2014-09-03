# Python Games

On the Raspbian desktop you'll find an icon with the Python logo labelled `Python Games`:

![Python Games icon](images/python-games-icon.png)

Double click this icon to start. This will prompt you to set your audio configuration to output sound over HDMI or the headphone jack. Make a selection or leave it as it is and click `OK` to proceed.

![Audio configuration](images/audio-output.png)

Now you'll be shown a tall window with the list of games available:

![Python Games selection screen](images/python-games-selection.png)

Pick a game, click it and hit `OK` to play.

## Examples

### Four in a Row

![Four in a Row](images/four-in-a-row.png)

### Flippy

![Flippy](images/flippy.png)

## Game source code

The source of each of these games is available on the Pi. Simply navigate to the directory `/home/pi/python_games` in a terminal or the file manager and you'll see the assets and source code.

The `python_games` directory listing in a terminal window:

![Python Games in a terminal](images/python-games-terminal.png)

The `python_games` folder contents in a the file manager window:

![Python Games in File Manager](images/python-games-folder.png)

The Python source code for the *Four in a Row* game, open for editing in `IDLE`.

![Four in a Row source code](images/four-in-a-row-code.png)

### Hack the game

You can edit the source of these games. Why not make a copy of a Python file, look through the code and change some numbers? See what happens.

If you can figure out how the game works, try to hack it to make it better, make it harder (or easier) to win, or add some features to the game! You could add [GPIO](../gpio/README.md) interaction so lights flash when you win, or add input buttons.
