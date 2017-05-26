#! /usr/bin/env python3
#-*- coding: UTF-8 -*-

### Legal
#
# Author:  Thomas DEBESSE <dev@illwieckz.net>
# License: ISC
# 

import argparse
import os
import subprocess
import configparser
import xdg.BaseDirectory
import distutils.spawn
from collections import OrderedDict

class ConfigFile():
	def __init__(self):
		self.parser = configparser.ConfigParser()
		self.modified = False

	def getKey(self, section, key):
		if not section in self.parser:
			return None

		if not key in self.parser[section]:
			return None

		return self.parser[section][key]

	def setKey(self, section, key, value):
		if not section in self.parser:
			self.parser.add_section(section)

		self.parser[section][key] = value
		self.modified = True

	def setDefaultFile(self, config_path):
		self.config_path = config_path

	def readDefault(self):
		self.readFile(self.config_path)

	def readFile(self, config_path):
		if os.path.isfile(config_path):
			print("reading config file: " + config_path)
			self.parser.read(config_path)

	def writeDefault(self):
		self.writeFile(self.config_path)

	def conditionalWriteDefault(self):
		if self.modified:
			self.writeDefault()
			self.modified = False

	def writeFile(self, config_path):
		with open(self.config_path, 'w') as configfile:
			print("writing config file: " + config_path)
			self.parser.write(configfile)

	def importConfig(self, config_file):
		for section in config_file.parser.sections():
			for key in config_file.parser[section]:
				self.setKey(section, key, config_file.getKey(section, key))

class XQEMURun():
	def __init__(self):
		self.config_base_dir_name = "xqemurun"
		self.config_base_file_name = "config.ini"
		self.config_path = os.path.join(xdg.BaseDirectory.xdg_config_home, self.config_base_dir_name, self.config_base_file_name)
		self.config_file = ConfigFile()
		self.config_runtime = ConfigFile()
		self.disabled  = [ "disabled", "off", "no", "none" ]
		bin_path = distutils.spawn.find_executable("qemu-system-xbox")
		if bin_path:
			self.config_runtime.setKey("bin", "bin", bin_path)

	def main(self):
		args = argparse.ArgumentParser(description="%(prog)s helps to run xqemu easily.")
		args.add_argument("--config", dest="config", metavar="FILE", help="path to config file")
		args.add_argument("--dir", dest="dir", metavar="DIR", help="directory from where to run XQEMU binary, default: none")
		args.add_argument("--qemu", dest="qemu", metavar="FILE", help="path to XQEMU binary, default: qemu-system-xbox")
		args.add_argument("--gdb", dest="gdb", metavar="OPTION", help="enable GDB debug, default: no")
		args.add_argument("--kvm", dest="kvm", metavar="OPTION", help="enable KVM, default: no")
		args.add_argument("--xdk", dest="xdk", metavar="SOCKET", help="path to socket file for XDK serial port, default: none")
		args.add_argument("--machine", dest="machine", metavar="OPTION", help="machine type, default: xbox")
		args.add_argument("--short", dest="short", metavar="OPTION", help="skip the logo animation, default: no")
		args.add_argument("--bootrom", dest="bootrom", metavar="FILE", help="path to bootrom dump")
		args.add_argument("--bios", dest="bios", metavar="FILE", help="path to bios dump")
		args.add_argument("--disk", dest="disk", metavar="FILE", help="path to disk image")
		args.add_argument("--hub", dest="hub", metavar="OPTION", help="usb hub option, default: emulated")
		args.add_argument("--pad1", dest="pad1", metavar="OPTION", help="usb pad1 device option, default: keyboard")
		args.add_argument("--pad2", dest="pad2", metavar="OPTION", help="usb pad2 device option")
		args.add_argument("--pad3", dest="pad3", metavar="OPTION", help="usb pad3 device option")
		args.add_argument("--pad4", dest="pad4", metavar="OPTION", help="usb pad4 device option")
		args.add_argument("media", nargs='?', metavar="FILE", help="path to media iso")

		args = args.parse_args()

		if args.config:
			self.config_path = os.path.abspath(args.config)

		self.config_file.setDefaultFile(self.config_path)

		for xdg_config_dir_path in reversed(xdg.BaseDirectory.xdg_config_dirs):
			config_file_path = os.path.join(xdg_config_dir_path, self.config_base_dir_name, self.config_base_file_name)
			if config_file_path != self.config_path:
				self.config_file.readFile(config_file_path)
				self.config_runtime.importConfig(self.config_file)

		print("default config file: " + self.config_path)
		if os.path.isfile(self.config_path):
			self.config_file.readDefault()
			self.config_runtime.importConfig(self.config_file)
		else:
			print("default config file not there")

		if args.dir:
			if args.dir in self.disabled:
				self.config_runtime.setKey("bin", "dir", "none")
			else:
				self.config_runtime.setKey("bin", "dir", os.path.abspath(args.dir))

		if args.qemu:
			self.config_runtime.setKey("bin", "bin", os.path.abspath(args.qemu))

		if args.gdb:
			if args.gdb in self.disabled:
				self.config_runtime.setKey("core", "gdb", "no")
			else:
				self.config_runtime.setKey("core", "gdb", "yes")

		if args.kvm:
			if args.gdb in self.disabled:
				self.config_runtime.setKey("core", "kvm", "no")
			else:
				self.config_runtime.setKey("core", "kvm", "yes")

		if args.xdk:
			if args.xdk in self.disabled:
				self.config_runtime.setKey("core", "xdk", args.xdk)
			else:
				self.config_runtime.setKey("core", "xdk", os.path.abspath(args.xdk))

		if args.machine:
			self.config_runtime.setKey("core", "machine", args.machine)

		if args.short:
			self.config_runtime.setKey("core", "short", args.short)

		if args.bootrom:
			self.config_runtime.setKey("sys", "bootrom", os.path.abspath(args.bootrom))

		if args.bios:
			self.config_runtime.setKey("sys", "bios", os.path.abspath(args.bios))

		if args.disk:
			if args.disk in self.disabled:
				self.config_runtime.setKey("sys", "disk", "none")
			else:
				self.config_runtime.setKey("sys", "disk", os.path.abspath(args.disk))

		if args.media:
			if args.media in self.disabled:
				self.config_runtime.setKey("sys", "media", "none")
			else:
				self.config_runtime.setKey("sys", "media", os.path.abspath(args.media))

		if args.hub:
			self.config_runtime.setKey("usb", "hub", args.hub)

		if args.pad1:
			self.config_runtime.setKey("usb", "pad1", args.pad1)

		if args.pad2:
			self.config_runtime.setKey("usb", "pad2", args.pad2)

		if args.pad3:
			self.config_runtime.setKey("usb", "pad3", args.pad3)

		if args.pad4:
			self.config_runtime.setKey("usb", "pad4", args.pad4)

		self.cli()

	def cli(self):

		alteredConfig = False

		machine = self.config_runtime.getKey("core", "machine")

		if not machine:
			machine = input("machine [xbox]:")

			if machine == "":
				machine = "xbox"

			if machine not in [ "xbox", "chihiro" ]:
				raise(Exception("UnknownMachine"))

			self.config_runtime.setKey("core", "machine", machine)
			self.config_file.setKey("core", "machine", machine)

		if not self.config_runtime.getKey("bin", "bin"):
			bin_path = input("path to qemu: ") 
			self.config_runtime.setKey("bin", "bin", bin_path)
			self.config_file.setKey("bin", "bin", bin_path)

		if not self.config_runtime.getKey(machine, "bootrom"):
			bootrom_path = input("path to bootrom dump: ")
			self.config_runtime.setKey(machine, "bootrom", bootrom_path)
			self.config_file.setKey(machine, "bootrom", bootrom_path)

		if not self.config_runtime.getKey(machine, "bios"):
			bios_path = input("path to bios dump: ")
			self.config_runtime.setKey(machine, "bios", bios_path)
			self.config_file.setKey(machine, "bios", bios_path)

		self.config_file.conditionalWriteDefault()

		self.qemu()

	def qemu(self):
		qemu_command = []

		qemu_dir_path = self.config_runtime.getKey("bin", "dir")
		if not qemu_dir_path or qemu_dir_path in self.disabled:
			qemu_dir_path = os.path.abspath(".")

		machine = self.config_runtime.getKey("core", "machine")
		print("machine type: " + machine)

		print("qemu execution directory: " + qemu_dir_path)

		qemu_bin_path = self.config_runtime.getKey("bin", "bin")
		print("qemu path: " + qemu_bin_path)

		qemu_command += [ qemu_bin_path ]

		if self.config_runtime.getKey("core", "gdb") == "yes":
			print("gdb debug: enabled")
			qemu_command += [ "-s", "-S" ]
		else:
			print("gdb debug: disabled")

		if self.config_runtime.getKey("core", "kvm") == "yes":
			print("kvm: enabled")
			kvm_enabled = True
		else:
			print("kvm: disabled")
			kvm_enabled = False

		xdk_socket = self.config_runtime.getKey("core", "xdk")
		if xdk_socket and xdk_socket not in self.disabled:
			print("xdk: " + xdk_socket)
		else:
			print("xdk: disabled")
			xdk_socket = None

		qemu_cpu_arg="pentium3"
		qemu_command += [ "-cpu", qemu_cpu_arg ]

		qemu_machine_arg = machine

		if machine == "chihiro":
			print("memory: 128Mb")
			qemu_memory_arg="128"
			mediaboard_path = self.config_runtime.getKey(machine, "bootrom")
			print("mediaboard dump: " + mediaboard_path)
			qemu_machine_arg += ",mediaboard_rom=" + mediaboard_path

		else:
			print("memory: 64Mb")
			qemu_memory_arg="64"
			bootrom_path = self.config_runtime.getKey(machine, "bootrom")
			print("bootrom dump: " + bootrom_path)
			qemu_machine_arg += ",bootrom=" + bootrom_path

		qemu_command += [ "-m", qemu_memory_arg ]

		if xdk_socket:
			qemu_xdk_socket_arg = "unix:" + xdk_socket
			qemu_command += [ "-device", "lpc47m157", "-serial", qemu_xdk_socket_arg ]

		if kvm_enabled:
			qemu_machine_arg += ",accel=kvm,kernel_irqchip=off"

		if self.config_runtime.getKey("core", "short") == "yes":
			print("skip logo animation: yes")
			qemu_machine_arg += ",short_animation"
		else:
			print("skip logo animation: no")

		qemu_command += [ "-machine", qemu_machine_arg ]

		bios_path = self.config_runtime.getKey(machine, "bios")
		print("bios dump: " + bios_path)
		qemu_bios_arg = bios_path
		qemu_command += [ "-bios", qemu_bios_arg ]

		if machine == "xbox":
			qemu_disk_arg = "index=0,media=disk,locked=on"
			disk_path = self.config_runtime.getKey(machine, "disk")

			if disk_path and disk_path not in self.disabled:
				print("disk image: " + disk_path)
				qemu_disk_arg += ",file=" + disk_path
			else:
				print("disk image: none")
				qemu_disk_arg += ",file=/dev/zero"

			qemu_command += [ "-drive", qemu_disk_arg ]

		qemu_media_arg = "index=1,media=cdrom"

		media_path = self.config_runtime.getKey(machine, "media")
		if media_path and media_path not in self.disabled:
			print("media iso: " + media_path)
			qemu_media_arg += ",file=" + media_path
		else:
			print("media iso: none")

		qemu_command +=	[ "-drive", qemu_media_arg ]

		pad_dict = OrderedDict()
		pad_dict["pad1"] = "3"
		pad_dict["pad2"] = "4"
		pad_dict["pad3"] = "1"
		pad_dict["pad4"] = "2"

		usb_hub_option = self.config_runtime.getKey("usb", "hub")
		if not usb_hub_option:
			usb_hub_option = "emulated"

		if usb_hub_option == "emulated":
			print("usb hub: emulated")
			qemu_usb_hub_device_arg = "usb-hub,bus=usb-bus.0,port=3"
			qemu_command += [ "-usb", "-device", qemu_usb_hub_device_arg ]

		elif usb_hub_option[0:8] == "forward:":
			print("usb hub: " + usb_hub_option)
			usb_product_id = usb_hub_option[8:13]
			usb_vendor_id = usb_hub_option[14:19]
			qemu_usb_hub_device_arg = "usb-host,bus=usb-bus.0,port=3,product_id=" + usb_product_id + ",vendorid=" + usb_vendor_id
			qemu_command += [ "-usb", "-device", qemu_usb_hub_device_arg ]

		if usb_hub_option == "emulated":
			for pad in pad_dict.keys():
				usb_pad_option = self.config_runtime.getKey("usb", "usb_" + pad)
				if not usb_pad_option:
					if pad == "pad1":
						usb_pad_option = "keyboard"
					else:
						usb_pad_option = "disabled"

				if usb_pad_option == "keyboard":
					print("usb " + pad + ": keyboard")
					qemu_usb_pad_device_arg = "usb-xbox-gamepad,bus=usb-bus.0,port=" + pad_dict[pad] + ".2"
					qemu_command += [ "-device", qemu_usb_pad_device_arg ]

				elif usb_pad_option[0:8] == "forward:":
					print("usb " + pad + ": " + usb_pad_option)
					usb_product_id = usb_hub_option[8:13]
					usb_vendor_id = usb_hub_option[14:19]
					qemu_usb_pad_device_arg = "usb-host,bus=usb-bus.0,port=3.2,product_id=" + usb_product_id + ",vendorid=" + usb_vendor_id
					qemu_command += [ "-usb", "-device", qemu_usb_hub_device_arg ]

		print("qemu command line : " + str(qemu_command))

		os.chdir(qemu_dir_path)
		subprocess.call(qemu_command)

if __name__ == "__main__":
	xqemurun = XQEMURun()
	xqemurun.main()
