# Text editors

On Linux, you have a choice of text editors. Some are easy to use but have limited functionality, others require training to use and a long time to master but offer incredible functionality.

## Desktop graphical editors

### Leafpad

On Raspbian, you'll find an editor called Leafpad. This is a simple editor which opens in a window like a normal application. It allows use of the mouse and keyboard, and has tabs and syntax highlighting.

You can use keyboard shortcuts such as `Ctrl + S` to save a file and `Ctrl + X` to exit.

### IDLE

IDLE is a Python REPL and IDE, so you can write and edit Python code in a window and run it from there.

IDLE has independent windows and syntax highlighting. It's somewhat buggy but generally ok for basic use.

You can use keyboard shortcuts like `Ctrl + S` to save a file, or `Alt + P` (previous command) and `Alt + N` (next command) in the REPL.

Note that IDLE uses Python2 and IDLE 3 uses Python3.

### GVim

See Vim below

## Command line editors

### Nano

GNU Nano is at the easy-to-use end of command line editors. It's installed by default, so use `nano somefile.txt` to edit a file and keyboard shortcuts like `Ctrl + O` to save and `Ctrl + X` to exit.

### Vi

Vi is a very old (c. 1976) command line editor, which is available on most UNIX systems and is preinstalled on Raspbian. It is succeeded by Vim (Vi Improved), which requires installation.

Unlike most editors, Vi and Vim have a number of different modes. When you open Vi with `vi somefile.txt`, you start in command mode which does not (directly) permit entry of text. Press `i` to switch to insert mode in order to edit the file, and type away. To save the file you must return to command mode, so hit the `Escape` key and enter `:w` (followed by `Enter`) which is the command to write the file to disk.

To search for the word 'raspberry' in a file, make sure you're in command mode (press `Escape`), then type `/raspberry` followed by `n` and `N` to flick forward/backward through the results.

To save and exit, enter the command `:wq`. To exit without saving, enter the command `:q!`.

Depending on your keyboard configuration you may find your cursor keys don't work. In this case, you can use the H-J-K-L keys to navigate the file (which move left, down, up, and right respectively) in command mode.

### Vim

Vim is an extension of Vi and works in much the same way, with a number of improvements. Only Vi is installed by default so to get the full features of Vim, install it with APT:

```
sudo apt-get install vim
```

You can edit a file in vim with `vim somefile.txt`. Vim also has a graphical version which opens in a window and allows interaction with the mouse. This version is installable separately:

```
sudo apt-get install vim-gnome
```

To use the graphical version of vim, use `gvim somefile.txt`. You can save configuration in a `.vimrc` file in your user's home directory. To learn more about editing in Vi and Vim, you can run `vimtutor` and follow the tutorial.

### Emacs

GNU Emacs is the GNU flavour of command line text editors; it is powerful, extensible, and customisable. You can install it with APT:

```
sudo apt-get install emacs
```

Use keyboard combination commands such as `Ctrl + X Ctrl + S` to save and `Ctrl + X Ctrl + C` to close.
