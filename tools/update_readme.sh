#! /bin/sh

# generate a README.md file with up-to-date built-in help.

test -f "README.md" && rm "README.md"
exec 1<&-
exec 1<>"README.md"

cat <<\EOF
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
EOF

src/xqemurun.py --help | sed -e 's/xqemurun.py/xqemurun/'

cat <<\EOF
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
EOF

#EOF
