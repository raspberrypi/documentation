# SCP (Secure Copy)

`scp` is a command for sending files over SSH. This means you can copy files between computers, say from your Raspberry Pi to your desktop or laptop, or vice-versa.

First of all, you'll need to know your Raspberry Pi's [IP address](../ip-address.md).

## Copying files to your Raspberry Pi

Copy the file `myfile.txt` from your computer to the `pi` user's home folder of your Raspberry Pi at the IP address `192.168.1.3` with the following command:

```bash
scp myfile.txt pi@192.168.1.3:
```

Copy the file to the `/home/pi/project/` directory on your Raspberry Pi (the `project` folder must already exist):

```bash
scp myfile.txt pi@192.168.1.3:project/
```

## Copying files from your Raspberry Pi

Copy the file `myfile.txt` from your Raspberry Pi to the current directory on your other computer:

```bash
scp pi@192.168.1.3:myfile.txt .
```

## Copying multiple files

Copy multiple files by separating them with spaces:

```bash
scp myfile.txt myfile2.txt pi@192.168.1.3:
```

Alternatively, use a wildcard to copy all files matching a particular search with:

```bash
scp *.txt pi@192.168.1.3:
```

(all files ending in `.txt`)

```bash
scp m* pi@192.168.1.3:
```

(all files starting with `m`)

```bash
scp m*.txt pi@192.168.1.3:
```

(all files starting with `m` and ending in `.txt`)

## Filenames with spaces

Note that some of the examples above will not work for file names containing spaces. Names like this need to be encased in quotes:

```bash
scp "my file.txt" pi@192.168.1.3:
```
