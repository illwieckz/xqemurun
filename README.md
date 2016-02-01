XQEMURun
========

![XQEMU](http://dl.illwieckz.net/b/xqemu/20160128-111444.xqemu.png)

Description
-----------

This is a simple wrapper for the [XQEMU](https://github.com/espes/xqemu) binary. It helps you to run it easily. XQEMURun does nothing by itself, all the good work on XQEMU is brought to you by [espes](https://github.com/espes) himself.

If you run `xqemurun` without option and something required is missing, it will ask you for required files and write a config file for you.

Once configured (see [config.ini](sample/config.ini) for all options available), you can run any iso you like this way:

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
usage: xqemurun [-h] [--qemu FILE] [--config FILE] [--enable-kvm {yes,no}]
                   [--bios FILE] [--bootrom FILE] [--disk FILE]
                   [FILE]

xqemurun helps to run xqemu easily.

positional arguments:
  FILE                  path to media iso

optional arguments:
  -h, --help            show this help message and exit
  --qemu FILE           path to xqemu binary
  --config FILE         path to config file
  --enable-kvm {yes,no}
                        enable kvm, default: no
  --bios FILE           path to bios dump
  --bootrom FILE        path to bootrom dump
  --disk FILE           path to disk image
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
