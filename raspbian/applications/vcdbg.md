## VCDBG

`vcdbg` is a application to help with debugging the VideoCore GPU from Linux running on the the ARM. It needs to be run as root. This application is mostly of use to Raspberry Pi engineers although there are some commands that general users may find useful.

`sudo vcdbg help` will give a list of available commands.

Only options of use to end users have been described here.

### Commands

#### version

Dumps various items of version information from the VideoCore.

#### malloc

List all memory allocations current in the VideoCore heap.

#### pools

List the current status of the pool allocator

#### reloc

Without any further parameters, lists the current status of the relocatable allocator. use `sudo vcdbg reloc small` to list small allocations as well.

Use the subcommand `sudo vcdbg reloc stats` to list statistics for the relocatable allocator. 

#### hist

Commands related to task history.

Use `sudo vcdbg hist gnuplot` to dump task history in gnuplot format to task.gpt and task.dat

  
  

