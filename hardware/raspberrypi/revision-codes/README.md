# Raspberry Pi revision codes

Each distinct Raspberry Pi model revision has a unique revision code. You can look up a Raspberry Pi's revision code by running:

```bash
cat /proc/cpuinfo
```

The last three lines show the hardware type, the revision code, and the Pi's unique serial number. For example:

```
Hardware    : BCM2835
Revision    : a02082
Serial      : 00000000765fc593
```

*Note: As of the 4.9 kernel, all Pis report `BCM2835`, even those with BCM2836, BCM2837 and BCM2711 processors. You should not use this string to detect the processor. Decode the revision code using the information below, or `cat /sys/firmware/devicetree/base/model`*

## Old-style revision codes

The first set of Raspberry Pi revisions were given sequential hex revision codes from `0002` to `0015`:

| Code | Model | Revision | RAM             | Manufacturer |
| ---- | ----- | -------- | --------------- | ------------ |
| 0002 | B     | 1.0      | 256MB          | Egoman       |
| 0003 | B     | 1.0      | 256MB          | Egoman       |
| 0004 | B     | 2.0      | 256MB          | Sony UK      |
| 0005 | B     | 2.0      | 256MB          | Qisda        |
| 0006 | B     | 2.0      | 256MB          | Egoman       |
| 0007 | A     | 2.0      | 256MB          | Egoman       |
| 0008 | A     | 2.0      | 256MB          | Sony UK      |
| 0009 | A     | 2.0      | 256MB          | Qisda        |
| 000d | B     | 2.0      | 512MB          | Egoman       |
| 000e | B     | 2.0      | 512MB          | Sony UK      |
| 000f | B     | 2.0      | 512MB          | Egoman       |
| 0010 | B+    | 1.2      | 512MB          | Sony UK      |
| 0011 | CM1   | 1.0      | 512MB          | Sony UK      |
| 0012 | A+    | 1.1      | 256MB          | Sony UK      |
| 0013 | B+    | 1.2      | 512MB          | Embest       |
| 0014 | CM1   | 1.0      | 512MB          | Embest       |
| 0015 | A+    | 1.1      | 256MB/512MB | Embest       |

## New-style revision codes

With the launch of the Raspberry Pi 2, new-style revision codes were introduced. Rather than being sequential, each bit of the hex code represents a piece of information about the revision:

```
uuuuuuuuFMMMCCCCPPPPTTTTTTTTRRRR
```

| Part     | Represents   | Options                    |
| -------- | ------------ | -------------------------- |
| uuuuuuuu | Unused       | Unused                     |
| F        | New flag     | 1: new-style revision      |
|          |              | 0: old-style revision      |
| MMM      | Memory size  | 0: 256MB                  |
|          |              | 1: 512MB                  |
|          |              | 2: 1GB                    |
|          |              | 3: 2GB                    |
|          |              | 4: 4GB                    |
| CCCC     | Manufacturer | 0: Sony UK                 |
|          |              | 1: Egoman                  |
|          |              | 2: Embest                  |
|          |              | 3: Sony Japan              |
|          |              | 4: Embest                  |
|          |              | 5: Stadium                 |
| PPPP     | Processor    | 0: BCM2835                 |
|          |              | 1: BCM2836                 |
|          |              | 2: BCM2837                 |
|          |              | 3: BCM2711                 |
| TTTTTTTT | Type         | 0: A                       |
|          |              | 1: B                       |
|          |              | 2: A+                      |
|          |              | 3: B+                      |
|          |              | 4: 2B                      |
|          |              | 5: Alpha (early prototype) |
|          |              | 6: CM1                     |
|          |              | 8: 3B                      |
|          |              | 9: Zero                    |
|          |              | a: CM3                     |
|          |              | c: Zero W                  |
|          |              | d: 3B+                     |
|          |              | e: 3A+                     |
|          |              | f: Internal use only       |
|          |              | 10: CM3+                   |
|          |              | 11: 4B                     |
| RRRR     | Revision     | 0, 1, 2, etc.              |

New-style revision codes in use:

| Code   | Model             | Revision | RAM    | Manufacturer |
| ------ | ----------------- | -------- | -------| ------------ |
| 900021 | A+                | 1.1      | 512MB | Sony UK      |
| 900032 | B+                | 1.2      | 512MB | Sony UK      |
| 900092 | Zero              | 1.2      | 512MB | Sony UK      |
| 900093 | Zero              | 1.3      | 512MB | Sony UK      |
| 9000c1 | Zero W            | 1.1      | 512MB | Sony UK      |
| 9020e0 | 3A+               | 1.0      | 512MB | Sony UK      |
| 920092 | Zero              | 1.2      | 512MB | Embest       |
| 920093 | Zero              | 1.3      | 512MB | Embest       |
| 900061 | CM                | 1.1      | 512MB | Sony UK      |
| a01040 | 2B                | 1.0      | 1GB   | Sony UK      |
| a01041 | 2B                | 1.1      | 1GB   | Sony UK      |
| a02082 | 3B                | 1.2      | 1GB   | Sony UK      |
| a020a0 | CM3               | 1.0      | 1GB   | Sony UK      |
| a020d3 | 3B+               | 1.3      | 1GB   | Sony UK      |
| a02042 | 2B (with BCM2837) | 1.2      | 1GB   | Sony UK      |
| a21041 | 2B                | 1.1      | 1GB   | Embest       |
| a22042 | 2B (with BCM2837) | 1.2      | 1GB   | Embest       |
| a22082 | 3B                | 1.2      | 1GB   | Embest       |
| a220a0 | CM3               | 1.0      | 1GB   | Embest       |
| a32082 | 3B                | 1.2      | 1GB   | Sony Japan   |
| a52082 | 3B                | 1.2      | 1GB   | Stadium      |
| a22083 | 3B                | 1.3      | 1GB   | Embest       |
| a02100 | CM3+              | 1.0      | 1GB   | Sony UK      |
| a03111 | 4B                | 1.1      | 1GB   | Sony UK      |
| b03111 | 4B                | 1.1      | 2GB   | Sony UK      |
| c03111 | 4B                | 1.1      | 4GB   | Sony UK      |
