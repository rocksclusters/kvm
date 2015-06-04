# $Id: __init__.py,v 1.10 2013/01/30 19:27:35 clem Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#

import os
import re
import syslog

import sys
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import rocks.commands
import rocks.db.vmextend
import rocks.db.mappings.kvm

class Command(rocks.commands.report.host.command):
	"""
	Reports the XML Configuration for VM that will be handed
	to libvirt for startup.	

	<arg type='string' name='host' repeat='1'>
	One or more VM host names.
	</arg>

	<example cmd='report host vm config compute-0-0-0'>
	list the XML configuration of Report XML Config of VM compute-0-0-0.
	</example>

	"""

	def getDisks(self, node):
		"""return the xml snippet regarding the disks section of the 
		given node"""

		returnxml = []
		idedevices = []

		for disk in node.vm_defs.disks:
			#
			# if the disk specification is a 'regular' file, then
			# make sure the file for the disk space exists. if
			# it doesn't, create a sparse file for the disk space.
			#
			file = os.path.join(disk.prefix, disk.name)

			if disk.vbd_type in [ 'file', 'qcow2', 'qed' ]:
				a = "    <disk type='file' device='disk'>"
				returnxml.append(a)

				if disk.vbd_type == 'file':
					#default
					a = "      <driver name='qemu' type='raw'/>"
				elif disk.vbd_type == 'qcow2':
					a = "      <driver name='qemu' type='qcow2'/>"
				elif disk.vbd_type == 'qed':
					a = "      <driver name='qemu' type='qed'/>"
				returnxml.append(a)
				#elif disk.vbd_type == 'tap:aio':
				#	a = "<driver name='tap' type='aio'/>"

				a = "      <source file='%s'/>" % file
				returnxml.append(a)

			elif disk.vbd_type == 'phy':
				a = "    <disk type='block' device='disk'>"
				returnxml.append(a)

				a = "      <source dev='%s'/>" % file
				returnxml.append(a)
			else:
				self.abort("Disk type is not valid. Please see rocks add host vm help.")

			# we misuse the mode column to carry the driver name 
			# that needs to should be used to expese the disk 
			if disk.mode == 'w':
				# default driver
				# legacy for backward compatibility
				bus = 'virtio'
			else:
				bus = disk.mode

			a = "      <target dev='%s' bus='%s'/>" % (disk.device, bus)
			if disk.device == 'ide':
				idedevices.append(disk.device)
			returnxml.append(a)

			a = "    </disk>"
			returnxml.append(a)

		#
		# check for a CDROM
		#
		cdrom_path = node.vm_defs.cdrom_path
		if cdrom_path:
			returnxml.append("<disk type='file' device='cdrom'>")
			returnxml.append("  <driver name='qemu' type='raw'/>")
			if cdrom_path.startswith('/dev'):
				# block device
				returnxml.append("  <source dev='%s'/>" % cdrom_path)
			else:
				# we assume it is a ISO file
				returnxml.append("  <source file='%s'/>" % cdrom_path)
			# find the ide device
			for i in ['a', 'b', 'c', 'd']:
				device = 'hd' + i
				if device not in idedevices:
					break
			returnxml.append("  <target dev='%s' bus='ide'/>"% device)
			returnxml.append("  <readonly/>")
			returnxml.append("</disk>")

		return returnxml


	def getInterfaces(self, node):
		"""return the xml snippet relative to the interfaces"""

		returnxml = []

		# we have to type of interface:
		# - tap interface (or directly attached interface): that have not 
		#   connectivity with the host
		# - bridged interface: these are attached through a standard bridge

		for tap_inter in self.newdb.getPhysTapDevicefromVnode(node):
			returnxml.append("    <interface type='direct'>")
			# we need to attach to the pyshical interface which starts with p
			options = tap_inter["options"]
			if options is not None and options.find("novtap") >= 0:
				prefix = ""
			else:
				prefix = "p"
			dev = prefix + tap_inter["device"] + "." + str(tap_inter["vlanID"])
			returnxml.append("      <source dev='%s' mode='bridge'/>" % dev )
			returnxml.append("      <mac address='%s'/>" % tap_inter["mac"])
			returnxml.append("      <model type='virtio' />")
			returnxml.append("    </interface>")

		for bridged_inter in self.newdb.getPhysBridgedDevicefromVnode(node):
			if bridged_inter["module"] == 'ovs-link':
				continue
			returnxml.append("    <interface type='bridge'>")
			returnxml.append("      <source bridge='%s'/>" % bridged_inter["device"])
			returnxml.append("      <mac address='%s'/>" % bridged_inter["mac"])
			if bridged_inter["module"] == 'ovs-bridge':
				returnxml.append("      <virtualport type='openvswitch'/>")
			else:
				returnxml.append("      <model type='virtio'/>")
			returnxml.append("    </interface>")

		return returnxml


	def getCpuMem(self, node):
		"""return the xml snippet relative to the cpu and memory 
		In particular the memory, vcpu, cpu, cputune, and feature tags.
		"""

		xmlconfig = []

		xmlconfig.append("  <memory>%s</memory>" % (node.vm_defs.mem * 1024))
		xmlconfig.append("  <vcpu>%s</vcpu>" % node.cpus)

		# cpu_mode you can specify the capabilities of the virtual cpu
		# host-passthrough should be the default for speed
		# if after the cpu_mode there is a : then the remaining of the
		# attribute value is used as a string for inner content of the
		# <cpu> </cpu> tag
		cpu_mode = self.newdb.getHostAttr(node, 'cpu_mode')
		if cpu_mode :
			cpu_match_split = cpu_mode.split(':', 1)
			if len(cpu_match_split) > 1:
				# cpu mode contains inner tag of cpus
				xmlconfig.append("  <cpu mode='" + cpu_match_split[0] + "'>")
				xmlconfig.append( cpu_match_split[1] )
				xmlconfig.append("  </cpu>")
			else:
				xmlconfig.append("  <cpu mode='" +
						cpu_mode + "'/>")

		# for cpu pinning
		attribute = self.newdb.getHostAttr(node, 'kvm_cpu_pinning')
		if attribute == "pin_all":
			xmlconfig.append("  <cputune>")
			for i in range(node.cpus):
			        xmlconfig.append("    <vcpupin vcpu=\"%d\" cpuset=\"%d\"/>" % (i, i))
			xmlconfig.append("  </cputune>")
		elif attribute:
			xmlconfig.append(attribute)

		if node.vm_defs.virt_type == 'hvm':
			features = self.newdb.getHostAttr(node,'HVM_Features')
			if features is None :
				features = """    <acpi/>\n    <apic/>\n    <pae/>"""
			xmlconfig.append("  <features>")
			xmlconfig.append(features)
			xmlconfig.append("  </features>")
		return xmlconfig


	def reportBootLoader(self, node):
		"""first section of the libvirt xml with the startup params"""

		returnxml = []
		returnxml.append("  <os>")
		returnxml.append("    <type>hvm</type>")

                #let's check out the boot action
		if not node.boot:
			#that's bad!
			self.abort('Host ' + node.name + ' doesn\'t have a boot action...')

		if node.installaction == "install vm frontend" and node.boot.action == 'install':
			#action == 'install' and installAction == install vm fronend
			#aka we are installing a frontend
			#1. anaconda kernel and ramdisk
			#2. network info to fetch stage2 from http server
			# Read the profile
			

			session = self.newdb.getSession()
			bootaction = rocks.db.mappings.base.Bootaction.loadOne(
					session, action = node.installaction)
			bootargs = bootaction.args
			ip = None
			netmask = None
			dns = None
			gateway = None
			mac = None
			if node.name in self.getHostnames( [ 'frontend' ]):
				subnet = 'public'
				for network in node.networks:
					if network.subnet.name == 'public':
						ip = network.ip
						netmask = network.subnet.netmask
						mac = network.mac
				
				dns = self.newdb.getHostAttr(node,
					'Kickstart_PublicDNSServers')
				
				for (key, val) in self.db.getHostRoutes(node.name).items():
					if key == '0.0.0.0' and val[0] == '0.0.0.0':
						gateway = val[1]
			
			if ip:
				bootargs += ' ip=%s ' % ip
			if netmask:
				bootargs += ' netmask=%s ' % netmask
			if dns:
			        #
			        # the user can enter in multiple DNS servers that are
			        # separated by a comma. we can only supply one DNS
			        # to anaconda, so let's just select the first one.
			        #
			        bootargs += ' dns=%s ' % dns.split(',')[0]
			if gateway:
			        bootargs += ' gateway=%s ' % gateway
			
			if mac:
				bootargs = bootargs.replace("ksdevice=eth1","ksdevice=%s" % mac)
			returnxml.append("    <kernel>%s</kernel>" % bootaction.kernel )
			returnxml.append("    <initrd>%s</initrd>" % bootaction.ramdisk )
			returnxml.append("    <cmdline>%s</cmdline>" % bootargs )
			returnxml.append("  </os>")
			returnxml.append("  <on_reboot>destroy</on_reboot>")
		else:
			#we boot the machine as if normal hardware
			if node.vm_defs.cdrom_path :
				returnxml.append("    <boot dev='cdrom'/>")
			returnxml.append("    <boot dev='network'/>")
			returnxml.append("    <boot dev='hd'/>")
			returnxml.append("    <bootmenu enable='yes'/>")
			returnxml.append("  </os>")
		return returnxml


	def runXMLPlugin(self, plugins, name, node, xml):
		"""if a plugin named name exist run it and return its xml if
		it does not exist return unmodified xml"""
                for plugin in plugins:
                        if name in plugin.__module__:
				syslog.syslog(syslog.LOG_INFO, 
						'PLUGIN (report host vm config) %s'
						% plugin.__module__)
				return plugin.run(node, xml)
		return xml


	def getXMLconfig(self, node):
		"""main function it buils the full libvirt xml for the given
		node and it returns it"""

		plugins = self.loadPlugins()

		xmlconfig = []
		xmlconfig.append("<domain type='kvm'>")
		xmlconfig.append("  <name>%s</name>" % node.name)

		xmlconfig = xmlconfig + self.runXMLPlugin(plugins, 'plugin_bootloader',
			node, self.reportBootLoader(node))

		xmlconfig = xmlconfig + self.runXMLPlugin(plugins, 'plugin_cpumem',
			node, self.getCpuMem(node))

		#
		# configure the devices
		#
		devicexml = []
		devicexml.append("  <devices>")
		devicexml.append("    <emulator>/usr/libexec/qemu-kvm</emulator>")

		# network config
		devicexml = devicexml + self.runXMLPlugin(plugins, 'plugin_interface',
			node, self.getInterfaces(node))

		# add the disk config
		devicexml = devicexml + self.runXMLPlugin(plugins, 'plugin_disk',
			node, self.getDisks(node))

		# additional devices set with attributes
		i = 0
		while True:
			attribute = self.newdb.getHostAttr(node, 'kvm_device_%d' % i)
			i = i + 1
			if attribute :
				devicexml.append(attribute)
			else:
				break

		# the extra devices
		devicexml.append("    <graphics type='vnc' port='-1' keymap='en-us'/>")
		devicexml.append("    <console tty='/dev/pts/0'/>")
		devicexml.append("  </devices>")
		xmlconfig = xmlconfig + self.runXMLPlugin(plugins, 'plugin_device',
                        node, devicexml)

		xmlconfig.append("</domain>")

		# the last one is the global plugin
		xmlconfig =  self.runXMLPlugin(plugins, 'plugin_global', node, xmlconfig)
		return '\n'.join(xmlconfig)


	def run(self, params, args):


		if len(args) < 1:
			self.abort('must supply at least one host')

		self.beginOutput()
		for node in self.newdb.getNodesfromNames(args, preload = 
				['vm_defs', 'vm_defs.disks', 'networks', 
				'networks.subnet', 'boot']):
			#
			# get the VM configuration (in XML format for libvirt)
			#
			if not node.vm_defs:
				continue
			xmlconfig = self.getXMLconfig(node)
			self.addOutput(node.name, '%s' % xmlconfig)
		self.endOutput(padChar='')

