#!/opt/rocks/bin/python
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
#
#

import os.path
import rocks.commands


class Command(rocks.commands.set.host.command):
	"""
	Change the disablekvm interface flag. This flag is used to disable the
	automatic generation of KVM bridged configuration when starting a 
	viratul machine. If a given interface has this flag true it will not 
	appear on the host at the first restart.
	This functionality can be used in conjunction with the plugins of 
	rocks report host vm config 

	<arg type='string' name='host' optional='0'>
	One or more VM host names.
	</arg>

	<arg type='string' name='iface'>
 	Interface that should be updated. This may be a logical interface or 
 	the mac address of the interface.
 	</arg>

	<param type='bool' name='disablekvm'>
	If true it will disable kvm bridging
	</param>
 	
	<param type='string' name='iface'>
	Can be used in place of the iface argument.
	</param>

	<param type='bool' name='disablekvm'>
	Can be used in place of the disablekvm argument
	</param>


	<example cmd='set host interface disablekvm compute-0-0-0 ib0 true'>
	Disable the automatic generation of ib0 for compute-0-0-0 in KVM
	</example>
	"""

	def run(self, params, args):

		(args, iface, disablekvm) = self.fillPositionalArgs(('iface', 'disablekvm'))

		if not iface:
			self.abort('must supply iface')
		if not disablekvm:
			self.abort('must supply disablekvm')
		if len(args) == 0:
			self.abort('must supply at least one hostname')

		disablekvm = self.str2bool(disablekvm)

		for node in self.newdb.getNodesfromNames(args,
				preload=['networks']):
			for net in node.networks:
				if net.device == iface:
					net.disable_kvm = disablekvm





RollName = "kvm"
