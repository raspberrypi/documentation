# Device Trees, Overlays and Parameters

Raspberry Pi's latest kernels and firmware now by default use Device Tree (DT) to manage some resource allocation module usage. At the time of writing this only applies to `BRANCH=next`, but at some point the master branch will also switch over at which time all users who update will be affected. This change is to ease the management of multiple drivers contending for system resources, and to allow HAT modules to be auto-configured.

The current solution is not a pure Device Tree system -- there is still board support code that creates some platform devices -- but the external interfaces (i2c, i2s, spi) and the audio devices that use them must now be instantiated using a Device Tree Blob (DTB) passed to the kernel by the loader (`start.elf`).

The main impact of using Device Tree is to change from *everything on*, relying on module blacklisting to manage contention, to *everything off unless requested by the DTB*. In order to continue to use external interfaces and the peripherals that attach to them, you will need to add some new settings to your `config.txt`:

```bash
# Uncomment some or all of these to enable the optional hardware interfaces
#device_tree_param=i2c1=on
#device_tree_param=i2s=on
#device_tree_param=spi=on

# Uncomment one of these lines to enable an audio interface
#device_tree_overlay=hifiberry-dac
#device_tree_overlay=hifiberry-dacplus
#device_tree_overlay=hifiberry-digi
#device_tree_overlay=iqaudio-dac
#device_tree_overlay=iqaudio-dacplus

# Uncomment this to enable the lirc-rpi module
#device_tree_overlay=lirc-rpi

# Uncomment this to override the defaults for the lirc-rpi module
#device_tree_param=gpio_out_pin=16
#device_tree_param=gpio_in_pin=17
#device_tree_param=gpio_in_pull=down
```

## Part 1: Device Trees

A Device Tree (DT) is a description of the hardware in a system. It should include the name of the base CPU, its memory configuration and any peripherals (internal and external). A DT should not be used to describe the software, although by listing the hardware modules it does usually cause driver modules to be loaded. It helps to remember that DTs are supposed to be OS-neutral, so anything which is Linux-specific probably shouldn't be there.

Device Trees represents the hardware configuration as a hierarchy of nodes. Each node may contain properties and subnodes. Properties are named arrays of bytes, which may contain strings, numbers (big-endian), arbitrary sequences of byte, and any combination thereof. By analogy to a filesystem, nodes are directories and properties are files. The locations of nodes and properties within the tree can be described using a path, with slashes as separators and a single slash (`/`) to indicate the root.

### 1.1: Basic DTS syntax

[ This section borrows heavily from [devicetree.org](http://devicetree.org/Device_Tree_Usage) ]

Device Trees are usually written in a textual form known as Device Tree Source (DTS) and stored in files with a `.dts` suffix. DTS syntax is C-like, with braces for grouping and semicolons at the end of each line. N.B. DTS requires semicolons after closing braces -- think of C `struct`s rather than functions. The compiled, binary format is referred to as Flattened Device Tree (FDT) or Device Tree Blob (DTB), and is stored in `.dtb` files.

The following is a simple tree in the `.dts` format:

```
/dts-v1/;
/include/ "common.dtsi";

/ {
    node1 {
        a-string-property = "A string";
        a-string-list-property = "first string", "second string";
        a-byte-data-property = [0x01 0x23 0x34 0x56];
        cousin: child-node1 {
            first-child-property;
            second-child-property = <1>;
            a-string-property = "Hello, world";
        };
        child-node2 {
        };
    };
    node2 {
        an-empty-property;
        a-cell-property = <1 2 3 4>; /* each number (cell) is a uint32 */
        child-node1 {
            my-cousin = <&cousin>;
        };
    };
};

/node2 {
    another-property-for-node2;
};
```

This tree contains:

 - List item
 - a required header -- `/dts-v1/`.
 - The inclusion of another DTS file, conventionally named `*.dtsi`, analogous to a `.h` header file in C -- see _An aside about /include/_ below.
 - a single root node: `/`
 - a couple of child nodes: `node1` and `node2`
 - some children for node1: `child-node1` and `child-node2`
 - a label (`cousin`) and a reference to that label (`&cousin`) -- see _Labels and References_ below.
 - a bunch of properties scattered through the tree.
 - a repeated node (`/node2`) -- see _An aside about /include/_ below.

Properties are simple key-value pairs where the value can either be empty or contain an arbitrary byte stream. While data types are not encoded into the data structure, there are a few fundamental data representations that can be expressed in a device tree source file.

Text strings (NUL-terminated) are indicated with double quotes:

```
string-property = "a string";
```

'Cells' are 32-bit unsigned integers delimited by angle brackets:

```
cell-property = <0xbeef 123 0xabcd1234>;
```

Arbitrary byte data is delimited with square brackets, and entered in hex:

```
binary-property = [01 23 45 67 89 ab cd ef];
```

Data of differing representations can be concatenated together using a comma:

```
mixed-property = "a string", [01 23 45 67], <0x12345678>;
```

Commas are also used to create lists of strings:

```
string-list = "red fish", "blue fish";
```

### 1.2: An aside about /include/

The `/include/` directive results in simple textual inclusion, much like C's `#include` directive, but a feature of the device tree compiler leads to different usage patterns. Given that nodes are named, potentially with absolute paths, it is possible for the same node to appear twice in a DTS file (and its inclusions). When this happens, the nodes and properties are combined, interleaving and overwriting properties as required (later values override earlier ones).

In the example above, the second appearanace of `/node2` causes a new property to be added to the original:

```
/node2 {
    an-empty-property;
    a-cell-property = <1 2 3 4>; /* each number (cell) is a uint32 */
    another-property-for-node2;
    child-node1 {
        my-cousin = <&cousin>;
    };
};
```

It is thus possible for one `.dtsi` to overwrite (or provide defaults for) multiple places in a tree.

### 1.3: Labels and References

It is often necessary for one part of the tree to refer to another, and there are four ways to do this:

1. Path strings

    Paths should be self explanatory, by analogy to a filesystem -- `/soc/i2c@7e205000` is the full path to the i2c0 device in BCM2835. Note that although it is easy to construct a path to a property (`/soc/i2c@7e205000/clocks` -- see, I just did it), the standard APIs don't do that; you first find a node, then choose properties of that node.

2. phandles

   A phandle is a unique 32-bit integer assigned to a node in its `phandle` property. (For historical reasons, you tend to also see a redundant, matching `linux,phandle`). phandles are numbered sequentially starting from 1 -- 0 is not a valid phandle -- and are usually allocated by the DT compiler when it encounters a reference to a node in an integer context, usually in the form of a label (see below). References to nodes using phandles are simply encoded as the corresponding integer (cell) values; there is no markup to indicate that they should be interpreted as phandles -- that is application defined.

3. Labels

   Just as a label in C gives a name to a place in the code, a DT label assigns a name to a node in the hierarchy. The compiler takes references to labels and converts them into paths when used in string context (`&node`) and phandles in integer context (`<&node>`); the original labels do not appear in the compiled output. Note that labels contain no structure -- they are just tokens in a flat, global namespace.

4. Aliases

   Aliases are similar to labels, except that they do appear in the FDT output as a form of index. They are stored as properties of the `/aliases` node, with each property mapping an alias name to a path string. Although the aliases node appears in the source, the path strings usually appear as references to labels (`&node`) rather then being written out in full. DT APIs that resolve a path string to a node typically look at the first character of the path, treating paths that do not start with a slash as aliases that must first be converted to a path using the `/aliases` table.

### 1.4: Device Tree semantics

How to construct a device tree -- how best to use it to capture the configuration of some hardware -- is a large and complex subject. There are many resources available, some of which are listed below, and this document isn't going to be another. But there are a few things that deserve a mention.

`compatible` properties are the link between the hardware description and the driver software. When an OS encounters a node with a `compatible` property it looks it up in its database of device drivers to find the best match. In Linux this usually results in the driver module being automatically loaded, provided it has been appropriately labelled and not blacklisted.

The `status` property indicates whether a device is enabled or disabled. If the `status` is `ok`, `okay` or absent, then the device is enabled. Otherwise `status` should be `disabled`, which means what you think it means. It can be useful to place devices in a `.dtsi` file with the status set to `disabled`.  A derived configuration can then include that `.dtsi` and set the status for the devices which are needed to `okay`.

Here are some articles about writing Device Trees:

- [devicetree.org/Device_Tree_Usage](http://devicetree.org/Device_Tree_Usage)
- [elinux.org/...](http://elinux.org/images/4/48/Experiences_With_Device_Tree_Support_Development_For_ARM-Based_SOC%27s.pdf)
- [power.org/...](https://www.power.org/download.php?popup=1&file=7920&referer=/documentation/epapr-version-1-1/) (requires registration...)

## Part 2: Device Tree Overlays

A modern SoC (System-on-Chip) is a very complicated device -- a complete device tree could be hundreds of lines long. Taking that one step further and placing the SoC on a board with other components only makes matters worse. To keep that manageable, particularly if there are related devices that share components, it makes sense to put the common elements in .dtsi files to be included from possibly multiple .dts files.

But when a system like Raspberry Pi supports optional plug-in accessories, such as HATs, the problem grows further. Ultimately, each possible configuration requires a device tree to describe it, but once you factor in different base hardware (models A, B, A+, and B+) and gadgets only requiring the use of a few GPIO pins that can coexist, the number of combinations starts to multiply rapidly.

What is needed is a way to describe these optional components using partial device trees, and then to be able to build a complete tree by taking a base DT and adding a number of optional elements. Well, you can, and these optional elements are called "overlays".

### 2.1: Fragments

A DT Overlay comprises a number of fragments, each of which targets one node (and its subnodes). Although the concept sounds simple enough, the syntax seems rather strange at first:

```
// Enable the i2c-1 device
/dts-v1/;
/plugin/;

/ {
    compatible = "brcm,bcm2708";

    fragment@0 {
        target = <&i2c1>;
        __overlay__ {
            status = "okay";
        };
    };
};
```

The `compatible` string identifies this as being for bcm2708, which is the base architecture of the BCM2835 part. Then comes the first (and in this case only) fragment. Fragments are numbered sequentially from zero. Failure to adhere to this may cause some or all of your fragments to be missed.

Each fragment consists of two parts -- a `target` property, identifying the node to apply the overlay to, and the `__overlay__` itself, the body of which is added to the target node. The example above can be interpreted as if it were written like this:

```
/dts-v1/;

/ {
    compatible = "brcm,bcm2708";
};

&i2c1 {
    status = "okay";
};
```

The effect of merging that overlay with a standard Raspberry Pi base device tree (`bcm2708-rpi-b-plus.dtb`, for example), provided the overlay is loaded afterwards, would be to enable the second i2c interface by changing its status to `okay`. But if you try to compile this overlay, using:

```
dtc -I dts -O dtb -o 2nd-overlay.dtb 2nd-overlay.dts
```

you will get an error:

```
Label or path i2c1 not found
```

This shouldn't be too unexpected, since there is no reference to the base `.dtb` or `.dts` file enabling the compiler to find the `i2c1` label.

Trying again, this time with the original example:

```
dtc -I dts -O dtb -o 1st-overlay.dtb 1st-overlay.dts
```

you will get one of two errors.

If `dtc` returns an error about the third line, then it doesn't have the extensions required for overlay work. The `/plugin/` directive is a signal to the compiler that it needs the ability to generate linkage information allowing unresolved symbols to be patched up later. To build an updated compiler, follow these steps in a suitable directory:

```bash
wget -c https://raw.githubusercontent.com/RobertCNelson/tools/master/pkgs/dtc.sh
chmod +x dtc.sh
./dtc.sh
```

Note: This script will download the mainline source, apply some patches, then build and install it. You may want to edit `dtc.sh` before running it to change the download path (currently `~/git/dtc`) and install path (`/usr/local/bin`).

If instead you see `Reference to non-existent node or label "i2c1"` then all you need to do is change the command line to tell the compiler to allow unresolved symbols, by adding `-@`:

```
dtc -@ -I dts -O dtb -o 1st-overlay.dtb 1st-overlay.dts
```

This time, compilation should complete successfully. It is interesting to dump the contents of the DTB file to see what the compiler has generated:

```
$ fdtdump 1st-overlay.dtb

/dts-v1/;
// magic:           0xd00dfeed
// totalsize:       0x106 (262)
// off_dt_struct:   0x38
// off_dt_strings:  0xe8
// off_mem_rsvmap:  0x28
// version:         17
// last_comp_version:    16
// boot_cpuid_phys: 0x0
// size_dt_strings: 0x1e
// size_dt_struct:  0xb0

/ {
    compatible = "brcm,bcm2708";
    fragment@0 {
        target = <0xdeadbeef>;
        __overlay__ {
            status = "okay";
        };
    };
    __fixups__ {
        i2c1 = "/fragment@0:target:0";
    };
};
```

After the verbose description of the file structure, there is our fragment. But look carefully -- where we wrote `&i2c1` it now says `0xdeadbeef`, a clue that something strange has happened. After the fragment is a new node, `__fixups__`. This contains a list of properties mapping the names of unresolved symbols to lists of paths to cells within the fragments that need patching with the phandle of the target node, once that target has been located. In this case, the path is to the `0xdeadbeef` value of `target`, but fragments can contain other unresolved references which would require additional fix-ups.

If you write more complicated fragments the compiler may generate two more nodes -- `__local_fixups__` and `__symbols__`. The former is required if any node in the fragments has a phandle, because the programme performing the merge will have to ensure that phandle numbers are sequential and unique, but the latter is the key to how unresolved symbols are dealt with.

Back in section 1.3 it says that *"the original labels do not appear in the compiled output"*, but this isn't true when using the `-@` switch. Instead, every label results in a property in the `__symbols__` node, mapping a label to a path, exactly like the `aliases` node. In fact, the mechanism is so similar that when resolving symbols, the Raspberry Pi loader will search the "aliases" node in the absence of a `__symbols__` node. This is useful because by providing sufficient aliases we can allow an older `dtc` to be used to build the base DTB files.

## 2.2: Device tree parameters

To avoid the need for lots of device tree overlays, and (we hope) to restrict the need to write DTS files to peripheral makers, the Raspberry Pi loader supports a new feature -- device tree parameters. This permits small changes to the DT using named parameters, similar to the way kernel modules receive parameters from the kernel command line. Parameters can be exposed by the base DTBs and by overlays, including HAT overlays.

Parameters are defined in the DTS by adding an `__overrides__` node to the root. It contains properties whose names are the required parameter names, and the values are a sequence comprising a phandle for the target node and a string naming the target property. If the target is a cell then the property name must be followed by a colon and the byte offset (in decimal by default, usually 0) into the property value where the cell to be patched can be found; otherwise, the parameter is treated as a string parameter to be overwritten by the supplied value. Note that cell parameters must refer to an existing cell, whereas a string parameter can cause the target property to grow.

Here is an example from `bcm2708-rpi-b-plus.dts` showing four string parameters:

```
/ {
    ...

    __overrides__ {
        i2s = <&i2s>,"status";
        spi = <&spi0>,"status";
        i2c0 = <&i2c0>,"status";
        i2c1 = <&i2c1>,"status";
    };
};
```

and one from `lirc-rpi-overlay.dts` showing some integer (cell) parameters:

```
/ {
    ...

    __overrides__ {
        gpio_out_pin =  <&lirc_pins>,"brcm,pins:0";
        gpio_in_pin =   <&lirc_pins>,"brcm,pins:4";
        gpio_in_pull =  <&lirc_pins>,"brcm,pull:4";

        sense =         <&lirc_rpi>,"rpi,sense:0";
        softcarrier =   <&lirc_rpi>,"rpi,softcarrier:0";
        invert =        <&lirc_rpi>,"rpi,invert:0";
        debug =         <&lirc_rpi>,"rpi,debug:0";
    };
};
```

Note that the `gpio_out_pin` and `gpio_in_pin` parameters refer to adjacent cells in the `brcm,pins` property.

## Part 3: Using device trees on Raspberry Pi

### 3.1: Overlays and config.txt

On Raspberry Pi it is the job of the loader (one of the start*.elf images) to combine overlays with an appropriate base device tree, and then to pass a fully resolved device tree to the kernel. The base device trees are located alongside start.elf in the FAT partition (/boot from linux), named `bcm2708-rpi-b.dtb` and `bcm2708-rpi-b-plus.dtb`. Here, the presence or absence of the "-plus" is the significant thing, not the "b" -- Model A's and A+'s will use the "b" and "b-plus" variants, respectively. This selection is automatic, and allows the same SD card image to be used in a variety of devices.

N.B. DT and ATAGs are mutually exclusive. As a result, passing a DT blob to a kernel that doesn't understand it causes a boot failure. To guard against this, the loader checks kernel images for DT-compatibility, which is marked by a trailer added by the mkknlimg utility (found [here](https://github.com/raspberrypi/tools/blob/master/mkimage/mkknlimg)). Any kernel without a trailer is assumed to be non-DT-capable.

In order to manage device tree and overlays, the loader supports a number of new `config.txt` directives:

```
device_tree_overlay=overlays/acme-board-overlay.dtb
```

The loader will also search for an attached HAT with a programmed EEPROM, and load the supporting overlay from there; this happens without any user intervention.

There are several ways to tell that the kernel is using device tree:

1. The "Machine model:" kernel message during boot up says "Raspberry Pi Model B+" (or B) instead of "BCM2708".
2. Some time later there is another kernel message saying "No ATAGs?" -- this is expected.
3. `/proc/device-tree` exists, and contains subdirectories and files that exactly mirror the nodes and properties of the DT.

With a device tree, the kernel will automatically search for and load modules that support the indicated, enabled devices. As a result, it should no longer be necessary to blacklist files that used to be loaded as a result of platform devices defined in the board support code. The flip-side is that by creating an appropriate DT overlay for a device, you save users of the device from having to edit `/etc/modules` -- all of the configuration goes in config.txt. And in the case of a HAT, even that step is unnecessary.

### 3.2: DT parameters

As described above, DT parameters are a convenient way to make small changes to a device's configuration. The current base DTBs support four parameters -- `i2c0`, `i2c1`, `i2s` and `spi` -- that allow you to enable those interfaces without using dedicated overlays. In use, parameters look like this:

```
device_tree_param=i2c1=on,spi=on
```

Note that multiple assignments can be placed on the same line (but don't exceed the 80 (or is it 79?) character limit, because *it would be bad*).

A future default `config.txt` may contain a section like this:

```
# Uncomment some or all of these to enable the optional hardware interfaces
#device_tree_param=i2c1=on
#device_tree_param=i2s=on
#device_tree_param=spi=on
```

If you have an overlay that defines some parameters, they can be specified either on subsequent lines like this:

```
device_tree_overlay=overlays/lirc-rpi-overlay.dtb
device_tree_param=gpio_out_pin=16
device_tree_param=gpio_in_pin=17
device_tree_param=gpio_in_pull=down
```

or appended to the overlay line like this:

```
dtoverlay=lirc-rpi:gpio_out_pin=16,gpio_in_pin=17,gpio_in_pull=down
```

Note here the use of the abbreviations -- the `overlays/` and `-overlay.dtb` are assumed.

Overlay parameters are only in scope until the next overlay is loaded. In the event of a parameter with the same name being exported by both the overlay and the base (don't do this -- it's just confusing), the parameter in the overlay takes precedence. To expose the parameter exported by the base DTB instead, end the current overlay scope using:

```
dtoverlay=
```

### 3.3: Supported overlays and parameters

Rather than documenting the individual overlays here, the reader is directed to the README file found alongside the overlay .dtb files in `/boot/overlays`. It will be updated with additions and changes.

## Part 4: Troubleshooting, and Pro tips

### 4.1: Debugging

The loader will skip over missing overlays and bad parameters, but if there are serious errors such as a missing or corrupt base dtb or a failed overlay merge then the loader will fall back to a non-DT boot. If this happens, or if your settings don't behave as you expect, it is worth checking for warnings or errors from the loader:

```
sudo vcdbg log msg
```

Extra debugging can be enabled by adding `dtdebug=1` to `config.txt`.

If the kernel fails to come up in DT mode, this is probably because the kernel image does not have a valid trailer. Use [knlinfo](https://github.com/raspberrypi/tools/blob/master/mkimage/knlinfo) to check for one, and [mkknlimg](https://github.com/raspberrypi/tools/blob/master/mkimage/mkknlimg) utility to add one.

If kernel modules don't load as expected, check that they aren't blacklisted (in `/etc/modprobe.d/raspi-blacklist.conf`); blacklisting shouldn't be necessary when using device tree. If that shows nothing untoward you can also check that the module is exporting the correct aliases by searching `/lib/modules/<version>/modules.alias` for the `compatible` value. If not, your driver is probably missing either:

```
.of_match_table = xxx_of_match,
```

or:

```
MODULE_DEVICE_TABLE(of, xxx_of_match);
```

Failing that, `depmod` has failed or the updated modules haven't been installed on the target filesystem.

### 4.2: Forcing a specific device tree

If you have very specific needs that aren't supported by the default DTBs (in particular, people experimenting with the pure-DT approach used by the ARCH_BCM2835 project), or if you just want to experiment with writing your own DTs, you can tell the loader to load an alternate DTB file like this:

```
device_tree=my-pi.dtb
```

## 4.3: Disabling device tree usage

If you decide this DT lark isn't for you (or for diagnostic purposes), you can disable DT loading and force the kernel to revert to the old behaviour by adding:

```
device_tree=
```

to `config.txt`.  Note, however, that future kernel releases may at some point no longer support this option.

### 4.4: Short-cuts

If typing `device_tree_overlay` is just too many keystrokes, there are a few short-cuts:

```
device_tree_overlay=overlays/acme-board-overlay.dtb
```

can be abbreviated to:

```
dtoverlay=acme-board
```

Similarly:

```
device_tree_param=i2c1=on
device_tree_param=i2s=on
```

can be shortened to:

```
dtparam=i2c1,i2s
```

(the `=on` is assumed).
