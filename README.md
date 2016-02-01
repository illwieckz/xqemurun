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
usage: xqemurun [-h] [--qemu FILE] [--config FILE] [--enable-kvm OPTION]
                [--bios FILE] [--bootrom FILE] [--disk FILE] [--usbhub OPTION]
                [--pad1 OPTION] [--pad2 OPTION] [--pad3 OPTION]
                [--pad4 OPTION]
                [FILE]

xqemurun helps to run xqemu easily.

positional arguments:
  FILE                 path to media iso

optional arguments:
  -h, --help           show this help message and exit
  --qemu FILE          path to xqemu binary, default: qemu-system-xbox
  --config FILE        path to config file
  --enable-kvm OPTION  enable kvm, default: no
  --bios FILE          path to bios dump
  --bootrom FILE       path to bootrom dump
  --disk FILE          path to disk image
  --usbhub OPTION      usb hub option, default: emulated
  --pad1 OPTION        pad1 device option, default: keyboard
  --pad2 OPTION        pad2 device option
  --pad3 OPTION        pad3 device option
  --pad4 OPTION        pad4 device option
```

Warning
-------

XQEMU is in a very early state, do not expect so much.

No warranty is given, use this at your own risk.

Author
------

Thomas Debesse <dev@illwieckz.net>

Copyright
---------

This tool is distributed under the highly permissive and laconic [ISC License](COPYING.md).
