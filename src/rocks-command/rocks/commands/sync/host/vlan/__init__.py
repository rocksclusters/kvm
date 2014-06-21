# $Id: __init__.py,v 1.6 2012/11/27 00:49:11 phil Exp $
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
#
#

import os
import time
import rocks.commands
import rocks.vmextended


from rocks.commands.sync.host import Parallel
from rocks.commands.sync.host import timeout


class Command(rocks.commands.sync.host.command):
	"""
	Start the vlan interface needed by virtual 
	machines on a vm-containers and on frontends.
	VLan used by virtual machines now are not anymore under
	Red Hat network manager control, but they are started 
	automatically by this command.

	If invoked against a VM it will start the VM vlan.

	If invoked against a VM-container it will update the file
	/etc/libvirt/networking/vlan.conf

	<example cmd='sync host vlan compute-0-0-0'>
	Start the vlan needed by the virtual host compute-0-0-0
	If the vrtual host does not use any vlan the command does nothing
	</example>
	"""


	def run(self, params, args):
		hosts = self.getHostnames(args, managed_only=1)

		if len(hosts) < 1:
			self.abort('must supply at least one host')

		threads = []

		for host in hosts:
			#
			# the name of the physical host that will boot
			# this VM host
			#
			cmd = '/opt/rocks/bin/rocks report host vlan '
			cmd += '%s | ' % host

			vm = rocks.vmextended.VMextended(self.db)
			(physnodeid, physhost) = vm.getPhysNode(host)

			if physnodeid and physhost:

				cmd += self.getExecCommand(physhost)
				# this is called only on a single host, no need to use parralel
				os.system(cmd)

			else:

				cmd += '/opt/rocks/bin/rocks report script |'
				cmd += self.getExecCommand(host)

				p = Parallel(cmd, host)
				threads.append(p)
				p.start()
				for thread in threads:
					thread.join(timeout)


RollName = "kvm"