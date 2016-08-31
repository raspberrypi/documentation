#!/usr/bin/env python3

import os
import re
import subprocess
import time
import sys
from tabulate import tabulate

HELP = "Usage:\n\
\tpxetools --add serial\n\
\tpxetools --remove serial\n\
\tpxetools --list\n"

LAN = None
NFS_IP = None

def cmd(cmd, print_out=False, print_cmd=True, can_fail=False):
    if print_cmd:
        print("# {}".format(cmd))

    out = None
    
    try:    
        out = subprocess.check_output(cmd, shell=True).decode()
    except:
        if not can_fail:
            raise

    if print_out:
        print(out)

    return out
        
def add():
    serial = None
    if len(sys.argv) != 3:
        if os.path.exists("/usr/local/sbin/get_serial"):
            # Auto detect
            print("Will try and auto detect serial. Please plug in your Pi now!")
            cmd("systemctl stop dnsmasq")
            cmd("iptables -t raw --flush")

            try:
                serial = cmd("get_serial", print_cmd=False).rstrip()
            except KeyboardInterrupt:
                cmd("iptables-restore < /etc/iptables/rules.v4")
                cmd("systemctl start dnsmasq")
                sys.exit()

            print("Found serial")
            cmd("iptables-restore < /etc/iptables/rules.v4")
            cmd("systemctl start dnsmasq")
    else:
        serial = sys.argv[2]
    
    # Validate serial
    serial = serial.lstrip("0")
    if not re.search("^[0-9a-f]{8}$", serial):
            raise Exception("Invalid serial number {}".format(serial))

    print("Serial: {}".format(serial))
    owner = input("Owner Name (ex Gordon): ")
    name = input("Name for pi: ")
    
    print("Select a base image:")
    selection = ["I will prepare my own filesystem"] + os.listdir('/nfs/bases')
    for i in range (0, len(selection)):
        print("\t{}. {}".format(i + 1, selection[i]))
    
    img_choice = input("Enter an option number: ")

    tftp_path = "/tftpboot/{}".format(serial)
    nfs_path = "/nfs/{}".format(serial)
    if os.path.exists(tftp_path):
        raise Exception("{} already exists!".format(tftp_path))

    valid_img_choice = True
    try:
        img_choice = int(img_choice)
        # Make 0 based again
        img_choice -= 1
    except ValueError:
        valid_img_choice = False

    if img_choice < 0 or img_choice > (len(selection) - 1) or (not valid_img_choice):
        raise Exception("Invalid image choice {}".format(img_choice))    

    img = None
    if img_choice > 0:
        img = "/nfs/bases/{}".format(selection[img_choice]) 

    print("\nSetting up pi...\n")

    cmd("iptables -t raw -I DHCP_clients -m mac --mac-source {0} -j ACCEPT".format(mac(serial))) 
    cmd("iptables-save > /etc/iptables/rules.v4")
    cmd("mkdir {}".format(tftp_path))
    cmd("cp -r /tftpboot/base/* {}".format(tftp_path))
    cmd("mkdir {}".format(nfs_path))
    cmd("echo \"{} *(rw,sync,no_subtree_check,no_root_squash)\" >> /etc/exports".format(nfs_path))
    cmd("exportfs -a")
    
    cmdline_txt = "dwc_otg.lpm_enable=0 root=/dev/nfs nfsroot={}:{} rw ip=dhcp rootwait elevator=deadline".format(NFS_IP, nfs_path)
    cmd("echo \"{}\" > {}/cmdline.txt".format(cmdline_txt, tftp_path))
    cmd("echo \"{}\" > {}/owner".format(owner, tftp_path))
    cmd("echo \"{}\" > {}/name".format(name, tftp_path))

    if img_choice:
        cmd("mkdir -p /mnt/tmp")
        cmd("kpartx -a -v {}".format(img), print_out=True)
        time.sleep(1)
        cmd("mount /dev/mapper/loop0p2 /mnt/tmp")
        cmd("rsync -a /mnt/tmp/ {}/".format(nfs_path))
        cmd("umount /mnt/tmp")
        cmd("echo > {}/etc/fstab".format(nfs_path))
        cmd("cd {}/etc/init.d; rm dhcpcd dphys-swapfile raspi-config resize2fs_once".format(nfs_path))
        cmd("cd {}/etc/systemd/system; rm -r dhcp* multi-user.target.wants/dhcp*".format(nfs_path))
        cmd("mount /dev/mapper/loop0p1 /mnt/tmp")
        cmd("rsync -a --exclude bootcode.bin --exclude start.elf --exclude cmdline.txt /mnt/tmp/ {}/".format(tftp_path))
        cmd("umount /mnt/tmp")
        cmd("kpartx -d -v {}".format(img), print_out=True)
    else:
        print("You opted to prep your own system so please put files in:\n\t{}\n\t{}".format(tftp_path, nfs_path))
        print("I have wrote you a cmdline.txt so don't change it:")
        print(cmdline_txt)

    print("Should be working. You might have to wait a couple of minutes before SSH lets you in")

def remove():
    serial = sys.argv[2]
    
    if not re.search("^[0-9a-f]{8}$", serial):
            raise Exception("Invalid serial number {}".format(serial))
    
    sure = ""
    while sure != "Y" and sure != "N":
        sure = input("ARE YOU SURE YOU WANT TO DELETE {}? Y/N: ".format(serial))

    if sure == "N":
        print("Aborting")
        return
    
    cmd("rm -rf /tftpboot/{}".format(serial), can_fail=True)

    nfspath = "/nfs/{}".format(serial)
    cmd("rm -rf {}".format(nfspath), can_fail=True)

    print("Removing from /etc/exports")
    with open("/etc/exports", 'r+') as f: 
        export = f.read()
        f.seek(0)

        for l in export.splitlines():
            if l.startswith(nfspath) == False:
                f.write(l + "\n")

        f.truncate()

    mac_uppercase = mac(serial).upper()
    print("Removing from iptables rules")
    with open("/etc/iptables/rules.v4", 'r+') as f:
        rules = f.read()
        f.seek(0)

        for l in rules.splitlines():
            if mac_uppercase not in l:
                f.write(l + "\n")

        f.truncate()

    cmd("iptables-restore < /etc/iptables/rules.v4")

def mac(serial):
    # MAC is least significant bits of serial
    # Example:
    # b8:27:eb:be:e3:d2
    # 0000000044bee3d2
    prefix = "b8:27:eb:"
    suffix = serial[-6:]

    # Insert colon every 2 chars. Stolen from stackoverflow
    s = suffix
    s = ":".join(a+b for a,b in zip(s[::2], s[1::2]))
    return prefix + s

def ip(mac):
    # Hacky way of getting IP from Mac Address
    cmdstr = ("nmap -sn -PR --min-rate 5000 --max-retries=0 {0} " 
              "| grep -i -B 2 {1} | head -n 1 |"
              " awk '{{print $5}}'").format(LAN, mac)
    ip = cmd(cmdstr, print_cmd=False)
    if len(ip) == 0:
        ip = "Not found"
    else:
        ip = ip.rstrip()

    return ip

def file_or_none(base, file):
    path = os.path.join(base, file)
    if not os.path.exists(path):
        return "Not Found"

    with open(path, 'r') as fh:
        return fh.read()

def list():
    tbl = [["Serial", "Owner", "Name", "MAC", "IP"]]
    pis = os.listdir("/tftpboot")
    pis = [p for p in pis if p != "base" and p != "bootcode.bin"]
    
    for p in pis:
        base = os.path.join("/tftpboot", p)
        tbl.append(["0x{}".format(p), file_or_none(base, "owner"), file_or_none(base, "name"), mac(p), ip(mac(p))])

    print(tabulate(tbl, headers="firstrow"))

if __name__ == "__main__":
    if os.geteuid() != 0:
        exit("Please run with sudo or as root user")

    LAN = cmd('ip -4 addr show dev eth0 | grep inet | cut -d " " -f6 | xargs ipcalc | grep Network | cut -d " " -f4', print_cmd=False).rstrip()
    NFS_IP = cmd('ifconfig eth0 | grep "inet addr" | cut -d " " -f 12 | cut -d ":" -f 2', print_cmd=False).rstrip()

    if len(sys.argv) == 1:
        print(HELP)
    elif sys.argv[1] == "--list":
        list()
    elif sys.argv[1] == "--add":
        add()
    elif sys.argv[1] == "--remove":
        remove()
    else:
        print(HELP)
