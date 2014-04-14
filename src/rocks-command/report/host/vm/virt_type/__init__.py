# $Id: __init__.py,v 1.4 2012/11/27 00:49:09 phil Exp $
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
# Revision 1.4  2012/11/27 00:49:09  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.3  2012/05/06 05:49:17  phil
# Copyright Storm for Mamba
#
# Revision 1.2  2012/04/13 02:29:23  clem
# more fixes
#
# Revision 1.1  2012/03/17 02:52:30  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.2  2011/07/23 02:31:44  phil
# Viper Copyright
#
# Revision 1.1  2011/02/14 04:19:14  phil
# Now support HVM as well as paravirtual instances.
# Preliminary testing on 64bit complete.
#
#
#

import os
import sys
import string
import rocks.commands
import rocks.vm

header = """
import os
import os.path
import sys
"""

class Command(rocks.commands.report.host.command):
	"""
	Output the type of virtualization used for a VM (with KVM
	it is always equal to hvm).
	
	<arg name='host' type='string'>
	One VM host name (e.g., compute-0-0-0).
	</arg>

	<example cmd='report host vm virt-type compute-0-0-0'>
	Report the vitualization type used.
	</example>
	"""

	def getVirtType(self, host):
		#
		# get the VM virtualization type 
		#
		rows = self.db.execute("""select vn.virt_type from
			vm_nodes vn, nodes n where
			vn.node = n.id and n.name = '%s' """ % host)

		virtType, =self.db.fetchone()
		if virtType is None:
			self.addOutput(host, 'para') 
		else:
			self.addOutput(host, '%s' % virtType) 
		return 

	def run(self, params, args):
		hosts = self.getHostnames(args)

		if len(hosts) < 1:
			self.abort('must supply host')

		self.beginOutput()
		for host in hosts:
			try:
				self.getVirtType(host)
			except TypeError:
				pass

		self.endOutput(padChar='')
	

