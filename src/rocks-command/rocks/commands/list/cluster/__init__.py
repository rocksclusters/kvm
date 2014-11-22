# $Id: __init__.py,v 1.3 2012/11/27 00:49:08 phil Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
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
# Revision 1.10  2011/07/23 02:31:43  phil
# Viper Copyright
#
# Revision 1.9  2010/09/07 23:53:32  bruno
# star power for gb
#
# Revision 1.8  2009/05/01 19:07:33  mjk
# chimi con queso
#
# Revision 1.7  2009/04/08 22:27:58  bruno
# retool the xen commands to use libvirt
#
# Revision 1.6  2008/10/18 00:56:23  mjk
# copyright 5.1
#
# Revision 1.5  2008/09/09 19:37:52  bruno
# make 'list cluster' simplier
#
# Revision 1.4  2008/09/08 21:51:40  bruno
# added optional status columns to VM listing commands
#
# Revision 1.3  2008/09/04 19:55:00  bruno
# list the FQDN for frontends
#
# Revision 1.2  2008/08/22 23:25:56  bruno
# closer
#
# Revision 1.1  2008/08/21 21:41:36  bruno
# list physical and virtual clusters
#

import rocks.commands
import rocks.db.mappings.kvm
from rocks.db.vmextend import getStatus

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.list.command):

	"""
	Lists a cluster, that is, for each frontend, all nodes that are
	associated with that frontend are listed.
	
	<arg optional='1' type='string' name='cluster' repeat='1'>
	Zero, one or more frontend names. If no frontend names are supplied,
	information for all clusters will be listed.
	</arg>

	<param type='bool' name='status'>
	If true, then for each VM-based cluster node, output the VM's status
	(e.g., 'active', 'paused', etc.).
        </param>

	<example cmd='list cluster frontend-0-0'>
	List the cluster associated with the frontend named 'frontend-0-0'.
	</example>

	<example cmd='list cluster'>
	List all clusters.
	</example>
	"""


	def run(self, params, args):
		(showstatus, ) = self.fillParams( [ ('status', 'n') ])
		showstatus = self.str2bool(showstatus)

		prel={'preload':['vm_defs', 'vm_defs.physNode']}

		frontends = self.newdb.getNodesfromNames(['frontend'], **prel)
		fenames = [i.name for i in frontends]
		clusters = self.newdb.getVClusters()

		if len(args) > 0:
			nodes = self.newdb.getNodesfromNames(args, **prel)
			for node in nodes:
				if node.name not in fenames:
					self.abort('host %s is not a virtual'
						' frontend' % node.name)
			frontends = nodes

		self.beginOutput()
		for frontend in frontends:

			if frontend.vm_defs:
				info = ('', 'VM')
				if showstatus:
					info += (getStatus(frontend),)
		
				self.addOutput(frontend.name, info)
				# this returns a list of strings
				clients = clusters.getNodes(frontend.name)
				# now it is a list of Node
				if clients:
					clients = self.newdb.getNodesfromNames(clients, **prel)

				for client in clients:
					if client.vm_defs:

						info = (client.name, 'VM')

						if showstatus:
							info += (getStatus(client),)
		
						self.addOutput('', info)
			else:
				info = ('', 'physical')
				if showstatus:
					info += (None,)
		
				self.addOutput(frontend.name, info)

				#
				# a physical frontend. go get all the physical
				# client nodes
				#
				nodes = self.newdb.getNodesfromNames(['compute'], 
							preload=['vm_defs'])

				for node in nodes:
					if node.vm_defs:
						info = (node.name, 'VM')
					else:
						info = (node.name, 'physical')
					if showstatus:
						info += (None,)

					self.addOutput('', info)

		header = [ 'frontend', 'client nodes', 'type' ]
		if showstatus:
			header.append('status')
		self.endOutput(header, trimOwner = 0)



RollName = "kvm"
