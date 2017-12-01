# $Id: __init__.py,v 1.5 2012/11/27 00:49:09 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 		         version 7.0 (Manzanita)
# 
# Copyright (c) 2000 - 2017 The Regents of the University of California.
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
# Revision 1.5  2012/11/27 00:49:09  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.4  2012/05/06 05:49:17  phil
# Copyright Storm for Mamba
#
# Revision 1.3  2012/04/08 00:49:59  clem
# code refactoring (added a new command sync host vlan)
# Fixed the restore and move command
#
# Revision 1.2  2012/03/31 01:07:28  clem
# latest version of the networking for kvm (vlan out of redhat network script)
# minor fixes here and there to change the disks path from /state/partition1/xen/disks
# to /state/partition1/kvm/disks
#
# Revision 1.1  2012/03/17 02:52:30  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.9  2011/07/23 02:31:45  phil
# Viper Copyright
#
# Revision 1.8  2011/01/10 22:40:11  bruno
# fix restore and resume
#
# Revision 1.7  2010/09/07 23:53:33  bruno
# star power for gb
#
# Revision 1.6  2009/05/01 19:07:34  mjk
# chimi con queso
#
# Revision 1.5  2009/04/29 17:37:38  bruno
# make sure libvirt is properly imported
#
# Revision 1.4  2009/04/08 22:27:58  bruno
# retool the xen commands to use libvirt
#
# Revision 1.3  2008/10/18 00:56:24  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:42:04  mjk
# copyright storm on
#
# Revision 1.1  2008/02/07 20:08:24  bruno
# retooled the commands and database tables to handle moving running VMs
#
#

import os
import rocks.commands
import rocks.vm

import sys
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt

class Command(rocks.commands.restore.host.command):
	"""
	Restore a VM on a physical node. This command restores a previously
	saved VM.

	<arg type='string' name='host' repeat='1'>
	A list of one or more VM host names.
	</arg>

	<param type='string' name='file'>
	The file name the saved VM state is stored in. If you don't
	supply this parameter, then the default file name is:
	/&lt;largest-partition-on-physical-host&gt;/kvm/disks/&lt;vm-name&gt;.saved.
	For example, on a physical node with the default partitioning, the
	file that contains the state for VM compute-0-0-0 is:
	/state/partition1/kvm/disks/compute-0-0-0.saved
	</param>

	<example cmd='restore host vm compute-0-0-0'>
	Restore VM host compute-0-0-0.
	</example>
	"""

	def run(self, params, args):
		file, = self.fillParams( [('file', None)] )
		hosts = self.getHostnames(args)

		if len(hosts) < 1:
			self.abort('must supply host')

		if file and len(hosts) > 1:
			self.abort('if you supply the "file" parameter, ' +
				'then you only can specify one VM host')
		import rocks.vm
		vm = rocks.vm.VM(self.db)

		for host in hosts:
			physhost = vm.getPhysHost(host)

			if not file:
				diskprefix = vm.getLargestPartition(physhost)
				if diskprefix:
					file = os.path.join(diskprefix,
						'kvm/disks/%s.saved' % host)

			#
			# we need to start vlan interface if any
			#
			self.command('sync.host.vlan', [host])


			if physhost and file:
				#
				# send the restore command to the physical node
				#
				import rocks.vmconstant
				hipervisor = libvirt.open( rocks.vmconstant.connectionURL % physhost)
				hipervisor.restore(file)



RollName = "kvm"
