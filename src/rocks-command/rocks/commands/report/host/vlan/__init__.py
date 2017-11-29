# $Id: __init__.py,v 1.6 2012/11/27 00:49:11 phil Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWindwer)
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
#
#

import os
import time
import xml.sax.saxutils

from rocks.db.mappings.base import *
from rocks.db.mappings.kvm import *
import rocks.db.mappings.kvm
import rocks.db.vmextend
import rocks.commands
import rocks

networking_file = '/etc/libvirt/networking/vlan.conf'
if rocks.version_major == '7':
	networking_file = '/etc/libvirt/qemu/networks/vlan.conf'
	

class Command(rocks.commands.HostArgumentProcessor,
        rocks.commands.report.command):
        """
	Print the command necessary to start the vlan interface needed 
	by virtual machines on a vm-containers and on frontends.
	VLan used by virtual machines now are not anymore under
	Red Hat network manager control, but they are managed by rocks.

	<example cmd='report host vlan compute-0-0-0'>
	Print the command necessary to start the vlan for host compute-0-0-0
	</example>
	"""

	def bootVLAN(self, node):
		"""return a string with the commands necessary to start up 
		the the VLAN relative to the given host and physhost"""

		ret = ""

		for physicaldev in self.newdb.getPhysTapDevicefromVnode(node):
			options = physicaldev["options"]
			if options is not None and options.find("novtap") >= 0:
				prefix=""
			else:
				prefix="p"
			
			device = prefix + physicaldev["device"]
			vlanid = physicaldev["vlanID"]
			physhost = node.vm_defs.physNode

			if (physhost, device, vlanid) not in self.vlanProcessed:

				# let's check if the device is already up
				ret += "ip link show %s.%s > /dev/null 2>&1 ||" % \
						(device, vlanid)

				ret += "ip link add link %s name %s.%s type vlan id %s && ip link set %s up && ip link set %s.%s up &&" \
					" ip link set arp off dev %s.%s;" % \
					(device, device, vlanid, vlanid, device, device, vlanid, device, vlanid)

				self.vlanProcessed.add((physhost, device, vlanid))
		if not ret:
			ret = '# no vlan for ' + node.name
		return ret


	def run(self, params, args):
		# keep trac of the (physhost, device, vlanid) that we already processed
		self.vlanProcessed = set()
		nodes = self.newdb.getNodesfromNames(args, managed_only=1,
				preload = ['vm_defs', 'vm_defs.physNode', 'networks'])


		if len(nodes) < 1:
			self.abort('must supply at least one host')

		s = self.newdb.getSession()
		self.beginOutput()
		for node in nodes:

			if node.vm_defs and node.vm_defs.physNode:
				temp_string = self.bootVLAN(node)
				self.addOutput(node.name, temp_string)

			else:
				# this is a physical host let's find out its VMs
				vm_nodes = s.query(Node).join(VmNode, Node.vm_defs).filter(
						VmNode.physNode == node).all()

				if not vm_nodes:
					continue

				self.addOutput(node.name, '<file name="%s">\n' % networking_file)
				for vm_node in vm_nodes:

					temp_string = self.bootVLAN(vm_node)
					temp_string = xml.sax.saxutils.escape(temp_string)
					self.addOutput(node.name, temp_string)
				self.addOutput(node.name, '</file>')

                self.endOutput(padChar='')

