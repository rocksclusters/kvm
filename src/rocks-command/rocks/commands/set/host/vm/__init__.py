# $Id: __init__.py,v 1.4 2012/11/27 00:49:10 phil Exp $
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
# $Log: __init__.py,v $
# Revision 1.4  2012/11/27 00:49:10  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.3  2012/08/29 01:39:55  clem
# Rework of the disk management in kvm
#
# - Now it support qcow2 format (default is still raw
#
# - Now it is also possible to specify the device used to
#   expose the disk inside the virtual machine
#
# - added some docs on the new disk string format
#
# Revision 1.2  2012/05/06 05:49:18  phil
# Copyright Storm for Mamba
#
# Revision 1.1  2012/03/17 02:52:31  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.14  2011/07/23 02:31:45  phil
# Viper Copyright
#
# Revision 1.13  2011/02/14 04:19:14  phil
# Now support HVM as well as paravirtual instances.
# Preliminary testing on 64bit complete.
#
# Revision 1.12  2010/10/25 22:28:23  bruno
# after we detemine a 'physnode' is in the cluster with getHostname, let's
# be sure to set the phynode name to what is returned by getHostname
#
# Revision 1.11  2010/09/07 23:53:33  bruno
# star power for gb
#
# Revision 1.10  2009/06/01 23:38:29  bruno
# can use a physical partition for a VMs disk
#
# Revision 1.9  2009/05/01 19:07:35  mjk
# chimi con queso
#
# Revision 1.8  2009/04/22 18:34:29  bruno
# can now resize a VMs disk
#
# Revision 1.7  2009/01/14 00:20:56  bruno
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
# Revision 1.6  2009/01/12 23:53:30  bruno
# don't reset the install profile to 'install' if the 'installprofile' flag is
# not supplied
#
# Revision 1.5  2008/12/16 00:45:11  bruno
# merge vm_profiles and pxeaction tables into bootaction table
#
# Revision 1.4  2008/10/27 19:25:01  bruno
# folded 'rocks * host vm boot' commands into 'rocks * host vm'
#
# Revision 1.3  2008/10/18 00:56:24  mjk
# copyright 5.1
#
# Revision 1.2  2008/04/21 16:37:35  bruno
# nuked the vm_macs table -- now using the networks table to store/retrieve
# mac addresses for VMs
#
# Revision 1.1  2008/04/17 23:23:39  bruno
# you now can change the number of cpus and memory allocated to VMs.
#
#
#

import os.path
import rocks.commands
import rocks.commands.add.host.vm
from rocks.db.mappings.kvm import *


class Command(rocks.commands.HostArgumentProcessor, rocks.commands.set.command):
	"""
	Change the VM configuration for a specific VM.
	
	<arg type='string' name='host' optional='0'>
	One or more VM host names.
	</arg>

	<param type='string' name='physnode'>
	The physical machine this VM should run on.
	</param>

	<param type='string' name='disk'>
	A VM disk specification. More than one disk can be supplied. Each
	disk specification must separated by a space.
	For more information on the disk format please look at the:
	rocks add host vm help
	</param>

	<param type='string' name='disksize'>
	The size of the VM disk in gigabytes. If more than one disk is
	supplied the sizes should be separated by space.
	</param>

	<param type='string' name='mem'>
	The amount of memory in megabytes to assign to this VM.
	</param>

	<param type='string' name='slice'>
	The slice ID for this VM.
	</param>

	<param type='string' name='virt-type'>
	Set the virtualization type for this VM. This can be 'para' or
	'hvm'.
	</param>

	<example cmd='set host vm compute-0-0-0 mem=4096'>
	Change the memory allocation for VM compute-0-0-0 to 4 GB.
	</example>
	"""


	def run(self, params, args):
		mem = None

		(physnode, disk, disksize, m, slice, virt_type) = \
			self.fillParams([ ('physnode', None),
				('disk', None), ('disksize', None),
				('mem', None), ('slice', None),
				('virt-type', None) ])

		try:
			if m:
				mem = int(m)
		except:
			self.abort('"mem" parameter must be an integer')

		if physnode:
			p = self.newdb.getNodesfromNames([physnode])
			if len(p) == 0:
				self.abort('physnode "%s" does not exist'
					% (physnode))
			if len(p) > 1:
				self.abort('too many physnodes. ' +
					'only supply one physnode')

			physnode = p[0]
		
		nodes = self.newdb.getNodesfromNames(args, preload=['vm_defs',
			'vm_defs.physNode', 'networks', 'vm_defs.disks'])
		if len(nodes) != 1:
			self.abort('must supply only one host')
		node = nodes[0]


		s = self.newdb.getSession()

		if not node.vm_defs:
			# this node did not have a vm_node let's add it
			vm_node = VmNode(node=node)
			s.add(vm_node)
		else:
			vm_node = node.vm_defs

		if physnode:
			# set the physicalNode of this virtual node
			vm_node.physNode = physnode

		#
		# is this just a disk resize?
		#
		if disksize and not disk:
			#
			# get the ids of the VM disks
			#
			if len(disksize.split(' ')) > len(vm_node.disks):
				self.abort('too many disksize vm has only '
					'%d disks' % len(vm_node.disks))

			for index, ds in enumerate(disksize.split(' ')):
				try:
					dsize = int(ds)
				except:
					msg = '"disksize" values must be '
					msg += 'integers'
					self.abort(msg)

				if dsize > 0:
					vm_node.disks[index].size = dsize

		elif disk:
			#
			# first remove all disk entries
			#
			for d in vm_node.disks:
				s.delete(d)

			#
			# then add them back
			#
			ds = []
			if disksize:
				ds = disksize.split(' ')

			for index, d in enumerate(disk.split(' ')):
				if (len(ds) - 1) < index:
					dsize = '36'
				else:
					dsize = ds[index]

				#
				# parse the disk specification
				#
				dict = rocks.commands.add.host.vm.parseDisk(d)

				disk = VmDisk(node=vm_node, size=dsize, **dict)
				s.add(disk)

				
		if mem:
			vm_node.mem = mem

		if slice:
			vm_node.slice = slice

		if virt_type and virt_type != 'None':
			virt_type=virt_type.lower()
			if virt_type == 'para' or virt_type == 'hvm':
				vm_node.virt_type = virt_type
			else:
				self.abort("virt-type must be either 'hvm' or 'para'")	


RollName = "kvm"
