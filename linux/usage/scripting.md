# Shell scripts

Commands can be combined together in a file which can then be executed. As an example, copy the following into your favourite text editor:

```bash
while :
do
echo Raspberry Pi!
done
```

Save this with the name `fun-script`. Before you can run it you must first make it executable; this can be done by using the change mode command `chmod`. Each file and directory has its own set of permissions that dictate what a user can and can't do to it. In this case, by running the command `chmod +x fun-script`, the file `fun-script` will now be executable. You can then run it by typing `./fun-script` (assuming that it's in your current directory). This script infinitely loops and prints `Raspberry Pi!`; to stop it, press `Ctrl + C`. This kills any command that's currently being run in the terminal.
