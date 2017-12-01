# $Id: __init__.py,v 1.3 2012/11/27 00:49:11 phil Exp $
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
# $Log: __init__.py,v $
# Revision 1.3  2012/11/27 00:49:11  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.2  2012/05/06 05:49:18  phil
# Copyright Storm for Mamba
#
# Revision 1.1  2012/03/17 02:52:32  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.10  2011/07/23 02:31:46  phil
# Viper Copyright
#
# Revision 1.9  2010/09/07 23:53:34  bruno
# star power for gb
#
# Revision 1.8  2009/12/01 18:54:41  bruno
# suppress error message when trying to stop a VM that is isn't running.
#
# Revision 1.7  2009/05/01 19:07:35  mjk
# chimi con queso
#
# Revision 1.6  2009/04/14 17:41:37  bruno
# bug fix
#
# Revision 1.5  2009/04/08 22:27:59  bruno
# retool the xen commands to use libvirt
#
# Revision 1.4  2008/10/18 00:56:24  mjk
# copyright 5.1
#
# Revision 1.3  2008/05/05 22:04:11  bruno
# doc fix
#
# Revision 1.2  2008/03/06 23:42:05  mjk
# copyright storm on
#
# Revision 1.1  2008/01/30 22:01:35  bruno
# closer
#
#

import os
import tempfile
import syslog
import rocks.commands
import rocks.db.mappings.kvm

import sys
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt

#
# this function is used to suppress an error message
# the error message looks like:
#
#	libvirt.libvirtError: Domain not found: xenUnifiedDomainLookupByName
#
def handler(ctxt, err):
	global errno

	errno = err


class Command(rocks.commands.stop.host.command):
	"""
	Destroy a VM slice on a physical node.

	<param type='bool' name='terminate'>
	If this is true the command will run only the plugin since it will
	assume that the host is already down.
	This is used by to invoke the plugin when the machine is powered 
	so external allocated resource can be freed (e.g. iSCSI connection)
	NB: if terminate is not equal to true the plugin will not be called.
	Basically the command either stops the VM or calls the plugins (this
	is to account for the fact that the libvirtd hooks are called both
	when the host is shutdown and when the host is forcefully stopped
	with rocks stop host vm)
	</param>

	<param type='string' name='action'>
	poweroff will shut down the VM immediately (default)
	shutdown will send the ACPI shutdown signal to the guest OS
	reset will poweroff and poweron the VM
	reboot will send the ACPI reboot signal to the guest OS
	</param>


	<arg type='string' name='host' repeat='1'>
	A list of one or more VM host names.
	</arg>

	<example cmd='stop host vm compute-0-0-0'>
	Stop VM host compute-0-0-0. This is equivalent to a 'hard power off',
	(i.e., pulling the power cord from a node).
	</example>
	"""

	def run(self, params, args):

		nodes = self.newdb.getNodesfromNames(args,
				preload = ['vm_defs'])

		(terminate, action) = self.fillParams( [
			('terminate', 'n'),
			('action', 'poweroff'),
			])

		terminate = self.str2bool(terminate)

		if len(nodes) < 1:
			self.abort('must supply host')

		plugins = self.loadPlugins()

		for node in nodes:

			if not terminate:
				#
				# the name of the physical host that will boot
				# this VM host
				#
				if not node.vm_defs:
					self.abort("host %s is not a virtual host" % node.name)

				if not node.vm_defs.physNode:
					self.abort("host %s does not have a physical host" % node.name)

				# get the physical node that houses this VM
				physhost = node.vm_defs.physNode.name

				import rocks.vmconstant
				hipervisor = libvirt.open(rocks.vmconstant.connectionURL 
									% physhost)
				libvirt.registerErrorHandler(handler, 'context')

				try:
					domU = hipervisor.lookupByName(node.name)
					if(action == 'poweroff'):
						domU.destroy()
						domU.undefine()
					elif(action == 'shutdown'):
						domU.shutdown()
						domU.undefine()
					elif(action == 'reset'):
						domU.reset(0)
					elif(action == 'reboot'):
						domU.reboot(0)
				except libvirt.libvirtError, m:
					pass

			if terminate:
				#
				# run the terminate plugins to deallocate the host resources
				#
				for plugin in plugins:
					syslog.syslog(syslog.LOG_INFO, 'run %s' % plugin)
					plugin.run(node)



RollName = "kvm"
