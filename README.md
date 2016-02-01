XQEMURun
========

![XQEMU](http://dl.illwieckz.net/b/xqemu/20160201-074350.xqemu.png)

Description
-----------

This is a simple wrapper for the [XQEMU](https://github.com/espes/xqemu) binary. It helps you to run it easily. XQEMURun does nothing by itself, all the good work on XQEMU is brought to you by [espes](https://github.com/espes) himself.

If you run `xqemurun` without option and something required is missing, it will ask you for required files and write a config file for you.

Once configured (see [config.ini](sample/config.ini) for all options available), you can run any iso you want this way:

```sh
xqemurun media.iso
```

Greetings
---------

Thanks to the awesome [XQEMU](http://xqemu.com/) project and special thanks to espes for what he is doing.

Installation
------------

```
sudo make install
```

Help
----

```
usage: xqemurun [-h] [--config FILE] [--dir DIR] [--qemu FILE]
                   [--gdb OPTION] [--kvm OPTION] [--xdk SOCKET]
                   [--machine OPTION] [--short OPTION] [--bootrom FILE]
                   [--bios FILE] [--disk FILE] [--hub OPTION] [--pad1 OPTION]
                   [--pad2 OPTION] [--pad3 OPTION] [--pad4 OPTION]
                   [FILE]

xqemurun helps to run xqemu easily.

positional arguments:
  FILE              path to media iso

optional arguments:
  -h, --help        show this help message and exit
  --config FILE     path to config file
  --dir DIR         directory from where to run XQEMU binary, default: none
  --qemu FILE       path to XQEMU binary, default: qemu-system-xbox
  --gdb OPTION      enable GDB debug, default: no
  --kvm OPTION      enable KVM, default: no
  --xdk SOCKET      path to socket file for XDK serial port, default: none
  --machine OPTION  machine type, default: xbox
  --short OPTION    skip the logo animation, default: no
  --bootrom FILE    path to bootrom dump
  --bios FILE       path to bios dump
  --disk FILE       path to disk image
  --hub OPTION      usb hub option, default: emulated
  --pad1 OPTION     usb pad1 device option, default: keyboard
  --pad2 OPTION     usb pad2 device option
  --pad3 OPTION     usb pad3 device option
  --pad4 OPTION     usb pad4 device option
