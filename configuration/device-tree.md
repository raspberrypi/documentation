# Device Trees, overlays, and parameters

Raspberry Pi kernels and firmware use a Device Tree (DT) to describe the hardware present in the Pi. These Device Trees may include DT parameters that provide a degree of control over some onboard features. DT overlays allow optional external hardware to be described and configured, and they also support parameters for more control.

The firmware loader (`start.elf` and its variants) is responsible for loading the DTB (Device Tree Blob - a machine readable DT file). It chooses which one to load based on the board revision number, and makes certain modifications to further tailor it (memory size, Ethernet addresses etc.). This runtime customisation avoids the need for lots of DTBs with only minor differences.

`config.txt` is scanned for user-provided parameters, along with any overlays and their parameters, which are then applied. The loader examines the result to learn (for example) which UART, if any, is to be used for the console. Finally it launches the kernel, passing a pointer to the merged DTB.

<a name="part1"></a>
## Device Trees

A Device Tree (DT) is a description of the hardware in a system. It should include the name of the base CPU, its memory configuration, and any peripherals (internal and external). A DT should not be used to describe the software, although by listing the hardware modules it does usually cause driver modules to be loaded. It helps to remember that DTs are supposed to be OS-neutral, so anything which is Linux-specific probably shouldn't be there.

A Device Tree represents the hardware configuration as a hierarchy of nodes. Each node may contain properties and subnodes. Properties are named arrays of bytes, which may contain strings, numbers (big-endian), arbitrary sequences of bytes, and any combination thereof. By analogy to a filesystem, nodes are directories and properties are files. The locations of nodes and properties within the tree can be described using a path, with slashes as separators and a single slash (`/`) to indicate the root.

<a name="part1.1"></a>
### 1.1: Basic DTS syntax

Device Trees are usually written in a textual form known as Device Tree Source (DTS) and stored in files with a `.dts` suffix. DTS syntax is C-like, with braces for grouping and semicolons at the end of each line. Note that DTS requires semicolons after closing braces: think of C `struct`s rather than functions. The compiled binary format is referred to as Flattened Device Tree (FDT) or Device Tree Blob (DTB), and is stored in `.dtb` files.

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

 - a required header: `/dts-v1/`.
 - The inclusion of another DTS file, conventionally named `*.dtsi` and analogous to a `.h` header file in C - see _An aside about /include/_ below.
 - a single root node: `/`
 - a couple of child nodes: `node1` and `node2`
 - some children for node1: `child-node1` and `child-node2`
 - a label (`cousin`) and a reference to that label (`&cousin`): see _Labels and References_ below.
 - several properties scattered through the tree
 - a repeated node (`/node2`) - see _An aside about /include/_ below.

Properties are simple key-value pairs where the value can either be empty or contain an arbitrary byte stream. While data types are not encoded in the data structure, there are a few fundamental data representations that can be expressed in a Device Tree source file.

Text strings (NUL-terminated) are indicated with double quotes:

```
string-property = "a string";
```

Cells are 32-bit unsigned integers delimited by angle brackets:

```
cell-property = <0xbeef 123 0xabcd1234>;
```

Arbitrary byte data is delimited with square brackets, and entered in hex:

```
binary-property = [01 23 45 67 89 ab cd ef];
```

Data of differing representations can be concatenated using a comma:

```
mixed-property = "a string", [01 23 45 67], <0x12345678>;
```

Commas are also used to create lists of strings:

```
string-list = "red fish", "blue fish";
```

<a name="part1.2"></a>
### 1.2: An aside about /include/

The `/include/` directive results in simple textual inclusion, much like C's `#include` directive, but a feature of the Device Tree compiler leads to different usage patterns. Given that nodes are named, potentially with absolute paths, it is possible for the same node to appear twice in a DTS file (and its inclusions). When this happens, the nodes and properties are combined, interleaving and overwriting properties as required (later values override earlier ones).

In the example above, the second appearance of `/node2` causes a new property to be added to the original:

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

It is thus possible for one `.dtsi` to overwrite, or provide defaults for, multiple places in a tree.

<a name="part1.3"></a>
### 1.3: Labels and references

It is often necessary for one part of the tree to refer to another, and there are four ways to do this:

1. Path strings

    Paths should be self-explanatory, by analogy with a filesystem - `/soc/i2s@7e203000` is the full path to the I2S device in BCM2835 and BCM2836. Note that although it is easy to construct a path to a property (for example, `/soc/i2s@7e203000/status`), the standard APIs don't do that; you first find a node, then choose properties of that node.

1. phandles

   A phandle is a unique 32-bit integer assigned to a node in its `phandle` property. For historical reasons, you may also see a redundant, matching `linux,phandle`. phandles are numbered sequentially, starting from 1; 0 is not a valid phandle. They are usually allocated by the DT compiler when it encounters a reference to a node in an integer context, usually in the form of a label (see below). References to nodes using phandles are simply encoded as the corresponding integer (cell) values; there is no markup to indicate that they should be interpreted as phandles, as that is application-defined.

1. Labels

   Just as a label in C gives a name to a place in the code, a DT label assigns a name to a node in the hierarchy. The compiler takes references to labels and converts them into paths when used in string context (`&node`) and phandles in integer context (`<&node>`); the original labels do not appear in the compiled output. Note that labels contain no structure; they are just tokens in a flat, global namespace.

1. Aliases

   Aliases are similar to labels, except that they do appear in the FDT output as a form of index. They are stored as properties of the `/aliases` node, with each property mapping an alias name to a path string. Although the aliases node appears in the source, the path strings usually appear as references to labels (`&node`), rather then being written out in full. DT APIs that resolve a path string to a node typically look at the first character of the path, treating paths that do not start with a slash as aliases that must first be converted to a path using the `/aliases` table.

<a name="part1.4"></a>
### 1.4: Device Tree semantics

How to construct a Device Tree, and how best to use it to capture the configuration of some hardware, is a large and complex subject. There are many resources available, some of which are listed below, but several points deserve mentioning in this document:

`compatible` properties are the link between the hardware description and the driver software. When an OS encounters a node with a `compatible` property, it looks it up in its database of device drivers to find the best match. In Linux, this usually results in the driver module being automatically loaded, provided it has been appropriately labelled and not blacklisted.

The `status` property indicates whether a device is enabled or disabled. If the `status` is `ok`, `okay` or absent, then the device is enabled. Otherwise, `status` should be `disabled`, so that the device is disabled. It can be useful to place devices in a `.dtsi` file with the status set to `disabled`. A derived configuration can then include that `.dtsi` and set the status for the devices which are needed to `okay`.

<a name="part2"></a>
## Part 2: Device Tree overlays

A modern SoC (System on a Chip) is a very complicated device; a complete Device Tree could be hundreds of lines long. Taking that one step further and placing the SoC on a board with other components only makes matters worse. To keep that manageable, particularly if there are related devices that share components, it makes sense to put the common elements in `.dtsi` files, to be included from possibly multiple `.dts` files.

When a system like Raspberry Pi also supports optional plug-in accessories such as HATs, the problem grows. Ultimately, each possible configuration requires a Device Tree to describe it, but once you factor in all the different base models and the large number of available accessories, the number of combinations starts to multiply rapidly.

What is needed is a way to describe these optional components using a partial Device Tree, and then to be able to build a complete tree by taking a base DT and adding a number of optional elements. You can do this, and these optional elements are called "overlays".

Unless you want to learn how to write overlays for Raspberry Pis, you might prefer to skip on to [Part 3: Using Device Trees on Raspberry Pi](#part3).

<a name="part2.1"></a>
### 2.1: Fragments

A DT overlay comprises a number of fragments, each of which targets one node and its subnodes. Although the concept sounds simple enough, the syntax seems rather strange at first:

```
// Enable the i2s interface
/dts-v1/;
/plugin/;

/ {
    compatible = "brcm,bcm2835";

    fragment@0 {
        target = <&i2s>;
        __overlay__ {
            status = "okay";
            test_ref = <&test_label>;
            test_label: test_subnode {
                dummy;
            };
        };
    };
};
```

The `compatible` string identifies this as being for BCM2835, which is the base architecture for the Raspberry Pi SoCs; if the overlay makes use of features of a Pi 4 then `brcm,bcm2711` is the correct value to use, otherwise `brcm,bcm2835` can be used for all Pi overlays. Then comes the first (and in this case only) fragment. Fragments should be numbered sequentially from zero. Failure to adhere to this may cause some or all of your fragments to be missed.

Each fragment consists of two parts: a `target` property, identifying the node to apply the overlay to; and the `__overlay__` itself, the body of which is added to the target node. The example above can be interpreted as if it were written like this:

```
/dts-v1/;
/plugin/;

/ {
    compatible = "brcm,bcm2835";
};

&i2s {
    status = "okay";
    test_ref = <&test_label>;
    test_label: test_subnode {
        dummy;
    };
};
```
(In fact, with a sufficiently new version of `dtc` you can write it exactly like that and get identical output, but some homegrown tools don't understand this format yet so any overlay that you might want to be included in the standard Raspberry Pi OS kernel should be written in the old format for now).

The effect of merging that overlay with a standard Raspberry Pi base Device Tree (e.g. `bcm2708-rpi-b-plus.dtb`), provided the overlay is loaded afterwards, would be to enable the I2S interface by changing its status to `okay`. But if you try to compile this overlay using:

```
dtc -I dts -O dtb -o 2nd.dtbo 2nd-overlay.dts
```

you will get an error:

```
Label or path i2s not found
```

This shouldn't be too unexpected, since there is no reference to the base `.dtb` or `.dts` file to allow the compiler to find the `i2s` label.

Trying again, this time using the original example and adding the `-@` option to allow unresolved references (and `-Hepapr` to remove some clutter):

```
dtc -@ -Hepapr -I dts -O dtb -o 1st.dtbo 1st-overlay.dts
```

If `dtc` returns an error about the third line, it doesn't have the extensions required for overlay work. Run `sudo apt install device-tree-compiler` and try again - this time, compilation should complete successfully. Note that a suitable compiler is also available in the kernel tree as `scripts/dtc/dtc`, built when the `dtbs` make target is used:
```
make ARCH=arm dtbs
```

It is interesting to dump the contents of the DTB file to see what the compiler has generated:

```
$ fdtdump 1st.dtbo
/dts-v1/;
// magic:		0xd00dfeed
// totalsize:		0x207 (519)
// off_dt_struct:	0x38
// off_dt_strings:	0x1c8
// off_mem_rsvmap:	0x28
// version:		17
// last_comp_version:	16
// boot_cpuid_phys:	0x0
// size_dt_strings:	0x3f
// size_dt_struct:	0x190

/ {
    compatible = "brcm,bcm2835";
    fragment@0 {
        target = <0xffffffff>;
        __overlay__ {
            status = "okay";
            test_ref = <0x00000001>;
            test_subnode {
                dummy;
                phandle = <0x00000001>;
            };
        };
    };
    __symbols__ {
        test_label = "/fragment@0/__overlay__/test_subnode";
    };
    __fixups__ {
        i2s = "/fragment@0:target:0";
    };
    __local_fixups__ {
        fragment@0 {
            __overlay__ {
                test_ref = <0x00000000>;
            };
        };
    };
};
```

After the verbose description of the file structure there is our fragment. But look carefully - where we wrote `&i2s` it now says `0xffffffff`, a clue that something strange has happened (older versions of dtc might say `0xdeadbeef` instead). The compiler has also added a `phandle` property containing a unique (to this overlay) small integer to indicate that the node has a label, and replaced all references to the label with the same small integer.

After the fragment there are three new nodes:
* `__symbols__` lists the labels used in the overlay (`test_label` here), and the path to the labelled node. This node is the key to how unresolved symbols are dealt with.
* `__fixups__` contains a list of properties mapping the names of unresolved symbols to lists of paths to cells within the fragments that need patching with the phandle of the target node, once that target has been located. In this case, the path is to the `0xffffffff` value of `target`, but fragments can contain other unresolved references which would require additional fixes.
* `__local_fixups__` holds the locations of any references to labels that exist within the overlay - the `test_ref` property. This is required because the program performing the merge will have to ensure that phandle numbers are sequential and unique.

Back in [section 1.3](#part1_3) it says that "the original labels do not appear in the compiled output", but this isn't true when using the `-@` switch. Instead, every label results in a property in the `__symbols__` node, mapping a label to a path, exactly like the `aliases` node. In fact, the mechanism is so similar that when resolving symbols, the Raspberry Pi loader will search the "aliases" node in the absence of a `__symbols__` node. This was useful at one time because providing sufficient aliases allowed very old versions of `dtc` to be used to build the base DTB files, but fortunately that is ancient history now.

<a name="part2.2"></a>
### 2.2: Device Tree parameters

To avoid the need for lots of Device Tree overlays, and to reduce the need for users of peripherals to modify DTS files, the Raspberry Pi loader supports a new feature - Device Tree parameters. This permits small changes to the DT using named parameters, similar to the way kernel modules receive parameters from `modprobe` and the kernel command line. Parameters can be exposed by the base DTBs and by overlays, including HAT overlays.

Parameters are defined in the DTS by adding an `__overrides__` node to the root. It contains properties whose names are the chosen parameter names, and whose values are a sequence comprising a phandle (reference to a label) for the target node, and a string indicating the target property; string, integer (cell) and boolean properties are supported.

<a name="part2.2.1"></a>
#### 2.2.1: String parameters

String parameters are declared like this:

```
name = <&label>,"property";
```

where `label` and `property` are replaced by suitable values. String parameters can cause their target properties to grow, shrink, or be created.

Note that properties called `status` are treated specially; non-zero/true/yes/on values are converted to the string `"okay"`, while zero/false/no/off becomes `"disabled"`.

<a name="part2.2.2"></a>
#### 2.2.2: Integer parameters

Integer parameters are declared like this:

```
name = <&label>,"property.offset"; // 8-bit
name = <&label>,"property;offset"; // 16-bit
name = <&label>,"property:offset"; // 32-bit
name = <&label>,"property#offset"; // 64-bit
```

where `label`, `property` and `offset` are replaced by suitable values; the offset is specified in bytes relative to the start of the property (in decimal by default), and the preceding separator dictates the size of the parameter. In a change from earlier implementations, integer parameters may refer to non-existent properties or to offsets beyond the end of an existing property.

<a name="part2.2.3"></a>
#### 2.2.3: Boolean parameters

Device Tree encodes boolean values as zero-length properties; if present then the property is true, otherwise it is false. They are defined like this:

```
boolean_property; // Set 'boolean_property' to true
```

Note that a property is assigned the value `false` by not defining it. Boolean parameters are declared like this:

```
name = <&label>,"property?";
```

where `label` and `property` are replaced by suitable values.

Inverted booleans invert the input value before applying it in the same was as a regular boolean; they are declared similarly, but use `!` to indicate the inversion:

```
name = <&label>,"property!";
```

Boolean parameters can cause properties to be created or deleted, but they can't delete a property that already exists in the base DTB.

<a name="part2.2.4"></a>
#### 2.2.4: Byte string parameters

Byte string properties are arbitrary sequences of bytes, e.g. MAC addresses. They accept strings of hexadecimal bytes, with or without colons between the bytes.

```
mac_address = <&ethernet0>,"local_mac_address[";
```
The `[` was chosen to match the DT syntax for declaring a byte string:
```
local_mac_address = [aa bb cc dd ee ff];
```

<a name="part2.2.5"></a>
#### 2.2.5: Parameters with multiple targets

There are some situations where it is convenient to be able to set the same value in multiple locations within the Device Tree. Rather than the ungainly approach of creating multiple parameters, it is possible to add multiple targets to a single parameter by concatenating them, like this:

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
#### 2.2.6: Literal assignments

As seen in [2.2.5](#part2.2.5), the DT parameter mechanism allows multiple targets to be patched from the same parameter, but the utility is limited by the fact that the same value has to be written to all locations (except for format conversion and the negation available from inverted booleans). The addition of embedded literal assignments allows a parameter to write arbitrary values, regardless of the parameter value supplied by the user.

Assignments appear at the end of a declaration, and are indicated by a `=`:

```
str_val  = <&target>,"strprop=value";              // 1
int_val  = <&target>,"intprop:0=42                 // 2
int_val2 = <&target>,"intprop:0=",<42>;            // 3
bytes    = <&target>,"bytestr[=b8:27:eb:01:23:45"; // 4
```
Lines 1, 2 and 4 are fairly obvious, but line 3 is more interesting because the value appears as an integer (cell) value. The DT compiler evaluates integer expressions at compile time, which might be convenient (particularly if macro values are used), but the cell can also contain a reference to a label:
```
// Force an LED to use a GPIO on the internal GPIO controller.
exp_led = <&led1>,"gpios:0=",<&gpio>,
          <&led1>,"gpios:4";
```
When the overlay is applied, the label will be resolved against the base DTB in the usual way. Note that it is a good idea to split multi-part parameters over multiple lines like this to make them easier to read - something that becomes more necessary with the addition of cell value assignments like this.

Bear in mind that parameters do nothing unless they are applied - a default value in a lookup table is ignored unless the parameter name is used without assigning a value.

<a name="part2.2.7"></a>
#### 2.2.7: Lookup tables

Lookup tables allow parameter input values to be transformed before they are used. They act as associative arrays, rather like switch/case statements:
```
phonetic = <&node>,"letter{a=alpha,b=bravo,c=charlie,d,e,='tango uniform'}";
bus      = <&fragment>,"target:0{0=",<&i2c0>,"1=",<&i2c1>,"}";
```
A key with no `=value` means to use the key as the value, an `=` with no key before it is the default value in the case of no match, and starting or ending the list with a comma (or an empty key=value pair anywhere) indicates that the unmatched input value should be used unaltered; otherwise, not finding a match is an error.

Note that the comma separator within the table string after a cell integer value is implicit - adding one explicitly creates an empty pair (see above).

N.B. As lookup tables operate on input values and literal assigments ignore them, it's not possible to combine the two - characters after the closing `}` in the lookup declaration are treated as an error.

<a name="part2.2.8"></a>
#### 2.2.8 Overlay/fragment parameters

The DT parameter mechanism as described has a number of limitations, including the inability to change the name of a node and to write arbitrary values to arbitrary properties when a parameter is used. One way to overcome some of these limitations is to conditionally include or exclude certain fragments.

A fragment can be excluded from the final merge process (disabled) by renaming the `__overlay__` node to `__dormant__`. The parameter declaration syntax has been extended to allow the otherwise illegal zero target phandle to indicate that the following string contains operations at fragment or overlay scope. So far, four operations have been implemented:

```
+<n>    // Enable fragment <n>
-<n>    // Disable fragment <n>
=<n>    // Enable fragment <n> if the assigned parameter value is true, otherwise disable it
!<n>    // Enable fragment <n> if the assigned parameter value is false, otherwise disable it
```

Examples:
```
just_one    = <0>,"+1-2"; // Enable 1, disable 2
conditional = <0>,"=3!4"; // Enable 3, disable 4 if value is true,
                          // otherwise disable 3, enable 4.
```
The `i2c-rtc` overlay uses this technique.

<a name="part2.2.9"></a>
#### 2.2.9 Special properties

A few property names, when targeted by a parameter, get special handling. One you may have noticed already - `status` - which will convert a boolean to either `okay` for true and `disabled` for false.

Assigning to the `bootargs` property appends to it rather than overwriting it - this is how settings can be added to the kernel command line.

The `reg` property is used to specify device addresses - the location of a memory-mapped hardware block, the address on an I2C bus, etc. The names of child nodes should be qualified with their addresses in hexadecimal, using `@` as a separator:
```
        bmp280@76 {
            reg = <0x77>;
            ...
        };
```
When assigning to the `reg` property, the address portion of the parent node name will be replaced with the assigned value. This can be used to prevent a node name clash when using the same overlay multiple times - a technique used by the `i2c-gpio` overlay.

The `name` property is a pseudo-property - it shouldn't appear in a DT, but assigning to it causes the name of its parent node to be changed to the assigned value. Like the `reg` property, this can be used to give nodes unique names.

<a name="part2.2.10"></a>
#### 2.2.10 The overlay map file

The introduction of the Pi 4, built around the BCM2711 SoC, brought with it many changes; some of these changes are additional interfaces, and some are modifications to (or removals of) existing interfaces. There are new overlays intended specifically for the Pi 4 that don't make sense on older hardware, e.g. overlays that enable the new SPI, I2C and UART interfaces, but other overlays don't apply correctly even though they control features that are still relevant on the new device.

There is therefore a need for a method of tailoring an overlay to multiple platforms with differing hardware. Supporting them all in a single .dtbo file would require heavy use of hidden ("dormant") fragments and a switch to an on-demand symbol resolution mechanism so that a missing symbol that isn't needed doesn't cause a failure. A simpler solution is to add a facility to map an overlay name to one of several implementation files depending on the current platform.

The overlay map, which is rolling out with the switch to Linux 5.4, is a file that gets loaded by the firmware at bootup. It is written in DTS source format - `overlay_map.dts`, compiled to `overlay_map.dtb` and stored in the overlays directory.

This is an edited version of the current map file (the full version is available [here](https://github.com/raspberrypi/linux/blob/rpi-5.4.y/arch/arm/boot/dts/overlays/overlay_map.dts)):

```
/ {
    vc4-kms-v3d {
        bcm2835;
        bcm2711 = "vc4-kms-v3d-pi4";
    };

    vc4-kms-v3d-pi4 {
        bcm2711;
    };

    uart5 {
        bcm2711;
    };

    pi3-disable-bt {
        renamed = "disable-bt";
    };

    lirc-rpi {
        deprecated = "use gpio-ir";
    };
};
```

Each node has the name of an overlay that requires special handling. The properties of each node are either platform names or one of a small number of special directives. The current supported platforms are `bcm2835`, which includes all Pis built around the BCM2835, BCM2836 and BCM2837 SoCs, and `bcm2711` for Pi 4B.

A platform name with no value (an empty property) indicates that the current overlay is compatible with the platform; for example, `vc4-kms-v3d` is compatible with the `bcm2835` platform. A non-empty value for a platform is the name of an alternative overlay to use in place of the requested one; asking for `vc4-kms-v3d` on BCM2711 results in `vc4-kms-v3d-pi4` being loaded instead. Any platform not included in an overlay's node is not compatible with that overlay.

The second example node - `vc4-kms-v3d-pi4` - could be inferred from the content of `vc4-kms-v3d`, but that intelligence goes into the construction of the file, not its interpretation.

In the event that a platform is not listed for an overlay, one of the special directives may apply:

* The `renamed` directive indicates the new name of the overlay (which should be largely compatible with the original), but also logs a warning about the rename.

* The `deprecated` directive contains a brief explanatory error message which will be logged after the common prefix `overlay '...' is deprecated:`.

Remember: only exceptions need to be listed - the absence of a node for an overlay means that the default file should be used for all platforms.

Accessing diagnostic messages from the firmware is covered in [Debugging](#part4.1).

The `dtoverlay` and `dtmerge` utilities have been extended to support the map file:
* `dtmerge` extracts the platform name from the compatible string in the base DTB.
* `dtoverlay` reads the compatible string from the live Device Tree at `/proc/device-tree`, but you can use the `-p` option to supply an alternate platform name (useful for dry runs on a different platform).

They both send errors, warnings and any debug output to STDERR.

<a name="part2.2.11"></a>
#### 2.2.11 Examples

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
                mac = [01 23 45 67 89 ab];
                spi = <&spi0>;
            };
        };
    };

    fragment@1 {
        target-path = "/";
        __overlay__ {
            frag1;
        };
    };

    fragment@2 {
        target-path = "/";
        __dormant__ {
            frag2;
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
        bool1 =       <&test>,"bool1!";
        bool2 =       <&test>,"bool2?";
        entofr =      <&test>,"english",
                      <&test>,"french{hello=bonjour,goodbye='au revoir',weekend}";
        pi_mac =      <&test>,"mac[{1=b8273bfedcba,2=b8273b987654}";
        spibus =      <&test>,"spi:0[0=",<&spi0>,"1=",<&spi1>,"2=",<&spi2>;

        only1 =       <0>,"+1-2";
        only2 =       <0>,"-1+2";
        enable1 =     <0>,"=1";
        disable2 =    <0>,"!2";
    };
};
```

For further examples, there is a large collection of overlay source files hosted in the Raspberry Pi Linux GitHub repository [here](https://github.com/raspberrypi/linux/tree/rpi-5.4.y/arch/arm/boot/dts/overlays).

<a name="part2.3"></a>
### 2.3: Exporting labels

The overlay handling in the firmware and the run-time overlay application using the `dtoverlay` utility treat labels defined in an overlay as being private to that overlay. This avoids the need to invent globally unique names for labels (which keeps them short), and it allows the same overlay to be used multiple times without clashing (provided some tricks are used - see [Special properties](#part2.2.9)).

Sometimes, however, it is very useful to be able to create a label with one overlay and use it from another. Firmware released since 14th February 2020 has the ability to declare some labels as being global - the `__export__` node:
```
    ...
    public: ...

    __exports__ {
        public; // Export the label 'public' to the base DT
    };
};
```
When this overlay is applied, the loader strips out all symbols except those that have been exported, in this case `public`, and rewrites the path to make it relative to the target of the fragment containing the label. Overlays loaded after this one can then refer to `&public`.

<a name="part2.4"></a>
### 2.4: Overlay application order

Under most circumstances it shouldn't matter which order the fragments are applied, but for overlays that patch themselves (where the target of a fragment is a label in the overlay, known as an intra-overlay fragment) it becomes important. In older firmware, fragments are applied strictly in order, top to bottom. With firmware released since 14th February 2020, fragments are applied in two passes:

i. First the fragments that target other fragments are applied and hidden.
ii. Then the regular fragments are applied.

This split is particularly important for runtime overlays, since step (i) occurs in the `dtoverlay` utility, and step (ii) is performed by the kernel (which can't handle intra-overlay fragments).

<a name="part3"></a>
## Part 3: Using Device Trees on Raspberry Pi

<a name="part3.1"></a>
### 3.1: DTBs, overlays and config.txt

On a Raspberry Pi it is the job of the loader (one of the `start.elf` images) to combine overlays with an appropriate base device tree, and then to pass a fully resolved Device Tree to the kernel. The base Device Trees are located alongside `start.elf` in the FAT partition (/boot from Linux), named `bcm2711-rpi-4-b.dtb`, `bcm2710-rpi-3-b-plus.dtb`, etc. Note that some models (3A+, A, A+) will use the "b" equivalents (3B+, B, B+), respectively. This selection is automatic, and allows the same SD card image to be used in a variety of devices.

Note that DT and ATAGs are mutually exclusive, and passing a DT blob to a kernel that doesn't understand it will cause a boot failure. The firmware will always try to load the DT and pass it to the kernel, since all kernels since rpi-4.4.y will not function without a DTB. You can override this by adding `device_tree=` in config.txt, which forces the use of ATAGs, which can be useful for simple "bare-metal" kernels.

[ The firmware used to look for a trailer appended to kernels by the `mkknlimg` utility, but support for this has been withdrawn. ]

The loader now supports builds using bcm2835_defconfig, which selects the upstreamed BCM2835 support. This configuration will cause `bcm2835-rpi-b.dtb` and `bcm2835-rpi-b-plus.dtb` to be built. If these files are copied with the kernel, then the loader will attempt to load one of those DTBs by default.

In order to manage Device Tree and overlays, the loader supports a number of `config.txt` directives:

```
dtoverlay=acme-board
dtparam=foo=bar,level=42
```

This will cause the loader to look for `overlays/acme-board.dtbo` in the firmware partition, which Raspberry Pi OS mounts on `/boot`. It will then search for parameters `foo` and `level`, and assign the indicated values to them.

The loader will also search for an attached HAT with a programmed EEPROM, and load the supporting overlay from there - either directly or by name from the "overlays" directory; this happens without any user intervention.

There are several ways to tell that the kernel is using Device Tree:

1. The "Machine model:" kernel message during bootup has a board-specific value such as "Raspberry Pi 2 Model B", rather than "BCM2709".
2. `/proc/device-tree` exists, and contains subdirectories and files that exactly mirror the nodes and properties of the DT.

With a Device Tree, the kernel will automatically search for and load modules that support the indicated enabled devices. As a result, by creating an appropriate DT overlay for a device you save users of the device from having to edit `/etc/modules`; all of the configuration goes in `config.txt`, and in the case of a HAT, even that step is unnecessary. Note, however, that layered modules such as `i2c-dev` still need to be loaded explicitly.

The flipside is that because platform devices don't get created unless requested by the DTB, it should no longer be necessary to blacklist modules that used to be loaded as a result of platform devices defined in the board support code. In fact, current Raspberry Pi OS images ship with no blacklist files (except for some WLAN devices where multiple drivers are available).

<a name="part3.2"></a>
### 3.2: DT parameters

As described above, DT parameters are a convenient way to make small changes to a device's configuration. The current base DTBs support parameters for enabling and controlling the onboard audio, I2C, I2S and SPI interfaces without using dedicated overlays. In use, parameters look like this:

```
dtparam=audio=on,i2c_arm=on,i2c_arm_baudrate=400000,spi=on
```

Note that multiple assignments can be placed on the same line, but ensure you don't exceed the 80-character limit.

If you have an overlay that defines some parameters, they can be specified either on subsequent lines like this:

```
dtoverlay=lirc-rpi
dtparam=gpio_out_pin=16
dtparam=gpio_in_pin=17
dtparam=gpio_in_pull=down
```

or appended to the overlay line like this:

```
dtoverlay=lirc-rpi,gpio_out_pin=16,gpio_in_pin=17,gpio_in_pull=down
```

Overlay parameters are only in scope until the next overlay is loaded. In the event of a parameter with the same name being exported by both the overlay and the base, the parameter in the overlay takes precedence; for clarity, it's recommended that you avoid doing this. To expose the parameter exported by the base DTB instead, end the current overlay scope using:

```
dtoverlay=
```

<a name="part3.3"></a>
### 3.3: Board-specific labels and parameters

Raspberry Pi boards have two I2C interfaces. These are nominally split: one for the ARM, and one for VideoCore (the "GPU"). On almost all models, `i2c1` belongs to the ARM and `i2c0` to VC, where it is used to control the camera and read the HAT EEPROM. However, there are two early revisions of the Model B that have those roles reversed.

To make it possible to use one set of overlays and parameters with all Pis, the firmware creates some board-specific DT parameters. These are:

```
i2c/i2c_arm
i2c_vc
i2c_baudrate/i2c_arm_baudrate
i2c_vc_baudrate
```

These are aliases for `i2c0`, `i2c1`, `i2c0_baudrate`, and `i2c1_baudrate`. It is recommended that you only use `i2c_vc` and `i2c_vc_baudrate` if you really need to - for example, if you are programming a HAT EEPROM (which is better done using a software I2C bus using the `i2c-gpio` overlay). Enabling `i2c_vc` can stop the Pi Camera or 7" DSI display functioning correctly.

For people writing overlays, the same aliasing has been applied to the labels on the I2C DT nodes. Thus, you should write:

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
### 3.4: HATs and Device Tree

A Raspberry Pi HAT is an add-on board with an embedded EEPROM designed for a Raspberry Pi with a 40-pin header. The EEPROM includes any DT overlay required to enable the board (or the name of an overlay to load from the filing system), and this overlay can also expose parameters.

The HAT overlay is automatically loaded by the firmware after the base DTB, so its parameters are accessible until any other overlays are loaded, or until the overlay scope is ended using `dtoverlay=`. If for some reason you want to suppress the loading of the HAT overlay, put `dtoverlay=` before any other `dtoverlay` or `dtparam` directive.

<a name="part3.5"></a>
### 3.5: Dynamic Device Tree

As of Linux 4.4, the RPi kernels support the dynamic loading of overlays and parameters. Compatible kernels manage a stack of overlays that are applied on top of the base DTB. Changes are immediately reflected in `/proc/device-tree` and can cause modules to be loaded and platform devices to be created and destroyed.

The use of the word "stack" above is important - overlays can only be added and removed at the top of the stack; changing something further down the stack requires that anything on top of it must first be removed.

There are some new commands for managing overlays:

<a name="part3.5.1"></a>
#### 3.5.1 The dtoverlay command

`dtoverlay` is a command line utility that loads and removes overlays while the system is running, as well as listing the available overlays and displaying their help information:

```
pi@raspberrypi ~ $ dtoverlay -h
Usage:
  dtoverlay <overlay> [<param>=<val>...]
                           Add an overlay (with parameters)
  dtoverlay -D [<idx>]     Dry-run (prepare overlay, but don't apply -
                           save it as dry-run.dtbo)
  dtoverlay -r [<overlay>] Remove an overlay (by name, index or the last)
  dtoverlay -R [<overlay>] Remove from an overlay (by name, index or all)
  dtoverlay -l             List active overlays/params
  dtoverlay -a             List all overlays (marking the active)
  dtoverlay -h             Show this usage message
  dtoverlay -h <overlay>   Display help on an overlay
  dtoverlay -h <overlay> <param>..  Or its parameters
    where <overlay> is the name of an overlay or 'dtparam' for dtparams
Options applicable to most variants:
    -d <dir>    Specify an alternate location for the overlays
                (defaults to /boot/overlays or /flash/overlays)
    -v          Verbose operation
```

Unlike the `config.txt` equivalent, all parameters to an overlay must be included in the same command line - the [dtparam](#part3.5.2) command is only for parameters of the base DTB.

Two points to note:
1. Command variants that change kernel state (adding and removing things) require root privilege, so you may need to prefix the command with `sudo`.

2. Only overlays and parameters applied at run-time can be unloaded - an overlay or parameter applied by the firmware becomes "baked in" such that it won't be listed by `dtoverlay` and can't be removed.

<a name="part3.5.2"></a>
#### 3.5.2 The dtparam command

`dtparam` creates and loads an overlay that has largely the same effect as using a dtparam directive in `config.txt`. In usage it is largely equivalent to `dtoverlay` with an overlay name of `-`, but there are a few differences:

1. `dtparam` will list the help information for all known parameters of the base DTB. Help on the dtparam command is still available using `dtparam -h`.

2. When indicating a parameter for removal, only index numbers can be used (not names).

3. Not all Linux subsystems respond to the addition of devices at runtime - I2C, SPI and sound devices work, but some won't.

<a name="part3.5.3"></a>
#### 3.5.3 Guidelines for writing runtime-capable overlays

This area is poorly documented, but here are some accumulated tips:

* The creation or deletion of a device object is triggered by a node being added or removed, or by the status of a node changing from disabled to enabled or vice versa. Beware - the absence of a "status" property means the node is enabled.

* Don't create a node within a fragment that will overwrite an existing node in the base DTB - the kernel will rename the new node to make it unique. If you want to change the properties of an existing node, create a fragment that targets it.

* ALSA doesn't prevent its codecs and other components from being unloaded while they are in use. Removing an overlay can cause a kernel exception if it deletes a codec that is still being used by a sound card. Experimentation found that devices are deleted in the reverse of fragment order in the overlay, so placing the node for the card after the nodes for the components allows an orderly shutdown.

<a name="part3.5.4"></a>
#### 3.5.4 Caveats

The loading of overlays at runtime is a recent addition to the kernel, and so far there is no accepted way to do this from userspace. By hiding the details of this mechanism behind commands the aim is to insulate users from changes in the event that a different kernel interface becomes standardised.

* Some overlays work better at run-time than others. Parts of the Device Tree are only used at boot time - changing them using an overlay will not have any effect.

* Applying or removing some overlays may cause unexpected behaviour, so it should be done with caution. This is one of the reasons it requires `sudo`.

* Unloading the overlay for an ALSA card can stall if something is actively using ALSA - the LXPanel volume slider plugin demonstrates this effect. To enable overlays for sound cards to be removed, the `lxpanelctl` utility has been given two new options - `alsastop` and `alsastart` - and these are called from the auxiliary scripts `dtoverlay-pre` and `dtoverlay-post` before and after overlays are loaded or unloaded, respectively.

* Removing an overlay will not cause a loaded module to be unloaded, but it may cause the reference count of some modules to drop to zero. Running `rmmod -a` twice will cause unused modules to be unloaded.

* Overlays have to be removed in reverse order. The commands will allow you to remove an earlier one, but all the intermediate ones will be removed and re-applied, which may have unintended consequences.

* Only Device Tree nodes at the top level of the tree and children of a bus node will be probed. For nodes added at run-time there is the further limitation that the bus must register for notifications of the addition and removal of children. However, there are exceptions that break this rule and cause confusion: the kernel explicitly scans the entire tree for some device types - clocks and interrupt controller being the two main ones - in order to (for clocks) initialise them early and/or (for interrupt controllers) in a particular order. This search mechanism only happens during booting and so doesn't work for nodes added by an overlay at run-time. It is therefore recommended for overlays to place fixed-clock nodes in the root of the tree unless it is guaranteed that the overlay will not be used at run-time.

<a name="part3.6"></a>
### 3.6: Supported overlays and parameters

As it is too time-consuming to document the individual overlays here, please refer to the [README](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README) file found alongside the overlay `.dtbo` files in `/boot/overlays`. It is kept up-to-date with additions and changes.

<a name="part4"></a>
## Part 4: Troubleshooting and pro tips

<a name="part4.1"></a>
### 4.1: Debugging

The loader will skip over missing overlays and bad parameters, but if there are serious errors, such as a missing or corrupt base DTB or a failed overlay merge, then the loader will fall back to a non-DT boot. If this happens, or if your settings don't behave as you expect, it is worth checking for warnings or errors from the loader:

```
sudo vcdbg log msg
```

Extra debugging can be enabled by adding `dtdebug=1` to `config.txt`.

You can create a human-readable representation of the current state of DT like this:

```
dtc -I fs /proc/device-tree
```

This can be useful to see the effect of merging overlays onto the underlying tree.

If kernel modules don't load as expected, check that they aren't blacklisted in `/etc/modprobe.d/raspi-blacklist.conf`; blacklisting shouldn't be necessary when using Device Tree. If that shows nothing untoward, you can also check that the module is exporting the correct aliases by searching `/lib/modules/<version>/modules.alias` for the `compatible` value. Otherwise, your driver is probably missing either:

```
.of_match_table = xxx_of_match,
```

or:

```
MODULE_DEVICE_TABLE(of, xxx_of_match);
```

Failing that, `depmod` has failed or the updated modules haven't been installed on the target filesystem.

<a name="part4.2"></a>
### 4.2: Testing overlays using dtmerge, dtdiff and ovmerge

Alongside the `dtoverlay` and `dtparam` commands is a utility for applying an overlay to a DTB - `dtmerge`. To use it you first need to obtain your base DTB, which can be obtained in one of two ways:

a) generate it from the live DT state in `/proc/device-tree`:
```
dtc -I fs -O dtb -o base.dtb /proc/device-tree
```
This will include any overlays and parameters you have applied so far, either in `config.txt` or by loading them at runtime, which may or may not be what you want. Alternatively...

b) copy it from the source DTBs in /boot. This won't include overlays and parameters, but it also won't include any other modifications by the firmware. To allow testing of all overlays, the `dtmerge` utility will create some of the board-specific aliases ("i2c_arm", etc.), but this means that the result of a merge will include more differences from the original DTB than you might expect. The solution to this is to use dtmerge to make the copy:

```
dtmerge /boot/bcm2710-rpi-3-b.dtb base.dtb -
```

(the `-` indicates an absent overlay name).

You can now try applying an overlay or parameter:

```
dtmerge base.dtb merged.dtb - sd_overclock=62
dtdiff base.dtb merged.dtb
```

which will return:
```
--- /dev/fd/63  2016-05-16 14:48:26.396024813 +0100
+++ /dev/fd/62  2016-05-16 14:48:26.396024813 +0100
@@ -594,7 +594,7 @@
                };

                sdhost@7e202000 {
-                       brcm,overclock-50 = <0x0>;
+                       brcm,overclock-50 = <0x3e>;
                        brcm,pio-limit = <0x1>;
                        bus-width = <0x4>;
                        clocks = <0x8>;
```

You can also compare different overlays or parameters.

```
dtmerge base.dtb merged1.dtb /boot/overlays/spi1-1cs.dtbo
dtmerge base.dtb merged2.dtb /boot/overlays/spi1-2cs.dtbo
dtdiff merged1.dtb merged2.dtb
```

to get:

```
--- /dev/fd/63  2016-05-16 14:18:56.189634286 +0100
+++ /dev/fd/62  2016-05-16 14:18:56.189634286 +0100
@@ -453,7 +453,7 @@

                        spi1_cs_pins {
                                brcm,function = <0x1>;
-                               brcm,pins = <0x12>;
+                               brcm,pins = <0x12 0x11>;
                                phandle = <0x3e>;
                        };

@@ -725,7 +725,7 @@
                        #size-cells = <0x0>;
                        clocks = <0x13 0x1>;
                        compatible = "brcm,bcm2835-aux-spi";
-                       cs-gpios = <0xc 0x12 0x1>;
+                       cs-gpios = <0xc 0x12 0x1 0xc 0x11 0x1>;
                        interrupts = <0x1 0x1d>;
                        linux,phandle = <0x30>;
                        phandle = <0x30>;
@@ -743,6 +743,16 @@
                                spi-max-frequency = <0x7a120>;
                                status = "okay";
                        };
+
+                       spidev@1 {
+                               #address-cells = <0x1>;
+                               #size-cells = <0x0>;
+                               compatible = "spidev";
+                               phandle = <0x41>;
+                               reg = <0x1>;
+                               spi-max-frequency = <0x7a120>;
+                               status = "okay";
+                       };
                };

                spi@7e2150C0 {
```

The [Utils](https://github.com/raspberrypi/utils) repo includes another DT utility - `ovmerge`. Unlike `dtmerge`, `ovmerge` combines file and applies overlays in source form. Because the overlay is never compiled, labels are preserved and the result is usually more readable. It also has a number of other tricks, such as the ability to list the order of file inclusion.

<a name="part4.3"></a>
### 4.3: Forcing a specific Device Tree

If you have very specific needs that aren't supported by the default DTBs, or if you just want to experiment with writing your own DTs, you can tell the loader to load an alternate DTB file like this:

```
device_tree=my-pi.dtb
```

<a name="part4.4"></a>
### 4.4: Disabling Device Tree usage

Since the switch to the 4.4 kernel and the use of more upstream drivers, Device Tree usage is required in Pi Linux kernels. However, for bare metal and other OSs, the method of disabling DT usage is to add:

```
device_tree=
```

to `config.txt`.

<a name="part4.5"></a>
### 4.5: Shortcuts and syntax variants

The loader understands a few shortcuts:

```
dtparam=i2c_arm=on
dtparam=i2s=on
```

can be shortened to:

```
dtparam=i2c,i2s
```

(`i2c` is an alias of `i2c_arm`, and the `=on` is assumed). It also still accepts the long-form versions: `device_tree_overlay` and `device_tree_param`.

<a name="part4.6"></a>
### 4.6: Other DT commands available in config.txt

`device_tree_address`
This is used to override the address where the firmware loads the device tree (not dt-blob). By default the firmware will choose a suitable place.

`device_tree_end`
This sets an (exclusive) limit to the loaded device tree. By default the device tree can grow to the end of usable memory, which is almost certainly what is required.

`dtdebug`
If non-zero, turn on some extra logging for the firmware's device tree processing.

`enable_uart`
Enable the primary/console UART (ttyS0 on a Pi 3, ttyAMA0 otherwise - unless swapped with an overlay such as miniuart-bt). If the primary UART is ttyAMA0 then enable_uart defaults to 1 (enabled), otherwise it defaults to 0 (disabled). This is because it is necessary to stop the core frequency from changing which would make ttyS0 unusable, so `enable_uart=1` implies core_freq=250 (unless force_turbo=1). In some cases this is a performance hit, so it is off by default. More details on UARTs can be found [here](uart.md)

`overlay_prefix`
Specifies a subdirectory/prefix from which to load overlays - defaults to "overlays/". Note the trailing "/". If desired you can add something after the final "/" to add a prefix to each file, although this is not likely to be needed.

Further ports can be controlled by the DT, for more details see [section 3](#part3).

<a name="part4.7"></a>
### 4.7 Further help

If you've read through this document and not found the answer to a Device Tree problem, there is help available. The author can usually be found on Raspberry Pi forums, particularly the [Device Tree](https://www.raspberrypi.org/forums/viewforum.php?f=107) forum.
