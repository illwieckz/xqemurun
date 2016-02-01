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
		qemu_bin_path = distutils.spawn.find_executable("qemu-system-xbox")
		if qemu_bin_path:
			self.config_runtime.setKey("bin", "qemu_bin", qemu_bin_path)
		self.config_runtime.setKey("bin", "qemu_dir", os.path.abspath("."))

	def main(self):
		args = argparse.ArgumentParser(description="%(prog)s helps to run xqemu easily.")
		args.add_argument("--qemu", dest="qemu", metavar="FILE", help="path to xqemu binary, default: qemu-system-xbox")
		args.add_argument("--config", dest="config", metavar="FILE", help="path to config file")
		args.add_argument("--enable-kvm", dest="enable_kvm", metavar="OPTION", help="enable kvm, default: no")
		args.add_argument("--bios", dest="bios", metavar="FILE", help="path to bios dump")
		args.add_argument("--bootrom", dest="bootrom", metavar="FILE", help="path to bootrom dump")
		args.add_argument("--disk", dest="disk", metavar="FILE", help="path to disk image")
		args.add_argument("--usbhub", dest="usbhub", metavar="OPTION", help="usb hub option, default: emulated")
		args.add_argument("--pad1", dest="pad1", metavar="OPTION", help="pad1 device option, default: keyboard")
		args.add_argument("--pad2", dest="pad2", metavar="OPTION", help="pad2 device option")
		args.add_argument("--pad3", dest="pad3", metavar="OPTION", help="pad3 device option")
		args.add_argument("--pad4", dest="pad4", metavar="OPTION", help="pad4 device option")
		args.add_argument("iso", nargs='?', metavar="FILE", help="path to media iso")

		args = args.parse_args()

		if args.config:
			self.config_path = os.path.abspath(args.config)

		self.config_file.setDefaultFile(self.config_path)

		for xdg_config_dir_path in reversed(xdg.BaseDirectory.xdg_config_dirs):
			config_file_path = os.path.join(xdg_config_dir_path, self.config_base_dir_name, self.config_base_file_name)
			if config_file_path != self.config_path:
				self.config_file.readFile(config_file_path)
				self.config_runtime.importConfig(self.config_file)

		print("Default config file: " + self.config_path)
		if os.path.isfile(self.config_path):
			self.config_file.readDefault()
			self.config_runtime.importConfig(self.config_file)
		else:
			print("Default config file not there")

		if args.enable_kvm == "yes":
			self.config_runtime.setKey("core", "kvm_enabled", "yes")

		if args.qemu:
			self.config_runtime.setKey("bin", "qemu_bin", os.path.abspath(args.qemu))

		if args.bootrom:
			self.config_runtime.setKey("sys", "bootrom_dump", os.path.abspath(args.bootrom))

		if args.bios:
			self.config_runtime.setKey("sys", "bios_dump", os.path.abspath(args.bios))

		if args.disk:
			self.config_runtime.setKey("sys", "disk_image", os.path.abspath(args.disk))

		if args.usbhub:
			self.config_runtime.setKey("usb", "usb_hub", args.usbhub)

		if args.pad1:
			self.config_runtime.setKey("usb", "usb_pad1", args.pad1)

		if args.pad2:
			self.config_runtime.setKey("usb", "usb_pad2", args.pad2)

		if args.pad3:
			self.config_runtime.setKey("usb", "usb_pad3", args.pad3)

		if args.pad4:
			self.config_runtime.setKey("usb", "usb_pad4", args.pad4)

		if args.iso:
			self.config_runtime.setKey("sys", "media_image", os.path.abspath(args.iso))

		self.cli()

	def cli(self):

		alteredConfig = False
		if not self.config_runtime.getKey("bin", "qemu_bin"):
			qemu_bin_path = input("path to qemu: ") 
			self.config_runtime.setKey("bin", "qemu_bin", qemu_bin_path)
			self.config_file.setKey("bin", "qemu_bin", qemu_bin_path)

		if not self.config_runtime.getKey("sys", "bootrom_dump"):
			bootrom_dump_path = input("path to bootrom dump: ")
			self.config_runtime.setKey("sys", "bootrom_dump", bootrom_dump_path)
			self.config_file.setKey("sys", "bootrom_dump", bootrom_dump_path)

		if not self.config_runtime.getKey("sys", "bios_dump"):
			bios_dump_path = input("path to bios dump: ")
			self.config_runtime.setKey("sys", "bios_dump", bios_dump_path)
			self.config_file.setKey("sys", "bios_dump", bios_dump_path)

		self.config_file.conditionalWriteDefault()

		self.qemu()

	def qemu(self):
		qemu_command = []

		qemu_dir_path = self.config_runtime.getKey("bin", "qemu_dir")
		print("qemu execution directory: " + qemu_dir_path)

		qemu_bin_path = self.config_runtime.getKey("bin", "qemu_bin")
		print("qemu path: " + qemu_bin_path)

		qemu_command.append(qemu_bin_path)

		qemu_cpu_arg="pentium3"
		qemu_command += [ "-cpu", qemu_cpu_arg ]

		qemu_memory_arg="64"
		qemu_command += [ "-m", qemu_memory_arg ]

		qemu_machine_arg = "xbox"
		if self.config_runtime.getKey("core", "kvm_enabled") == "yes":
			print("kvm: enabled")
			qemu_machine_arg += ",accel=kvm,kernel_irqchip=off"
		else:
			print("kvm: disabled")

		bootrom_dump_path = self.config_runtime.getKey("sys", "bootrom_dump")
		print("bootrom dump: " + bootrom_dump_path)
		qemu_machine_arg += ",bootrom=" + bootrom_dump_path
		qemu_command += [ "-machine", qemu_machine_arg ]

		bios_dump_path = self.config_runtime.getKey("sys", "bios_dump")
		print("bios dump: " + bios_dump_path)
		qemu_bios_arg = bios_dump_path
		qemu_command += [ "-bios", qemu_bios_arg ]

		qemu_disk_arg = "index=0,media=disk,locked=on"
		disk_image_path = self.config_runtime.getKey("sys", "disk_image")
		if disk_image_path:
			print("disk image: " + disk_image_path)
			qemu_disk_arg += ",file=" + disk_image_path
		else:
			print("disk image: none")
			qemu_disk_arg += ",file=/dev/zero"

		qemu_command += [ "-drive", qemu_disk_arg ]

		qemu_media_arg = "index=1,media=cdrom"
		media_iso_path = self.config_runtime.getKey("sys", "media_iso")
		if media_iso_path:
			print("media iso: " + media_iso_path)
			qemu_media_arg += ",file=" + media_iso_path
		else:
			print("media iso: none")

		qemu_command +=	[ "-drive", qemu_media_arg ]

		pad_dict = OrderedDict()
		pad_dict["pad1"] = "3"
		pad_dict["pad2"] = "4"
		pad_dict["pad3"] = "1"
		pad_dict["pad4"] = "2"

		usb_hub_option = self.config_runtime.getKey("usb", "usb_hub")
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
