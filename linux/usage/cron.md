# Scheduling tasks with Cron

Cron is a tool for configuring scheduled tasks on Unix systems. It is used to schedule commands or scripts to run periodically and at fixed intervals. Tasks range from backing up the user's home folders every day at midnight, to logging CPU information every hour.

The command `crontab` (cron table) is used to edit the list of scheduled tasks in operation, and is done on a per-user basis; each user (including `root`) has their own `crontab`.

## Editing crontab

Run `crontab` with the `-e` flag to edit the cron table:

```bash
crontab -e
```

### Select an editor

The first time you run `crontab` you'll be prompted to select an editor; if you are not sure which one to use, choose `nano` by pressing `Enter`.

### Add a scheduled task

The layout for a cron entry is made up of six components: minute, hour, day of month, month of year, day of week, and the command to be executed.

```
# m h  dom mon dow   command
```

```
# * * * * *  command to execute
# ┬ ┬ ┬ ┬ ┬
# │ │ │ │ │
# │ │ │ │ │
# │ │ │ │ └───── day of week (0 - 7) (0 to 6 are Sunday to Saturday, or use names; 7 is Sunday, the same as 0)
# │ │ │ └────────── month (1 - 12)
# │ │ └─────────────── day of month (1 - 31)
# │ └──────────────────── hour (0 - 23)
# └───────────────────────── min (0 - 59)
```

For example:

```
0 0 * * *  /home/pi/backup.sh
```

This cron entry would run the `backup.sh` script every day at midnight.

### View scheduled tasks

View your currently saved scheduled tasks with:

```bash
crontab -l
````

### Run a task on reboot

To run a command every time the Raspberry Pi starts up, write `@reboot` instead of the time and date. For example:

```
@reboot python /home/pi/myscript.py
```

This will run your Python script every time the Raspberry Pi reboots. If you want your command to be run in the background while the Raspberry Pi continues starting up, add a space and `&` at the end of the line, like this:

```
@reboot python /home/pi/myscript.py &
```
