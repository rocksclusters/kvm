# $Id: __init__.py,v 1.4 2012/11/27 00:49:10 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 6.1.1 (Sand Boa)
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
# Revision 1.3  2012/05/06 05:49:17  phil
# Copyright Storm for Mamba
#
# Revision 1.2  2012/03/31 01:07:28  clem
# latest version of the networking for kvm (vlan out of redhat network script)
# minor fixes here and there to change the disks path from /state/partition1/xen/disks
# to /state/partition1/kvm/disks
#
# Revision 1.1  2012/03/17 02:52:31  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.8  2011/07/23 02:31:45  phil
# Viper Copyright
#
# Revision 1.7  2010/09/07 23:53:33  bruno
# star power for gb
#
# Revision 1.6  2009/05/01 19:07:35  mjk
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
# Revision 1.2  2008/03/06 23:42:05  mjk
# copyright storm on
#
# Revision 1.1  2008/02/07 20:08:25  bruno
# retooled the commands and database tables to handle moving running VMs
#
#

import os
import os.path
import rocks.commands
import rocks.vm

import sys
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt

class Command(rocks.commands.save.host.command):
	"""
	Save a VM on a physical node. This command saves a currently running
	VM, then halts the VM. This saved state can be used to restart the
	VM with the command 'rocks restore host vm'.

	<arg type='string' name='host' repeat='1'>
	A list of one or more VM host names.
	</arg>

	<arg type='string' name='file'>
	The file name the saved VM state will be stored in. If you don't
	supply this parameter, then the default file name will be:
	/&lt;largest-partition-on-physical-host&gt;/kvm/disks/&lt;vm-name&gt;.saved.
	For example, on a physical node with the default partitioning, the
	saved file for VM compute-0-0-0 will be named:
	/state/partition1/kvm/disks/compute-0-0-0.saved
	</arg>

	<example cmd='save host vm compute-0-0-0'>
	Save VM host compute-0-0-0.
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
			if not physhost:
				continue
			
			if not file:
				diskprefix = vm.getLargestPartition(physhost)
				if diskprefix:
					#
					# create a default file name
					#
					file = os.path.join(os.path.join(
						diskprefix, 'kvm/disks'),
						'%s.saved' % host)

			if physhost and file:
				#
				# send the save command to the physical node
				#
				import rocks.vmconstant
				hipervisor = libvirt.open( rocks.vmconstant.connectionURL % physhost)
				domU = hipervisor.lookupByName(host)
				domU.save(file)


