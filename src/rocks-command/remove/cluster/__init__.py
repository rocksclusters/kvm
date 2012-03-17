# $Id: __init__.py,v 1.1 2012/03/17 02:52:30 clem Exp $
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
# $Log: __init__.py,v $
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

		vm = rocks.vm.VM(self.db)
		frontends = self.getHostnames( [ 'frontend' ])
		hosts = self.getHostnames(args)
		for host in hosts:
			if host not in frontends:
				self.abort('host %s is not a frontend' % host)
			if not vm.isVM(host):
				self.abort('host %s is not a virtual frontend'
					% host)

		for frontend in hosts:
			#
			# find all the client nodes related to this frontend.
			#
			# all client nodes of this VM frontend have
			# the same vlan ids as this frontend
			#
			rows = self.db.execute("""select net.vlanid, net.subnet
				from networks net, nodes n where n.name = '%s'
				and net.node = n.id and net.vlanid > 1""" %
				frontend)

			vlans = []
			for vlanid, subnet in self.db.fetchall():
				vlans.append((vlanid, subnet))

			if not vlans:
				self.abort('could not find VLAN Id ' +
					'for frontend %s' % frontend)

			phys_nodes = []
			vm_nodes = []
			for vlanid, subnet in vlans:
				self.db.execute("""select n.name from
					networks net, nodes n where
					net.vlanid = %s and net.node = n.id""" %
					vlanid)

				for node, in self.db.fetchall():
					if vm.isVM(node):
						vm_nodes.append(
							(node, vlanid, subnet))
					else:
						phys_nodes.append(
							(node, vlanid, subnet))

			#
			# remove the VLAN configuration from the physical nodes
			#
			pnodes = []
			for node, vlanid, subnet in phys_nodes:
				rows = self.db.execute("""select net.device from
					nodes n, networks net where
					n.name = '%s' and n.id = net.node and
					net.vlanid = %s""" % (node, vlanid))

				if rows != 1:
					self.abort('could not find VLAN ' +
						'%s for node %s' %
						(vlanid, node))

				iface, = self.db.fetchone()

				self.command('remove.host.interface',
					[ node, iface ] )

				#
				# remove the ifcfg file from the physical host
				#
				rows = self.db.execute("""select net.device from
					nodes n, networks net where
					n.name = '%s' and n.id = net.node and
					net.subnet = %s and net.device not like
					'vlan%%' """ % (node, subnet))

				if rows != 1:
					self.abort('could not find VLAN ' +
						'%s for node %s' %
						(vlanid, node))

				device, = self.db.fetchone()
				cmd = '"rm -f /etc/sysconfig/network-scripts/'
				cmd += 'ifcfg-%s.%s"' % (device, vlanid)

				self.command('run.host', [ node, cmd ] )

				pnodes.append(node)

			#
			# reconfigure and restart the network on the
			# physical hosts
			#
			try:
				self.command('sync.host.network', pnodes)
			except:
				pass

			#
			# remove all the VMs associated with the cluster
			#
			vnodes = []
			for node, vlanid, subnet in vm_nodes:
				vnodes.append(node)

			self.command('remove.host', vnodes )

		self.command('sync.config')


