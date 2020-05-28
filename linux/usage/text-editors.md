# Text editors

On Linux, you have a choice of text editors. Some are easy-to-use but have limited functionality; others require training to use and take a long time to master, but offer incredible functionality.

## Desktop graphical editors

### Text Editor

When using Raspberry Pi OS Desktop, in the accessories menu there is an option to run a Text Editor. This is a simple editor which opens in a window like a normal application. It allows use of the mouse and keyboard, and has tabs and syntax highlighting.

You can use keyboard shortcuts, such as `Ctrl + S` to save a file and `Ctrl + X` to exit.

### Thonny

Thonny is a Python REPL and IDE, so you can write and edit Python code in a window and run it from there.

Thonny has independent windows and syntax highlighting, and uses Python 3

### GVim

See Vim below.

### Geany

A fast and lightweight IDE, supporting many different file types, including C/C++ and Python. Installed by default on Raspberry Pi OS.

## Command-line editors

### Nano

GNU Nano is at the easy-to-use end of command-line editors. It's installed by default, so use `nano somefile.txt` to edit a file, and keyboard shortcuts like `Ctrl + O` to save and `Ctrl + X` to exit.

### Vi

Vi is a very old (c. 1976) command-line editor, which is available on most UNIX systems and is pre-installed on Raspberry Pi OS. It's succeeded by Vim (Vi Improved), which requires installation.

Unlike most editors, Vi and Vim have a number of different modes. When you open Vi with `vi somefile.txt`, you start in command mode which doesn't directly permit text entry. Press `i` to switch to insert mode in order to edit the file, and type away. To save the file you must return to command mode, so press the `Escape` key and enter `:w` (followed by `Enter`), which is the command to write the file to disk.

To search for the word 'raspberry' in a file, make sure you're in command mode (press `Escape`), then type `/raspberry` followed by `n` and `N` to flick forwards/backwards through the results.

To save and exit, enter the command `:wq`. To exit without saving, enter the command `:q!`.

Depending on your keyboard configuration, you may find your cursor keys don't work. In this case, you can use the H-J-K-L keys (which move left, down, up, and right respectively) to navigate the file in command mode.

### Vim

Vim is an extension of Vi and works in much the same way, with a number of improvements. Only Vi is installed by default so to get the full features of Vim, install it with APT:

```
sudo apt install vim
```

You can edit a file in Vim with `vim somefile.txt`. Vim also has a graphical version which opens in a window and allows interaction with the mouse. This version is installable separately:

```
sudo apt install vim-gnome
```

To use the graphical version of Vim, use `gvim somefile.txt`. You can save configuration in a `.vimrc` file in your user's home directory. To learn more about editing in Vi and Vim, you can run `vimtutor` and follow the tutorial.

### Emacs

Emacs is a GNU command-line text editor; it's powerful, extensible, and customisable. You can install it with APT:

```
sudo apt install emacs
```

You can use keyboard combination commands, such as `Ctrl + X Ctrl + S` to save and `Ctrl + X Ctrl + C` to close.
