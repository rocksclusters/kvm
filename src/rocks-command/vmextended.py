#!/opt/rocks/bin/python
# 
# @Copyright@
# 
# 				Rocks(r)
# 			 www.rocksclusters.org
# 			 version 5.6 (Emerald Boa)
# 			 version 6.1 (Emerald Boa)
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

import os
import rocks.vm


import sys
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt


class VMextended(rocks.vm.VM):
	""" This class should contain general functions needed when dealing 
	with virtual machines. It extends rocks.vm.VM because that file is part
	of the base roll while this is part of the KVM roll """

	# we have self.db inherited from the superclass
	# self.db = db


	def getPhysNode(self, host):
		"""given a hostname it returns its physical node id"""

		rows = self.db.execute("""select vn.physnode
			from vm_nodes vn, nodes n
			where n.name = '%s' and n.id = vn.node"""
			% (host))

		if rows == 1:
			physnodeid, = self.db.fetchone()
		else:
			return (None, None)

		rows = self.db.execute("""select name from nodes where
			id = %s""" % (physnodeid))

		if rows == 1:
			physhost, = self.db.fetchone()
		else:
			return (None, None)

		return (physnodeid, physhost)


	def getStatus(self, host, physhost=None):
		"""given a virtual hostname it returns its status as a string"""

		if physhost == None:
			(physnodeid, physhost) = self.getPhysNode(host)
			if not physhost:
				return 'nostate-error'

		try:
			import rocks.vmconstant
			hipervisor = libvirt.open(rocks.vmconstant.connectionURL % physhost)
		except:
			import traceback
			traceback.print_exc()
			return 'nostate-error'

		found = 0
		for id in hipervisor.listDomainsID():
			if id == 0:
				#
				# skip dom0
				#
				continue

			domU = hipervisor.lookupByID(id)
			if domU.name() == host:
				found = 1
				break

		state = 'nostate'

		if found:
			status = domU.info()[0]

			if status == libvirt.VIR_DOMAIN_NOSTATE:
				state = 'nostate'
			elif status == libvirt.VIR_DOMAIN_RUNNING or \
					status == libvirt.VIR_DOMAIN_BLOCKED:
				state = 'active'
			elif status == libvirt.VIR_DOMAIN_PAUSED:
				state = 'paused'
			elif status == libvirt.VIR_DOMAIN_SHUTDOWN:
				state = 'shutdown'
			elif status == libvirt.VIR_DOMAIN_SHUTOFF:
				state = 'shutoff'
			elif status == libvirt.VIR_DOMAIN_CRASHED:
				state = 'crashed'

		return state


	def getCDROM(self, hostname):
		"""return a string with the path of the CDROM if one was defined
		None otherwise"""

		rows = self.db.execute("""select vn.cdrom_path from
			vm_nodes vn, nodes n where n.name = '%s'
			and n.id = vn.node""" % (hostname))

		if rows == 1:
			cdrom, = self.db.fetchone()
			return cdrom

		else:
			return None

