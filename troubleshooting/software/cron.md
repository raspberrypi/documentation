#Cron / Crontab

Cron is is service running on any linux based Raspberry Pi which can be used to run commands, scripts or other software at specific times.
For example, if you wanted a script to run once every 5 minutes, cron would provide you with one way of achieving this.

For troubleshooting purposes you may wish to check how cron is set up on a particular Raspberry Pi.

To check the config for scripts that will be run as the current user, type:
```
crontab -l
```
To check the config for scripts that will run as root, type::
```
sudo crontab -l
```

If you want to temporarily prevent a script from running then you can edit the crontab with 
```
crontab -e
```
or
```
sudo crontab -e
```
as appropriate.
