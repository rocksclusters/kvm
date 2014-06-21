# $Id: __init__.py,v 1.3 2012/11/27 00:49:08 phil Exp $
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
# Revision 1.3  2012/11/27 00:49:08  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.2  2012/05/06 05:49:16  phil
# Copyright Storm for Mamba
#
# Revision 1.1  2012/03/17 02:52:29  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.18  2011/07/23 02:31:43  phil
# Viper Copyright
#
# Revision 1.17  2011/03/24 23:30:01  bruno
# make sure the 'virt-type' field is set to None for every
# disk specification that is not the first one.
#
# Revision 1.16  2011/02/14 04:19:14  phil
# Now support HVM as well as paravirtual instances.
# Preliminary testing on 64bit complete.
#
# Revision 1.15  2010/09/07 23:53:32  bruno
# star power for gb
#
# Revision 1.14  2010/01/15 20:16:25  bruno
# set the disk and disksize to the empty string if no disks are specified
# for a VM.
#
# Revision 1.13  2009/05/01 19:07:33  mjk
# chimi con queso
#
# Revision 1.12  2009/04/08 22:27:58  bruno
# retool the xen commands to use libvirt
#
# Revision 1.11  2009/01/14 00:20:56  bruno
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
# Revision 1.10  2008/10/27 19:25:01  bruno
# folded 'rocks * host vm boot' commands into 'rocks * host vm'
#
# Revision 1.9  2008/10/18 00:56:23  mjk
# copyright 5.1
#
# Revision 1.8  2008/09/08 21:27:43  bruno
# add optional status to 'rocks list host vm'
#
# Revision 1.7  2008/04/21 16:37:35  bruno
# nuked the vm_macs table -- now using the networks table to store/retrieve
# mac addresses for VMs
#
# Revision 1.6  2008/03/06 23:42:04  mjk
# copyright storm on
#
# Revision 1.5  2008/02/27 01:29:27  bruno
# bug fix
#
# Revision 1.4  2008/02/19 23:20:24  bruno
# katz made me do it.
#
# Revision 1.3  2008/02/07 20:08:24  bruno
# retooled the commands and database tables to handle moving running VMs
#
# Revision 1.2  2008/01/30 22:01:34  bruno
# closer
#
# Revision 1.1  2007/12/03 19:48:51  bruno
# xen for V
#
#

import os.path
import rocks.commands
import rocks.vmextended

import sys
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt

class Command(rocks.commands.list.host.command):
	"""
	Lists the VM configuration for hosts.
	
	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied,
	information for all hosts will be listed.
	</arg>

	<param type='bool' name='showdisks'>
	If true, then output VM disk configuration. The default is 'false'.
        </param>

	<param type='bool' name='status'>
	If true, then output each VM's status (e.g., 'active', 'paused', etc.).
        </param>

	<example cmd='list host vm compute-0-0'>
	List the VM configuration for compute-0-0.
	</example>

	<example cmd='list host vm compute-0-0 compute-0-1'>
	List the VM configuration for compute-0-0 and compute-0-1.
	</example>
	"""

	def run(self, params, args):
		(showdisks, showstatus) = self.fillParams( [
			('showdisks', 'n'), 
			('status', 'n')
			])

		showdisks = self.str2bool(showdisks)
		showstatus = self.str2bool(showstatus)

		vmlib = rocks.vmextended.VMextended(self.db)

		self.beginOutput()

		#
		# one query does it all!!
		# with perload we specify all the sub fileds that we will use
		# and we fetch all the data we need with one big query
		#
		for host in self.newdb.getNodesfromNames(args, 
				preload=['vm_defs', 'networks', 'vm_defs.disks']):

			if not host.vm_defs :
				continue

			# get the physical node that houses this VM
			physhost = host.vm_defs.physNode.name

			# get networks
			macs = [net.mac for net in host.networks]
			if len(macs) > 0:
				mac = macs[0]
			else:
				mac = None

			# disks
			disks = []
			for disk in host.vm_defs.disks:

				file = os.path.join(disk.prefix,
					disk.name)

				diskstr = '%s:%s,%s,%s' % \
					(disk.vbd_Type, file,
					disk.device, disk.mode)
				disks.append((diskstr, disk.size))

			if len(disks) > 0:
				(disk, disksize) = disks[0]
			else:
				disk = ''
				disksize = ''


			if host.vm_defs.virt_type:
				virtType = host.vm_defs.virt_type
			else:
				virtType = "para"

			# spit it out!
			info = (host.vm_defs.slice, host.vm_defs.mem, host.cpus, mac, physhost, virtType)
			if showstatus:
				info += (vmlib.getStatus(host.name, physhost),)
			if showdisks:
				info += (disk, disksize, host.vm_defs.cdrom_path)

			self.addOutput(host.name, info)

			index = 1
			while len(macs) > index or len(disks) > index:
				if len(macs) > index:
					mac = macs[index]
				else:
					mac = ''

				if len(disks) > index:
					disk, disksize = disks[index]
				else:
					disk = ''
					disksize = ''

				info = (None, None, None, mac, None, None)
				if showstatus:
					info += (None,)
				if showdisks:
					info += (disk, disksize, None)

				self.addOutput(host.name, info)

				index += 1

		header = [ 'vm-host', 'slice', 'mem', 'cpus', 'mac', 'host', 'virt-type' ]

		if showstatus:
			header.append('status')
		if showdisks:
			header += [ 'disk', 'disksize', 'cdrom']

		self.endOutput(header)


