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
usage: xqemurun [-h] [--config FILE] [--dir DIRECTORY] [--bin FILE]
                [--display DISPLAY] [--qemudebug OPTION] [--mesadebug OPTION]
                [--egldebug OPTION] [--gldebug OPTION] [--glsoftware DRIVER]
                [--vsync OPTION] [--kvm OPTION] [--xdk SOCKET]
                [--short OPTION] [--machine OPTION] [--bootrom FILE]
                [--bios FILE] [--disk FILE] [--hub OPTION] [--pad1 OPTION]
                [--pad2 OPTION] [--pad3 OPTION] [--pad4 OPTION]
                [FILE]

xqemurun helps to run xqemu easily.

positional arguments:
  FILE                 path to media iso, default: none

optional arguments:
  -h, --help           show this help message and exit
  --config FILE        path to config file, default:
                       ~/.config/xqemurun/config.ini
  --dir DIRECTORY      directory from where to run XQEMU binary, default: none
  --bin FILE           XQEMU binary, default: qemu-system-xbox
  --display DISPLAY    graphical display, default: sdl
  --qemudebug OPTION   QEMU debug mode, default: disabled
  --mesadebug OPTION   Mesa debug info printing, default: disabled
  --egldebug OPTION    EGL debug info printing, default: disabled
  --gldebug OPTION     OpenGL debug info printing, default: disabled
  --glsoftware DRIVER  OpenGL software rendering, default: disabled
  --vsync OPTION       Vertical sync mode, default: system
  --kvm OPTION         enable KVM acceleration, default: disabled
  --xdk SOCKET         path to socket file for XDK serial port, default: none
  --short OPTION       skip the logo animation, default: disabled
  --machine OPTION     machine type, default: xbox
  --bootrom FILE       path to bootrom dump, default: none
  --bios FILE          path to bios dump, default: none
  --disk FILE          path to disk image, default: none
  --hub OPTION         usb hub option, default: emulated
  --pad1 OPTION        usb pad1 device option, default: keyboard
  --pad2 OPTION        usb pad2 device option, default: disabled
  --pad3 OPTION        usb pad3 device option, default: disabled
  --pad4 OPTION        usb pad4 device option, default: disabled
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
