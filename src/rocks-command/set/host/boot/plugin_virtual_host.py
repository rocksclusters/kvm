# $Id: plugin_virtual_host.py,v 1.1 2012/03/17 02:52:31 clem Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# $Log: plugin_virtual_host.py,v $
# Revision 1.1  2012/03/17 02:52:31  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.4  2011/07/23 02:31:45  phil
# Viper Copyright
#
# Revision 1.3  2010/09/07 23:53:33  bruno
# star power for gb
#
# Revision 1.2  2009/05/01 19:07:35  mjk
# chimi con queso
#
# Revision 1.1  2009/01/16 23:58:15  bruno
# configuring the boot action and writing the boot files (e.g., PXE host config
# files and Xen config files) are now done in exactly the same way.
#
#

import sys
import string
import rocks.commands
import os
import tempfile

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'virtual-host'

	def run(self, host):
		#
		# the name of the physical host that will boot
		# this VM host
		#
		rows = self.db.execute("""select vn.physnode from
			vm_nodes vn, nodes n where n.name = '%s'
			and n.id = vn.node""" % (host))

		if rows == 1:
			physnodeid, = self.db.fetchone()
		else:
			return

		rows = self.db.execute("""select name from nodes where
			id = %s""" % (physnodeid))

		if rows == 1:
			physhost, = self.db.fetchone()
		else:
			return

		#
		# create the configuration file
		#
		temp = tempfile.mktemp()
		fout = open(temp, 'w')
		fout.write(self.owner.command('report.host.vm', [ host ]))
		fout.close()

		#
		# send the configuration file to the physical node that
		# houses this VM
		#
		os.system('scp -q %s %s:/etc/xen/rocks/%s' % 
			(temp, physhost, host))
		os.unlink(temp)

