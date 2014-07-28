# $Id: __init__.py,v 1.8 2012/11/27 00:49:07 phil Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
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
# $Log: __init__.py,v $
# Revision 1.8  2012/11/27 00:49:07  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.7  2012/08/29 01:39:55  clem
# Rework of the disk management in kvm
#
# - Now it support qcow2 format (default is still raw
#
# - Now it is also possible to specify the device used to
#   expose the disk inside the virtual machine
#
# - added some docs on the new disk string format
#
# Revision 1.6  2012/05/06 05:49:15  phil
# Copyright Storm for Mamba
#
# Revision 1.5  2012/04/13 02:25:22  clem
# some nimor fixes to the documentation of the command
#
# Revision 1.4  2012/04/06 19:25:48  clem
# install headless so rocks-console works
#
# Revision 1.3  2012/04/05 21:17:53  clem
# Minor error in the add host vm
#
# Revision 1.2  2012/03/31 01:07:28  clem
# latest version of the networking for kvm (vlan out of redhat network script)
# minor fixes here and there to change the disks path from /state/partition1/xen/disks
# to /state/partition1/kvm/disks
#
# Revision 1.1  2012/03/17 02:52:29  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.38  2011/07/23 02:31:43  phil
# Viper Copyright
#
# Revision 1.37  2011/06/23 20:29:07  phil
# Call add.host command instead of inserting manually.
#
# Revision 1.36  2011/02/14 04:19:14  phil
# Now support HVM as well as paravirtual instances.
# Preliminary testing on 64bit complete.
#
# Revision 1.35  2010/09/07 23:53:32  bruno
# star power for gb
#
# Revision 1.34  2009/11/13 23:22:52  bruno
# another fix from federico sacerdoti. if an IP address is specified on the
# command line, need to make sure it is single quoted.
#
# Revision 1.33  2009/11/13 21:42:39  bruno
# fix from federico sacerdoti to enable using physical devices (partitions,
# LVM partitions, etc.) as devices for virtual disks.
#
# Revision 1.32  2009/07/28 17:52:20  bruno
# be consistent -- all references to 'vlanid' should be 'vlan'
#
# Revision 1.31  2009/06/30 17:15:50  bruno
# one more time
#
# Revision 1.30  2009/06/30 16:59:38  bruno
# move code to correct location
#
# Revision 1.29  2009/06/30 16:30:26  bruno
# fixes to support for virtual compute nodes that are managed by a
# physical frontend
#
# Revision 1.28  2009/05/01 19:07:33  mjk
# chimi con queso
#
# Revision 1.27  2009/02/13 18:38:34  bruno
# ensure the locally administered bit is set and the multicast bit is not
# set in the first MAC octet
#
# Revision 1.26  2009/02/12 05:15:36  bruno
# add and remove virtual clusters faster
#
# Revision 1.25  2009/02/11 19:03:50  bruno
# create a locally administered base mac address that will be used by VMs.
#
# this address is based on the public IP of the frontend.
#
# Revision 1.24  2009/01/14 00:20:55  bruno
# unify the physical node and VM node boot action functionality
#
# - all bootaction's are global
#
# - the node table has a 'runaction' (what bootaction should the node do when
#   a node normally boots) and an 'installaction (the bootaction for installs).
#
# - the 'boot' table has an entry for each node and it dictates what the node
#   will do on the next boot -- it will look up the runaction in the nodes table
#   (for a normal boot) or the installaction in the nodes table (for an install).
#
# Revision 1.23  2009/01/07 18:55:51  bruno
# doc touchup
#
# Revision 1.22  2008/12/16 00:45:05  bruno
# merge vm_profiles and pxeaction tables into bootaction table
#
# Revision 1.21  2008/10/31 19:56:55  bruno
# one more fix
#
# Revision 1.20  2008/10/18 00:56:22  mjk
# copyright 5.1
#
# Revision 1.19  2008/09/04 15:54:16  bruno
# xen tweaks
#
# Revision 1.18  2008/08/20 22:52:58  bruno
# install a virtual cluster of any size in 6 simple steps!
#
# Revision 1.17  2008/07/29 16:47:24  bruno
# more vlan support for xen VMs
#
# Revision 1.16  2008/04/21 16:37:35  bruno
# nuked the vm_macs table -- now using the networks table to store/retrieve
# mac addresses for VMs
#
# Revision 1.15  2008/04/17 16:38:21  bruno
# incorporate phil's vm changes
#
# Revision 1.14  2008/04/15 20:29:16  bruno
# 'name' parameter now works
#
# Revision 1.13  2008/04/15 20:02:35  bruno
# now can use 'num-macs' parameter
#
# Revision 1.12  2008/03/12 19:30:08  bruno
# change default virtual block device (vbd) from tap:aio to file (file is
# more stable)
#
# Revision 1.11  2008/03/06 23:42:04  mjk
# copyright storm on
#
# Revision 1.10  2008/02/12 00:01:25  bruno
# fixes
#
# Revision 1.9  2008/02/08 23:29:59  bruno
# tune
#
# Revision 1.8  2008/02/07 20:08:24  bruno
# retooled the commands and database tables to handle moving running VMs
#
# Revision 1.7  2008/02/02 00:27:24  bruno
# can create multiple VMs with one command
#
# Revision 1.6  2008/02/01 21:38:54  bruno
# closer
#
# Revision 1.5  2008/01/30 22:01:34  bruno
# closer
#
# Revision 1.4  2008/01/30 01:46:58  bruno
# remove hardcode of '/state/partition1' for location of xen configuration
# files.
#
# if no disk specification is set, select the largest partition.
#
# Revision 1.3  2008/01/24 22:28:18  bruno
# change default file spec to 'tap:aio'
#
# Revision 1.2  2007/12/10 20:59:25  bruno
# fixes to get a VMs configured and running on newly installed xen-based
# physical machines.
#
# Revision 1.1  2007/12/03 19:48:51  bruno
# xen for V
#
#

import sys
import string
import os
import os.path
import IPy

import rocks.commands
import rocks.vm
from rocks.db.mappings.base import *
from rocks.db.mappings.kvm import *



def parseDisk(disk):
	"""parse a string representing a disk and returns a touple with
	the various components. Used by rocks set host vm."""

	dict={}

	d = disk.split(',')
	if len(d) != 3:
                rocks.commands.Abort('Invalid disk specification.'
				' Please see rocks add host vm help.')

	dict['device'] = d[1]
	dict['mode'] = d[2]

	e = d[0].split(':')
	dict['vbd_type'] = ':'.join(e[0:-1])

	if dict['vbd_type'] == 'phy':
		dict['prefix'] = ''
		dict['name'] = e[-1]	# allows for '/' in name for LVM
	else:
		dict['prefix'] = os.path.dirname(e[-1])
		dict['name'] = os.path.basename(e[-1])

	return dict



class Command(rocks.commands.HostArgumentProcessor, rocks.commands.add.command):
	"""
	Add a VM specification to the database.
	
	<arg type='string' name='host' optional='0' repeat='1'>
	One or more physical host names.
	</arg>

	<arg type='string' name='membership' optional='0'>
	The membership to assign to the VM.
	</arg>

	<param type='string' name='membership'>
	Can be used in place of the membership argument.
	</param>

	<param type='string' name='virt-type'>
	Virtualization Type. With the kvm roll only hvm is 
	a valid value.
	</param>

	<param type='string' name='name'>
	The name to assign to the VM (e.g., 'compute-0-0-0').
	</param>

	<param type='string' name='ip'>
	The IP address to assign to the VM.
	If no IP address is provided, then one will be automatically assigned.
	</param>

	<param type='string' name='subnet'>
	The subnet to associate to this VM.
	The default is: private.
	</param>

	<param type='string' name='mem'>
	The amount of memory in megabytes to assign to this VM.
	The default is: 1024.
	</param>

	<param type='string' name='cpus'>
	The number of CPUs to assign to this VM.
	The default is: 1.
	</param>

	<param type='string' name='slice'>
	The 'slice' id on the physical node. Each VM on a physical node has
	a unique slice number
	The default is the next available free slice number.
	</param>

	<param type='string' name='mac'>
	A MAC address to assign to this VM.
	If no MAC address is specified, the next free MAC address will be
	selected.
	</param>

	<param type='string' name='num-macs'>
	The number of MAC addresses to automatically assign to this VM.
	The default is 1.
	</param>
	
	<param type='string' name='disk'>
	A disk specification for this VM.
	The fist part of the disk is a string used to specify the format of the disk on the domain 0:
	file is used for raw file format, qcow2 for the qcow2 file fomat, and phy for a physical device
	The second part of the disk string is a path to the location of the disk on the system up to the 
	first comma (,). 
	The third part is used to indicate the name under which the disk is exposed to the guest OS. 
	The actual device name specified is not guaranteed to map to the device name in the guest OS. 
	Treat it as a device ordering hint.
	The forth part indicate the type of disk device to emulate valid values are "virtio" (default), 
	"ide", "scsi".

	The default is: file:/&lt;largest-partition-on-physical-node&gt;/kvm/disks/&lt;vm-name&gt;.vda,vda,virtio
	</param>

	<param type='string' name='disksize'>
	The amount of disk space in gigabytes to assign to the disk
	specification.
	The default is: 36.
	</param>

	<param type='string' name='vlan'>
	The vlan ID to set for each interface. If you supply multiple MACs
	(e.g., 'num-macs' > 1), you can specify multiple vlan IDs by a
	comma separated list (e.g., vlan="3,4,5"). To not specify a vlan
	for a MAC, use the keyword 'none'. For example, if you want to
	specify a vlan ID for interface 1 and 3, but not interface 2, type:
	vlan="3,none,5".
	The default is to not assign a vlan ID.
	</param>

	<param type='bool' name='sync-config'>
	Decides if 'rocks sync config' should be run after the VM is added.
	The default is: yes.
	</param>

	<example cmd='add host vm'>
	Create a default VM.
	</example>

	<example cmd='add host vm mem=4096'>
	Create a VM and allocate 4 GB of memory to it.
	</example>
	"""

	def addToDB(self, physnode, membership, subnet, nodename, ip, mem, cpus, 
			slice, mac, num_macs, disk, disksize, vlanids, 
			virt_type):

		#
		# we're good to go -- add the VM to the nodes table
		#
		# use add host command directly
		success = self.command('add.host', [ nodename, 
				'membership=%s' % membership.name, 
				'cpus=%d' % int(cpus),
				'rack=%d' % int(physnode.rack),
				'rank=%d' % int(physnode.rank),
				'os=linux'])

		# get the newnode
		s = self.newdb.getSession()
		node = Node.load(s, name=nodename).one()

		#
		# insert the additional network interfaces
		#
		for index in range(0, num_macs):

			if not mac:
				mac = self.getNextMac()

			vlan=None
			if vlanids and len(vlanids) > index:
				if vlanids[index] != 'none':
					vlan = int(vlanids[index])

			net = Network(node=node, mac=mac, ip=ip, name=node.name, 
				device='eth%d' % index, subnet=subnet, 
				vlanID=vlan)
			mac = None
			ip = None
			subnet = None
			s.add(net)

		# 
		# make this node a virtual node: vm_node and vm_disk 
		# tables
		#
		vm_node = VmNode(node=node, physNode=physnode, mem=mem, 
				slice=slice, virt_type=virt_type)
		s.add(vm_node)

		dict = parseDisk(disk)
		disk = VmDisk(node=vm_node, size=disksize, **dict)
		s.add(disk)


	def getNextIP(self, name):

		nextip = self.command('report.nextip', [name])
		if nextip and len(nextip) > 0:
			return nextip.strip()


	def makeOctets(self, str):
		octets = []
		for a in str.split(':'):
			octets.append(int(a, 16))

		return octets
			

	def getNextMac(self):
		#
		# find the next free VM MAC address in the database
		#

		#
		# get the VM MAC base addr and its mask
		#
		globalAttr = self.newdb.getCategoryAttrs('global', 'global')

		
		for a in globalAttr:
			if a.attr ==  'vm_mac_base_addr':
				base_addr = self.makeOctets(a.value)
			elif a.attr == 'vm_mac_base_addr_mask':
				mask = self.makeOctets(a.value)

		if not mask:
			self.abort('no VM MAC base address mask is defined')
		if not base_addr:
			self.abort('no VM MAC base address is defined')


		max = 0
		for m,  in self.newdb.getSession().query(Network.mac).\
				filter(Network.mac != None).all():

			if len(m) > 18:
				# skip IB mac addresses from this algorithm
				continue

			mac = self.makeOctets(m)

			i = 0
			match = 1
			for a in base_addr:
				if (base_addr[i] & mask[i]) != \
						(mac[i] & mask[i]):
					match = 0
					break
				i += 1

			if match == 0:
				continue

			i = 0
			x = 0
			for a in range(len(mac) - 1, -1, -1):
				y = (mac[a] * (2 ** (8 * i)))
				x += y
				i += 1
				
			if x > max:
				max = x

		newmac = []

		if max == 0:
			#
			# this is the first assignment, use the base_addr as
			# the mac address
			#
			for a in base_addr:
				newmac.append('%02x' % a)
		else:
			max += 1

			#
			# now convert the integer into a mac address
			#
			i = 0
			bitmask = 0xff
			for a in range(len(mac) - 1, -1, -1):
				x = (max & bitmask) >> (8 * i)
				if a == 0:
					#
					# special case for the first MAC octet.
					#
					# the first bit should be zero (the
					# multicast bit).
					#
					if (x & 0x1) == 1:
						x += 1

					# 
					# the second bit should be one (the
					# locally administered bit).
					#
					if (x & 0x2) == 0:
						x |= 0x2
					
				newmac.append('%02x' % x)
				bitmask = bitmask << 8 
				i += 1

			newmac.reverse()

		return ':'.join(newmac)
				

	def addVMHost(self, node, membership, subnet, nodename, ip, mem, cpus,
		slice, mac, num_macs, disk, disksize, vlan, virt_type):
		"""node is a Node type and membership is a Membership type, 
		subnet is a Subnet type. All other input params are strings"""

		s = self.newdb.getSession()
		knownhosts = s.query(Node.name).all()

		if not slice:
			#
			# find the next free slice in the database
			#
			slices = s.query(sqlalchemy.sql.func.max(VmNode.slice)).\
					filter(VmNode.physNode == node).all()
			slice = 0
			if slices[0][0]:
				slice = slices[0][0]
			
			#
			# special case where the user didn't specify the
			# slice *and* the nodename, then we are allowed to
			# increment the slice value until we find a unique
			# nodename
			#
			while not nodename:
				nodename = '%s-%s-%s-%s' % (membership.appliance.name, 
						node.rack, node.rank, slice)

				if (nodename,) in knownhosts:
					nodename = None
					slice += 1

		if not nodename:
			nodename = '%s-%s-%s-%s' % (membership.appliance.name, 
					node.rack, node.rank, slice)

			if (nodename,) in knownhosts:
				#
				# make sure the nodename is not already in
				# the database
				#
				self.abort('nodename (%s) ' % nodename + \
					'is already in the databaase')
			
		if not disk:
			#
			# find the largest partition on the remote node
			# and use it as the directory prefix
			#
			vm = rocks.vm.VM(self.db)

			vbd_type = 'file'
			prefix = vm.getLargestPartition(node.name)
			device = 'vda'
			name = '%s.%s' % (nodename, device)
			mode = 'virtio'

			if not prefix:
				self.abort('could not find a partition on '
					+ 'host (%s) to hold the ' % node.name
					+ 'VM\'s disk image')

			disk = '%s:%s,%s,%s' % (vbd_type, 
				os.path.join(prefix, 'kvm/disks', name),
				device, mode)

		if not ip:
			if membership.name == 'Hosted VM':
				ip = None
			else:
				ip = self.getNextIP(subnet.name)
		if ip:
			ip = ip.strip("'")

		if vlan:
			vlanids = vlan.split(',')
		else:
			vlanids = None

		#
		# we now have all the parameters -- add them to the database
		#
		self.addToDB(node, membership, subnet, nodename, ip, mem, cpus, 
			slice, mac, num_macs, disk, disksize, vlanids, virt_type)
		# write all this stuff to disk
		self.newdb.commit()
		self.newdb.renewConnection()

		#
		# set the default installaction
		#
		if virt_type == 'para':
			self.command('set.host.installaction', [ nodename,
				'install vm' ] )

		# HVMs boot just like real hardware
		if virt_type == 'hvm':
			self.command('set.host.installaction', [nodename, 
					'install headless'])
			self.command('set.host.runaction', [nodename, 'os'])
		#
		# set the first boot state to 'install'
		#
		self.command('set.host.boot', [nodename, 'action=install'])

		#
		# print the name of the new VM
		#
		self.beginOutput()
		self.addOutput('', 'added VM %s on physical node %s' %
			(nodename, node.name))
		self.endOutput()


	def run(self, params, args):
		(args, membership) = self.fillPositionalArgs(('membership', ))

		if not membership:
			self.abort('must supply a membership')

		if not len(args):
			self.abort('must supply at least one host')

		#
		# fillParams with the above default values
		#
		(nodename, ip, subnet, mem, cpus, slice, mac, macs, disk,
			disksize, vlan, sync_config, virt_type) = self.fillParams(
				[('name', None),
				('ip', None),
				('subnet', 'private'),
				('mem', 1024),
				('cpus', 1),
				('slice', None),
				('mac', None),
				('num-macs', '1'),
				('disk', None),
				('disksize', 36),
				('vlan', None),
				('sync-config', 'y'),
				('virt-type', 'hvm')
				])

		virt_type=virt_type.lower()

		nodes = self.newdb.getNodesfromNames(args)

		if len(nodes) > 1:
			if nodename:
				self.abort("can't supply the 'name' " +
					"parameter with more than one host")
			if ip:
				self.abort("can't supply the 'ip' " +
					"parameter with more than one host")
			if slice:
				self.abort("can't supply the 'slice' " +
					"parameter with more than one host")
			if mac:
				self.abort("can't supply the 'mac' " +
					"parameter with more than one host")
			if virt_type != 'para' and virt_type != 'hvm':
				self.abort("Virtualization type must be either 'hvm' or 'para'")
			import rocks.vmconstant
			if rocks.vmconstant.virt_engine == 'kvm' and virt_type != 'hvm':
				self.abort("KVM supports only hvm virtualization")
		try:
			num_macs = int(macs)
		except:
			self.abort("the num_macs parameter must be an integer")

		membership_db = self.newdb.getSession().query(Membership).filter(
				Membership.name == membership).\
				options(sqlalchemy.orm.joinedload('appliance')).one()

		if not membership_db.appliance :
			self.abort("membership %s is not valid" % membership)


		if membership == 'Hosted VM':
			ip = None
			subnet_db = None
		else:
			subnet_db = self.newdb.getSession().query(Subnet).\
					filter(Subnet.name == subnet).one()



		for node in nodes:
			self.addVMHost(node, membership_db, subnet_db, nodename, ip,
				mem, cpus, slice, mac, num_macs, disk, disksize,
				vlan, virt_type)

		syncit = self.str2bool(sync_config)

		if syncit:
			#
			# reconfigure and restart the appropriate rocks services
			#
			self.command('sync.config')

RollName = "kvm"
