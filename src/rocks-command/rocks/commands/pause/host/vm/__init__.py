# $Id: __init__.py,v 1.3 2012/11/27 00:49:09 phil Exp $
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
# Revision 1.3  2012/11/27 00:49:09  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.2  2012/05/06 05:49:16  phil
# Copyright Storm for Mamba
#
# Revision 1.1  2012/03/17 02:52:29  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.8  2011/07/23 02:31:44  phil
# Viper Copyright
#
# Revision 1.7  2010/09/07 23:53:32  bruno
# star power for gb
#
# Revision 1.6  2009/05/01 19:07:34  mjk
# chimi con queso
#
# Revision 1.5  2009/04/29 17:37:37  bruno
# make sure libvirt is properly imported
#
# Revision 1.4  2009/04/08 22:27:58  bruno
# retool the xen commands to use libvirt
#
# Revision 1.3  2008/10/18 00:56:23  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:42:04  mjk
# copyright storm on
#
# Revision 1.1  2008/01/29 18:53:05  bruno
# added 'pause' and 'resume'
#
#

import os
import tempfile
import rocks.commands
import rocks.db.mappings.kvm


import sys
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt

class Command(rocks.commands.pause.host.command):
	"""
	Pauses a VM slice on a physical node.

	<arg type='string' name='host' repeat='1'>
	A list of one or more VM host names.
	</arg>

	<example cmd='pause host vm compute-0-0-0'>
	Pause VM host compute-0-0-0.
	</example>
	"""

	def run(self, params, args):
		nodes = self.newdb.getNodesfromNames(args, managed_only=1,
				preload = ['vm_defs', 'vm_defs.physNode'])
		
		if len(nodes) < 1:
			self.abort('must supply host')

		for node in nodes:
			#
			# the name of the physical host that will boot
			# this VM host
			#
			if node.vm_defs and node.vm_defs.physNode:
				#
				# send the pause command to the physical node
				#
				import rocks.vmconstant
				hipervisor = libvirt.open(rocks.vmconstant.connectionURL % 
							node.vm_defs.physNode.name)
				domU = hipervisor.lookupByName(node.name)
				domU.suspend()
			else:
				self.abort("virtual host %s does not have a valid physical host" %
						node.name)


RollName = "kvm"
