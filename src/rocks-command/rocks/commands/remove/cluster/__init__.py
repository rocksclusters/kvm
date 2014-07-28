# $Id: __init__.py,v 1.4 2012/11/27 00:49:09 phil Exp $
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
# Revision 1.4  2012/11/27 00:49:09  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.3  2012/06/04 22:25:50  clem
# no need for double quote the command variable in rocks.run.command [host, command]
#
# Revision 1.2  2012/05/06 05:49:16  phil
# Copyright Storm for Mamba
#
# Revision 1.1  2012/03/17 02:52:30  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.7  2011/07/23 02:31:44  phil
# Viper Copyright
#
# Revision 1.6  2010/09/07 23:53:32  bruno
# star power for gb
#
# Revision 1.5  2009/05/01 19:07:34  mjk
# chimi con queso
#
# Revision 1.4  2009/02/12 05:15:36  bruno
# add and remove virtual clusters faster
#
# Revision 1.3  2008/10/18 00:56:23  mjk
# copyright 5.1
#
# Revision 1.2  2008/09/04 15:54:16  bruno
# xen tweaks
#
# Revision 1.1  2008/08/22 23:25:56  bruno
# closer
#
#

import rocks.vm
import rocks.commands
import rocks.db.vmextend
import rocks.db.mappings.kvm

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.remove.command):

	"""
	Remove a virtual cluster.
	
	<arg optional='1' type='string' name='cluster' repeat='1'>
	One or more virtual frontend names.
	</arg>

	<example cmd='rmeove cluster frontend-0-0-0'>
	Remove the cluster associated with the frontend named 'frontend-0-0'.
	</example>
	"""

	def run(self, params, args):
		if len(args) == 0:
			self.abort('must supply at least one frontend name')

		clusters = self.newdb.getVClusters()

		nodes = self.newdb.getNodesfromNames(args)
		for node in nodes:
			if node.name not in clusters.getFrontends():
				self.abort('host %s is not a virtual frontend' % node.name)

		# the list of nodes we want to sync the network
		restart_net_physNodes = set()
		for frontend in nodes:
			#
			# find all the client nodes related to this frontend.
			#
			nodes_str = clusters.getNodes(frontend.name)
			if nodes_str:
				nodes = self.newdb.getNodesfromNames(nodes_str,
					preload=["vm_defs", "vm_defs.physNode"])
			else:
				nodes = []

			# a set of tuple with (device, vlanid, physicalnode)
			# to track the network interfaces we have to delete
			delete_interfaces = set()
			# a list of vmhost we haveh to delete
			delete_vmhosts = []

			for node in nodes + [frontend]:

				delete_vmhosts.append(node.name)
				devs = self.newdb.getPhysTapDevicefromVnode(node)
				physNode = node.vm_defs.physNode.name
				for dev in devs:
					# the set will delete duplicates
					delete_interfaces.add((dev['device'],
						dev["vlanID"], physNode))

			for (device, vlanid, physNode) in delete_interfaces:

				print "Removing vlan", vlanid, " on host ",\
						physNode
				self.command('remove.host.interface',
					[physNode, 'vlan%d' % vlanid])
				restart_net_physNodes.add(physNode)


			#
			# remove all the VMs associated with the cluster
			#
			print "Removing hosts: ", ' '.join(delete_vmhosts)
			self.command('remove.host', delete_vmhosts)

		#
		# reconfigure and restart the network on the
		# physical hosts
		#
		print "Syncing configuration"
		self.command('sync.host.network', list(restart_net_physNodes))
		self.command('sync.config')



RollName = "kvm"
