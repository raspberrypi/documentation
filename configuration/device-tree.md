# Device Trees, Overlays and Parameters

Raspberry Pi's latest kernels and firmware, including Raspbian and NOOBS releases, now by default use Device Tree (DT) to manage some resource allocation and module loading. This change is to alleviate the problem of multiple drivers contending for system resources, and to allow HAT modules to be auto-configured.

The current implementation is not a pure Device Tree system -- there is still board support code that creates some platform devices -- but the external interfaces (i2c, i2s, spi) and the audio devices that use them must now be instantiated using a Device Tree Blob (DTB) passed to the kernel by the loader (`start.elf`).

The main impact of using Device Tree is to change from *everything on*, relying on module blacklisting to manage contention, to *everything off unless requested by the DTB*. In order to continue to use external interfaces and the peripherals that attach to them, you will need to add some new settings to your `config.txt`. See [Part 3](#part3) for more information, but in the meantime here are a few examples:

```bash
# Uncomment some or all of these to enable the optional hardware interfaces
#dtparam=i2c_arm=on
#dtparam=i2s=on
#dtparam=spi=on

# Uncomment one of these lines to enable an audio interface
#dtoverlay=hifiberry-amp
#dtoverlay=hifiberry-dac
#dtoverlay=hifiberry-dacplus
#dtoverlay=hifiberry-digi
#dtoverlay=iqaudio-dac
#dtoverlay=iqaudio-dacplus

# Uncomment this to enable the lirc-rpi module
#dtoverlay=lirc-rpi

# Uncomment this to override the defaults for the lirc-rpi module
#dtparam=gpio_out_pin=16
#dtparam=gpio_in_pin=17
#dtparam=gpio_in_pull=down
```

<a name="part1"></a>
## Part 1: Device Trees

A Device Tree (DT) is a description of the hardware in a system. It should include the name of the base CPU, its memory configuration and any peripherals (internal and external). A DT should not be used to describe the software, although by listing the hardware modules it does usually cause driver modules to be loaded. It helps to remember that DTs are supposed to be OS-neutral, so anything which is Linux-specific probably shouldn't be there.

Device Trees represents the hardware configuration as a hierarchy of nodes. Each node may contain properties and subnodes. Properties are named arrays of bytes, which may contain strings, numbers (big-endian), arbitrary sequences of byte, and any combination thereof. By analogy to a filesystem, nodes are directories and properties are files. The locations of nodes and properties within the tree can be described using a path, with slashes as separators and a single slash (`/`) to indicate the root.

<a name="part1.1"></a>
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

<a name="part1.2"></a>
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

<a name="part1.3"></a>
### 1.3: Labels and References

It is often necessary for one part of the tree to refer to another, and there are four ways to do this:

1. Path strings

    Paths should be self explanatory, by analogy to a filesystem -- `/soc/i2s@7e203000` is the full path to the I2S device in BCM2835 and BCM2836. Note that although it is easy to construct a path to a property (`/soc/i2s@7e203000/status` -- see, I just did it), the standard APIs don't do that; you first find a node, then choose properties of that node.

2. phandles

   A phandle is a unique 32-bit integer assigned to a node in its `phandle` property. (For historical reasons, you tend to also see a redundant, matching `linux,phandle`). phandles are numbered sequentially starting from 1 -- 0 is not a valid phandle -- and are usually allocated by the DT compiler when it encounters a reference to a node in an integer context, usually in the form of a label (see below). References to nodes using phandles are simply encoded as the corresponding integer (cell) values; there is no markup to indicate that they should be interpreted as phandles -- that is application defined.

3. Labels

   Just as a label in C gives a name to a place in the code, a DT label assigns a name to a node in the hierarchy. The compiler takes references to labels and converts them into paths when used in string context (`&node`) and phandles in integer context (`<&node>`); the original labels do not appear in the compiled output. Note that labels contain no structure -- they are just tokens in a flat, global namespace.

4. Aliases

   Aliases are similar to labels, except that they do appear in the FDT output as a form of index. They are stored as properties of the `/aliases` node, with each property mapping an alias name to a path string. Although the aliases node appears in the source, the path strings usually appear as references to labels (`&node`) rather then being written out in full. DT APIs that resolve a path string to a node typically look at the first character of the path, treating paths that do not start with a slash as aliases that must first be converted to a path using the `/aliases` table.

<a name="part1.4"></a>
### 1.4: Device Tree semantics

How to construct a device tree -- how best to use it to capture the configuration of some hardware -- is a large and complex subject. There are many resources available, some of which are listed below, and this document isn't going to be another. But there are a few things that deserve a mention.

`compatible` properties are the link between the hardware description and the driver software. When an OS encounters a node with a `compatible` property it looks it up in its database of device drivers to find the best match. In Linux this usually results in the driver module being automatically loaded, provided it has been appropriately labelled and not blacklisted.

The `status` property indicates whether a device is enabled or disabled. If the `status` is `ok`, `okay` or absent, then the device is enabled. Otherwise `status` should be `disabled`, which means what you think it means. It can be useful to place devices in a `.dtsi` file with the status set to `disabled`.  A derived configuration can then include that `.dtsi` and set the status for the devices which are needed to `okay`.

Here are some articles about writing Device Trees:

- [devicetree.org/Device_Tree_Usage](http://devicetree.org/Device_Tree_Usage)
- [elinux.org/...](http://elinux.org/images/4/48/Experiences_With_Device_Tree_Support_Development_For_ARM-Based_SOC%27s.pdf)
- [power.org/...](https://www.power.org/download.php?popup=1&file=7920&referer=/documentation/epapr-version-1-1/) (requires registration...)

<a name="part2"></a>
## Part 2: Device Tree Overlays

A modern SoC (System-on-Chip) is a very complicated device -- a complete device tree could be hundreds of lines long. Taking that one step further and placing the SoC on a board with other components only makes matters worse. To keep that manageable, particularly if there are related devices that share components, it makes sense to put the common elements in .dtsi files to be included from possibly multiple .dts files.

But when a system like Raspberry Pi supports optional plug-in accessories, such as HATs, the problem grows further. Ultimately, each possible configuration requires a device tree to describe it, but once you factor in different base hardware (models A, B, A+, and B+) and gadgets only requiring the use of a few GPIO pins that can coexist, the number of combinations starts to multiply rapidly.

What is needed is a way to describe these optional components using partial device trees, and then to be able to build a complete tree by taking a base DT and adding a number of optional elements. Well, you can, and these optional elements are called "overlays".

<a name="part2.1"></a>
### 2.1: Fragments

A DT Overlay comprises a number of fragments, each of which targets one node (and its subnodes). Although the concept sounds simple enough, the syntax seems rather strange at first:

```
// Enable the i2s interface
/dts-v1/;
/plugin/;

/ {
    compatible = "brcm,bcm2708";

    fragment@0 {
        target = <&i2s>;
        __overlay__ {
            status = "okay";
        };
    };
};
```

The `compatible` string identifies this as being for bcm2708, which is the base architecture of the BCM2835 part. For the BCM2836 part you could use a compatible string of "brcm,bcm2709", but unless you are targeting features of the ARM CPUs then the two architectures ought to be equivalent, so sticking to "brcm,bcm2708" is reasonable. Then comes the first (and in this case only) fragment. Fragments are numbered sequentially from zero. Failure to adhere to this may cause some or all of your fragments to be missed.

Each fragment consists of two parts -- a `target` property, identifying the node to apply the overlay to, and the `__overlay__` itself, the body of which is added to the target node. The example above can be interpreted as if it were written like this:

```
/dts-v1/;

/ {
    compatible = "brcm,bcm2708";
};

&i2s {
    status = "okay";
};
```

The effect of merging that overlay with a standard Raspberry Pi base device tree (`bcm2708-rpi-b-plus.dtb`, for example), provided the overlay is loaded afterwards, would be to enable the i2s interface by changing its status to `okay`. But if you try to compile this overlay, using:

```
dtc -I dts -O dtb -o 2nd-overlay.dtb 2nd-overlay.dts
```

you will get an error:

```
Label or path i2s not found
```

This shouldn't be too unexpected, since there is no reference to the base `.dtb` or `.dts` file enabling the compiler to find the `i2s` label.

Trying again, this time with the original example:

```
dtc -I dts -O dtb -o 1st-overlay.dtb 1st-overlay.dts
```

you will get one of two errors.

If `dtc` returns an error about the third line, then it doesn't have the extensions required for overlay work. The `/plugin/` directive is a signal to the compiler that it needs the ability to generate linkage information allowing unresolved symbols to be patched up later.

To install an appropriate `dtc` on a Pi, type:
```
sudo apt-get install device-tree-compiler
```

On other platforms, you have two options: if you download the kernel sources from the raspberrypi github and `make ARCH=arm dtbs` then it will build a suitable `dtc` in `scripts/dtc`. Alternatively, follow these steps in a suitable directory:

```bash
wget -c https://raw.githubusercontent.com/RobertCNelson/tools/master/pkgs/dtc.sh
chmod +x dtc.sh
./dtc.sh
```

Note: This script will download the mainline source, apply some patches, then build and install it. You may want to edit `dtc.sh` before running it to change the download path (currently `~/git/dtc`) and install path (`/usr/local/bin`).

If instead you see `Reference to non-existent node or label "i2s"` then all you need to do is change the command line to tell the compiler to allow unresolved symbols, by adding `-@`:

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
        i2s = "/fragment@0:target:0";
    };
};
```

After the verbose description of the file structure, there is our fragment. But look carefully -- where we wrote `&i2s` it now says `0xdeadbeef`, a clue that something strange has happened. After the fragment is a new node, `__fixups__`. This contains a list of properties mapping the names of unresolved symbols to lists of paths to cells within the fragments that need patching with the phandle of the target node, once that target has been located. In this case, the path is to the `0xdeadbeef` value of `target`, but fragments can contain other unresolved references which would require additional fix-ups.

If you write more complicated fragments the compiler may generate two more nodes -- `__local_fixups__` and `__symbols__`. The former is required if any node in the fragments has a phandle, because the programme performing the merge will have to ensure that phandle numbers are sequential and unique, but the latter is the key to how unresolved symbols are dealt with.

Back in section 1.3 it says that *"the original labels do not appear in the compiled output"*, but this isn't true when using the `-@` switch. Instead, every label results in a property in the `__symbols__` node, mapping a label to a path, exactly like the `aliases` node. In fact, the mechanism is so similar that when resolving symbols, the Raspberry Pi loader will search the "aliases" node in the absence of a `__symbols__` node. This is useful because by providing sufficient aliases we can allow an older `dtc` to be used to build the base DTB files.

<a name="part2.2"></a>
### 2.2: Device tree parameters

To avoid the need for lots of device tree overlays, and (we hope) to restrict the need to write DTS files to peripheral makers, the Raspberry Pi loader supports a new feature -- device tree parameters. This permits small changes to the DT using named parameters, similar to the way kernel modules receive parameters from `modprobe` and the kernel command line. Parameters can be exposed by the base DTBs and by overlays, including HAT overlays.

Parameters are defined in the DTS by adding an `__overrides__` node to the root. It contains properties whose names are the chosen parameter names, and whose values are a sequence comprising a phandle (reference to a label) for the target node, and a string indicating the target property; string, integer (cell) and boolean properties are supported.

<a name="part2.2.1"></a>
#### 2.2.1: String parameters

String parameters are declared like this:
```
name = <&label>,"property";
```
where `label` and `property` are replaced by suitable values. String parameters can cause their target properties to grow, shrink, or be created.

Note that properties called `status` are treated specially - non-zero/true/yes/on values are converted to the string `"okay"`, while zero/false/no/off becomes `"disabled"`.

<a name="part2.2.2"></a>
#### 2.2.2: Integer parameters

Integer parameters are declared like this:
```
name = <&label>,"property.offset"; // 8-bit
name = <&label>,"property;offset"; // 16-bit
name = <&label>,"property:offset"; // 32-bit
name = <&label>,"property#offset"; // 64-bit
```
where `label`, `property` and `offset` are replaced by suitable values; the offset is specified in bytes relative to the start of the property (in decimal by default), and the preceding separator dictates the size of the parameter. Integer parameters must refer to an existing part of a property - they cannot cause their target properties to grow.

<a name="part2.2.3"></a>
#### 2.2.3: Boolean parameters

Device Tree encodes boolean values as zero-length properties - if present then the property is true, otherwise it is false. They are defined like this:
```
boolean_property; // Set 'boolean_property' to true
```
Note that a property is assigned the value false by not defining it. Boolean parameters are declared like this:
```
name = <&label>,"property?";
```
where `label` and `property` are replaced by suitable values. Boolean parameters can cause properties to be created or deleted.

<a name="part2.2.4"></a>
#### 2.2.4 Examples
Here are some examples of different types of properties, with parameters to modify them:

```
/ {
	fragment@0 {
		target-path = "/";
		__overlay__ {

			test: test_node {
				string = "hello";
				status = "disabled";
				bytes = /bits/ 8 <0x67 0x89>;
				u16s = /bits/ 16 <0xabcd 0xef01>;
				u32s = /bits/ 32 <0xfedcba98 0x76543210>;
				u64s = /bits/ 64 < 0xaaaaa5a55a5a5555 0x0000111122223333>;
				bool1; // Defaults to true
				       // bool2 defaults to false
			};
		};
	};

    __overrides__ {
		string =      <&test>,"string";
		enable =      <&test>,"status";
		byte_0 =      <&test>,"bytes.0";
		byte_1 =      <&test>,"bytes.1";
		u16_0 =       <&test>,"u16s;0";
		u16_1 =       <&test>,"u16s;2";
		u32_0 =       <&test>,"u32s:0";
		u32_1 =       <&test>,"u32s:4";
		u64_0 =       <&test>,"u64s#0";
		u64_1 =       <&test>,"u64s#8";
		bool1 =       <&test>,"bool1?";
		bool2 =       <&test>,"bool2?";
    };
};
```

<a name="part2.2.5"></a>
#### 2.2.5: Parameters with multiple targets

There are some situations where it is convenient to be able to set the same value in multiple locations within the device tree. Rather than the ungainly approach of creating multiple parameters, it is possible to add multiple targets to a single parameter by concatenating them, like this:

```
    __overrides__ {
        gpiopin = <&w1>,"gpios:4",
                  <&w1_pins>,"brcm,pins:0";
        ...
    };
```
(example taken from the `w1-gpio` overlay)

Note that it is even possible to target properties of different types with a single parameter. You could reasonably connect an "enable" parameter to a `status` string, cells containing zero or one, and a proper boolean property.

<a name="part2.2.6"></a>
#### 2.2.6: Further overlay examples

There is a growing collection of overlay source files hosted in the raspberrypi/linux github repository [here](https://github.com/raspberrypi/linux/tree/rpi-3.18.y/arch/arm/boot/dts/overlays).

<a name="part3"></a>
## Part 3: Using device trees on Raspberry Pi

<a name="part3.1"></a>
### 3.1: Overlays and config.txt

On Raspberry Pi it is the job of the loader (one of the start*.elf images) to combine overlays with an appropriate base device tree, and then to pass a fully resolved device tree to the kernel. The base device trees are located alongside start.elf in the FAT partition (/boot from linux), named `bcm2708-rpi-b.dtb`, `bcm2708-rpi-b-plus.dtb`, `bcm2708-rpi-cm.dtb` and `bcm2709-rpi-2-b.dtb`. Note that Model A's and A+'s will use the "b" and "b-plus" variants, respectively. This selection is automatic, and allows the same SD card image to be used in a variety of devices.

N.B. DT and ATAGs are mutually exclusive. As a result, passing a DT blob to a kernel that doesn't understand it causes a boot failure. To guard against this, the loader checks kernel images for DT-compatibility, which is marked by a trailer added by the mkknlimg utility (found [here](https://github.com/raspberrypi/tools/blob/master/mkimage/mkknlimg), or in the scripts directory of a recent kernel source tree). Any kernel without a trailer is assumed to be non-DT-capable.

The loader now also support builds using bcm2835_defconfig, which select the upstreamed BCM2835 support. This configuration will cause `bcm2835-rpi-b.dtb` and `bcm2835-rpi-b-plus.dtb` to be built. If these files are copied with the kernel, and if the kernel has been tagged by a recent `mkknlimg`, then the loader will attempt to load one of those DTBs by default.

In order to manage device tree and overlays, the loader supports a number of new `config.txt` directives:

```
dtoverlay=acme-board
dtparam=foo=bar,level=42
```

This will cause the loader to look for `overlays/acme-board-overlay.dtb` in the firmware partition, which Raspbian mounts on `/boot`. It will then search for parameters `foo` and `level`, and assign them the indicated values.

The loader will also search for an attached HAT with a programmed EEPROM, and load the supporting overlay from there; this happens without any user intervention.

There are several ways to tell that the kernel is using device tree:

1. The "Machine model:" kernel message during boot up has a board-specific value such as "Raspberry Pi 2 Model B", rather than "BCM2709".
2. Some time later there is another kernel message saying "No ATAGs?" -- this is expected.
3. `/proc/device-tree` exists, and contains subdirectories and files that exactly mirror the nodes and properties of the DT.

With a device tree, the kernel will automatically search for and load modules that support the indicated, enabled devices. As a result, by creating an appropriate DT overlay for a device, you save users of the device from having to edit `/etc/modules` -- all of the configuration goes in config.txt (and in the case of a HAT, even that step is unnecessary). Note, however, that layered modules such as `i2c-dev` still need to be loaded explicitly.

The flip-side is that because platform devices don't get created unless requested by the DTB, it should no longer be necessary to blacklist modules that used to be loaded as a result of platform devices defined in the board support code. In fact, current Raspbian images ship without a blacklist file.

<a name="part3.2"></a>
### 3.2: DT parameters

As described above, DT parameters are a convenient way to make small changes to a device's configuration. The current base DTBs support parameters for enabling and controlling the I2C, I2S and SPI interfaces without using dedicated overlays. In use, parameters look like this:

```
dtparam=i2c_arm=on,i2c_arm_baudrate=400000,spi=on
```

Note that multiple assignments can be placed on the same line (but don't exceed the 80 (or is it 79?) character limit, because *it would be bad*).

A future default `config.txt` may contain a section like this:

```
# Uncomment some or all of these to enable the optional hardware interfaces
#dtparam=i2c_arm=on
#dtparam=i2s=on
#dtparam=spi=on
```

If you have an overlay that defines some parameters, they can be specified either on subsequent lines like this:

```
dtoverlay=lirc-rpi
dtparam=gpio_out_pin=16
dtparam=gpio_in_pin=17
dtparam=gpio_in_pull=down
```

or appended to the overlay line like this:

```
dtoverlay=lirc-rpi:gpio_out_pin=16,gpio_in_pin=17,gpio_in_pull=down
```

Note here the use of a colon (`:`) to separate the overlay name from its parameters, which is a supported syntax variant.

Overlay parameters are only in scope until the next overlay is loaded. In the event of a parameter with the same name being exported by both the overlay and the base (don't do this -- it's just confusing), the parameter in the overlay takes precedence. To expose the parameter exported by the base DTB instead, end the current overlay scope using:

```
dtoverlay=
```

<a name="part3.3"></a>
### 3.3: Board-specific labels and parameters

Raspberry Pi boards have two I2C interfaces. These are nominally split -- one for the ARM, and one for VideoCore (the "GPU"). On almost all models, `i2c1` belongs to the ARM and `i2c0` to VC, where it is used to control the camera and read the HAT EEPROM. However, there are two early revisions of the Model B that have those roles reversed.

To make it possible to use one set of overlays and parameters with all Pis, the firmware creates some board-specific DT parameters. These are:
```
i2c/i2c_arm
i2c_vc
i2c_baudrate/i2c_arm_baudrate
i2c_vc_baudrate
```
These are aliases for `i2c0`, `i2c1`, `i2c0_baudrate` and `i2c1_baudrate`. It is recommended that you only use `i2c_vc` and `i2c_vc_baudrate` if you really need to - for example, if you are programming a HAT EEPROM. Enabling `i2c_vc` can stop the Pi Camera being detected.

For people writing overlays, the same aliasing has been applied to the labels on the I2C DT nodes. Thus you should write:
```
fragment@0 {
	target = <&i2c_arm>;
	__overlay__ {
		status = "okay";
	};
};
```
Any overlays using the numeric variants will be modified to use the new aliases.

<a name="part3.4"></a>
### 3.4: HATs and device tree

A Raspberry Pi HAT is an add-on card for a "Plus"-shaped (A+, B+ or Pi 2 B) Raspberry Pi with an embedded EEPROM. The EEPROM includes any DT overlay required to enable the board, and this overlay can also expose parameters.

The HAT overlay is automatically loaded by the firmware after the base DTB, so its parameters are accessible until any other overlays are loaded (or until the overlay scope is ended using `dtoverlay=`. If for some reason you want to suppress the loading of the HAT overlay, put `dtoverlay=` before any other `dtoverlay` or `dtparam` directive.

<a name="part3.5"></a>
### 3.5: Supported overlays and parameters

Rather than documenting the individual overlays here, the reader is directed to the [README](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README) file found alongside the overlay .dtb files in `/boot/overlays`. It is kept up-to-date with additions and changes.

<a name="part4"></a>
## Part 4: Troubleshooting, and Pro tips

<a name="part4.1"></a>
### 4.1: Debugging

The loader will skip over missing overlays and bad parameters, but if there are serious errors such as a missing or corrupt base dtb or a failed overlay merge then the loader will fall back to a non-DT boot. If this happens, or if your settings don't behave as you expect, it is worth checking for warnings or errors from the loader:

```
sudo vcdbg log msg
```

Extra debugging can be enabled by adding `dtdebug=1` to `config.txt`.

If the kernel fails to come up in DT mode, **this is probably because the kernel image does not have a valid trailer**. Use [knlinfo](https://github.com/raspberrypi/tools/blob/master/mkimage/knlinfo) to check for one, and [mkknlimg](https://github.com/raspberrypi/tools/blob/master/mkimage/mkknlimg) utility to add one. Note that both utilities are also included in the scripts directory of current raspberrypi kernel source trees.

You can create a (semi-)human readable representation of the current state of DT like this:
```
dtc -I fs /proc/device-tree
```
which can be useful to see the effect of merging overlays onto the underlying tree.

If kernel modules don't load as expected, check that they aren't blacklisted (in `/etc/modprobe.d/raspi-blacklist.conf`); blacklisting shouldn't be necessary when using device tree. If that shows nothing untoward you can also check that the module is exporting the correct aliases by searching `/lib/modules/<version>/modules.alias` for the `compatible` value. If not, your driver is probably missing either:

```
.of_match_table = xxx_of_match,
```

or:

```
MODULE_DEVICE_TABLE(of, xxx_of_match);
```

Failing that, `depmod` has failed or the updated modules haven't been installed on the target filesystem.

<a name="part4.2"></a>
### 4.2: Forcing a specific device tree

If you have very specific needs that aren't supported by the default DTBs (in particular, people experimenting with the pure-DT approach used by the ARCH_BCM2835 project), or if you just want to experiment with writing your own DTs, you can tell the loader to load an alternate DTB file like this:

```
device_tree=my-pi.dtb
```

<a name="part4.3"></a>
## 4.3: Disabling device tree usage

If you decide this DT lark isn't for you (or for diagnostic purposes), you can disable DT loading and force the kernel to revert to the old behaviour by adding:

```
device_tree=
```

to `config.txt`.  Note, however, that future kernel releases may at some point no longer support this option.

<a name="part4.4"></a>
### 4.4: Short-cuts and syntax variants

The loader understands a few short-cuts:

```
dtparam=i2c_arm=on
dtparam=i2s=on
```

can be shortened to:

```
dtparam=i2c,i2s
```

(`i2c` is an alias of `i2c_arm`, and the `=on` is assumed). It also still accepts the long-form versions -- `device_tree_overlay` and `device_tree_param`.

You can also use some alternative separators if you think that `=` is overused. These are all legal:
```
dtoverlay thing:name=value,othername=othervalue
dtparam setme andsetme='long string with spaces and "a quote"'
dtparam quote="'"
```
These examples use whitespace to separate the directive from the rest of the line instead of `=`. They also use a colon to separate the overlay from its parameters, and `setme` is given the default value 1/true/on/okay.
