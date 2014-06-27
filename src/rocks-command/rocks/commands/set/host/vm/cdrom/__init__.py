#
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
# I was gonna go with the rocks set host vm disk="cdrom:/pathtoiso/file.ido,vda,virtio"
# but then it seemed all to complicated for such a simple task. 
#
# So I optited for a much simpler solution.
#
#

import os.path
import rocks.commands


class Command(rocks.commands.HostArgumentProcessor, rocks.commands.set.command):
	"""
	Add a CDROM image to the virtual machine specified.
	The machine must be restarted to make this effective

	<arg type='string' name='host' optional='0'>
	One or more VM host names.
	</arg>

	<param type='string' name='cdrom'>
	The path to the ISO image to use as a CDROM of the physical device 
	path (/dev/cdrom)
	if it is cdrom=none, it will remove the cdrom image from the current disks
	</param>

	<example cmd='set host vm cdrom compute-0-0-0 cdrom=/root/kernel-6.1-0.x86_64.disk1.iso'>
	Mount the ISO /root/kernel-6.1-0.x86_64.disk1.iso as a CDROM
	</example>

	<example cmd='set host vm cdrom compute-0-0-0 cdrom=none'>
	Remove the CDROM from node compute-0-0-0
	</example>
	"""

	def run(self, params, args):

		(cdrom,) = self.fillParams([ ('cdrom', ""), ])
		if cdrom.lower() == 'none':
			cdrom = ""
		else:
			if not os.path.isabs(cdrom):
				self.abort('You must use an absolute path for the ISO')

		nodes = self.newdb.getNodesfromNames(args, preload=['vm_defs'])
		if len(nodes) != 1:
			self.abort('must supply only one host')
		node = nodes[0]

		node.vm_defs.cdrom_path = cdrom
		#TODO add code to attach cdrom to running instances


RollName = "kvm"
