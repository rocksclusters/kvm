# $Id: __init__.py,v 1.7 2012/11/27 00:49:11 phil Exp $
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
# Revision 1.7  2012/11/27 00:49:11  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.6  2012/05/06 05:49:18  phil
# Copyright Storm for Mamba
#
# Revision 1.5  2012/04/08 00:49:59  clem
# code refactoring (added a new command sync host vlan)
# Fixed the restore and move command
#
# Revision 1.4  2012/04/06 00:57:54  clem
# set the boot action to os for the virtual frontend after power on
#
# Revision 1.3  2012/03/31 01:07:28  clem
# latest version of the networking for kvm (vlan out of redhat network script)
# minor fixes here and there to change the disks path from /state/partition1/xen/disks
# to /state/partition1/kvm/disks
#
# Revision 1.2  2012/03/28 18:31:19  clem
# removing pygrub configuration file generation code
#
# Revision 1.1  2012/03/17 02:52:31  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.26  2011/07/23 02:31:46  phil
# Viper Copyright
#
# Revision 1.25  2011/02/14 04:19:14  phil
# Now support HVM as well as paravirtual instances.
# Preliminary testing on 64bit complete.
#
# Revision 1.24  2010/09/20 17:55:50  phil
# Allow VMs to define interfaces with no MAC addresses. In this case, do
# not bridge the interface in dom0.
#
# Revision 1.23  2010/09/07 23:53:33  bruno
# star power for gb
#
# Revision 1.22  2010/06/30 17:59:58  bruno
# can now route error messages back to the terminal that issued the command.
#
# can optionally set the VNC viewer flags.
#
# Revision 1.21  2009/10/12 21:12:39  bruno
# suppress error message when we boot a VM for the first time
#
# Revision 1.20  2009/06/01 23:38:30  bruno
# can use a physical partition for a VMs disk
#
# Revision 1.19  2009/05/06 16:37:12  bruno
# keep a xen domain up after a crash. helpful for debugging.
#
# Revision 1.18  2009/05/01 19:07:35  mjk
# chimi con queso
#
# Revision 1.17  2009/04/14 16:12:17  bruno
# push towards chimmy beta
#
# Revision 1.16  2009/04/08 22:27:58  bruno
# retool the xen commands to use libvirt
#
# Revision 1.15  2009/03/06 21:21:30  bruno
# updated for host attributes
#
# Revision 1.14  2009/01/16 23:58:15  bruno
# configuring the boot action and writing the boot files (e.g., PXE host config
# files and Xen config files) are now done in exactly the same way.
#
# Revision 1.13  2009/01/14 01:08:26  bruno
# kill the 'install=y' flag
#
# Revision 1.12  2009/01/14 00:20:56  bruno
# unify the physical node and VM node boot action functionality
#
# - all bootaction's are global
#
# - the node table has a 'runaction' (what bootaction should the node do when
#   a node normally boots) and an 'installaction (the bootaction for installs).
#
# - the 'boot' table has an entry for each node and it dictates what the node
#   will do on the next boot -- it will look up the runaction in the nodes table
#   (for a normal boot) or the installaction in the nodes table (for an install).
#
# Revision 1.11  2008/12/16 00:45:11  bruno
# merge vm_profiles and pxeaction tables into bootaction table
#
# Revision 1.10  2008/10/18 00:56:24  mjk
# copyright 5.1
#
# Revision 1.9  2008/09/25 17:56:54  bruno
# can't have spaces after the 'related' tag. otherwise, the xen usersguide
# will not build
#
# Revision 1.8  2008/09/01 15:58:57  phil
# Support start host vm install=y to force the node to boot its install profile.
# Requires rocks-pygrub to be the bootloader.
#
# Revision 1.7  2008/07/01 22:57:09  bruno
# fixes to the xen reports which generate xen configuration files
#
# Revision 1.6  2008/04/17 16:38:21  bruno
# incorporate phil's vm changes
#
# Revision 1.5  2008/03/06 23:42:05  mjk
# copyright storm on
#
# Revision 1.4  2008/02/08 23:29:59  bruno
# tune
#
# Revision 1.3  2008/02/02 00:01:58  bruno
# fixes
#
# Revision 1.2  2008/02/01 21:38:54  bruno
# closer
#
# Revision 1.1  2008/01/29 00:20:08  bruno
# split 'rocks boot' into 'rocks create' and 'rocks start'
#
#

import os
import tempfile
import rocks.vmextended
import rocks.commands
import rocks.vmconstant
import syslog
import re

import sys
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt

#
# this function is used to suppress an error message when we start a VM
# for the very first time and there isn't a disk file created for it yet.
# the error message looks like:
#
#	libvir: Xen Daemon error : POST operation failed: (xend.err "Error
#	creating domain: Disk isn't accessible)"
#
def handler(ctxt, err):
	global errno

	errno = err


class Command(rocks.commands.start.host.command):
	"""
	Boots a VM slice on a physical node.
	If kvm_autostart == true make the VM start automatically when
	the physical container boot.

	<arg type='string' name='host' repeat='1'>
	A list of one or more VM host names.
	</arg>

	<example cmd='start host vm compute-0-0-0'>
	Start VM host compute-0-0-0.
	</example>

	<example cmd='start host vm compute-0-0-0'>
	Start VM host compute-0-0-0.
	</example>
	"""


	def bootVM(self, hipervisor, host, xmlconfig, autostart):
		""" try to boot a VM named host defined by xmlconfig

		if it succeeds it returns True if it fails because of a missing
		disk it returns False all other cases it throw an exception"""
		#
		# first let's try to undefine the old domain if any
		#
		try:
			dom = hipervisor.lookupByName(host)
			# but before check that it is not running
			if dom.info()[0] == libvirt.VIR_DOMAIN_RUNNING or \
                                        dom.info()[0] == libvirt.VIR_DOMAIN_BLOCKED:
				self.abort("The host %s is already running." % host)
			if dom.info()[0] == libvirt.VIR_DOMAIN_PAUSED:
				self.abort("The host %s is puased. "
					"You need to resume it (rocks resume host vm)."
					% host)
			dom.undefine()
		except libvirt.libvirtError, m:
			if str(m).find("managed save image exists") > 0:
				self.abort("Saved image exists. "
					"Try to run \nrocks restore host vm %s "
					"file=/var/lib/libvirt/qemu/save/%s.save\n"
					"ssh %s rm -f /var/lib/libvirt/qemu/save/%s.save"
					% (host, host, hipervisor.getHostname(), host))
			# that's ok the domain is not defined
			pass

		try:
			domain = hipervisor.defineXML(xmlconfig)
			domain.create()
			if domain and autostart:
				domain.setAutostart(True)

			return True

		except libvirt.libvirtError, m:
			str_tmp = '%s' % m
			NoDisk = str_tmp.find("Disk isn't accessible") >= 1 or \
					 str_tmp.find("Disk image does not exist") >= 1 or \
					 str_tmp.find("No such file or directory") >= 1
			if NoDisk:
				# the disk hasn't been created yet,
				return False
			else:
				#  fail badly
				self.abort(str_tmp)



	def run(self, params, args):
		nodes = self.newdb.getNodesfromNames(args,
				preload=['vm_defs', 'networks', 'vm_defs.disks'])
		
		if len(nodes) < 1:
			self.abort('must supply at least one host')

		sync_vlan = set()
		plugins = self.loadPlugins()

		for node in nodes:
			#
			# I need to run only one particular plugin here i can't just
			# just call the plugins.runPlugins()
			#
			for plugin in plugins:
				if 'plugin_allocate' in plugin.__module__:
					syslog.syslog(syslog.LOG_INFO, 'run %s' % plugin)
					plugin.run(node)

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

			if self.newdb.getHostAttr(node, 'kvm_autostart') == 'true':
				autostart = True
				sync_vlan.add(physhost)
			else:
				autostart = False
			#
			# boot the VM
			#
			hipervisor = libvirt.open( rocks.vmconstant.connectionURL % physhost)
			libvirt.registerErrorHandler(handler, 'context')
			self.command('sync.host.vlan', [node.name])

			#
			# get the VM configuration (in XML format for libvirt)
			#
			xmlconfig = []
			for plugin in plugins:
				if 'plugin_preboot' in plugin.__module__:
					syslog.syslog(syslog.LOG_INFO, 'run %s' % plugin)
					xmlconfig = plugin.run(node)

			if not xmlconfig:
				xmlconfig = self.command('report.host.vm.config', [ node.name ])

			if not self.bootVM(hipervisor, node.name, xmlconfig, autostart):
				#
				# the disk hasn't been created yet,
				# call a program to set them up, then
				# retry the createLinux()
				#
				cmd = 'ssh -q %s ' % physhost
				cmd += '/opt/rocks/bin/'
				cmd += 'rocks-create-vm-disks '
				cmd += '--hostname=%s' % node.name
				os.system(cmd)

				# let's try one last time to start the domain
				if not self.bootVM(hipervisor, node.name, xmlconfig, autostart):
					# we should never get here
					self.abort('unable to boot the virtual machine')

			if node.installaction == "install vm frontend" :
				#this is a virtual frontend we need to change the boot action
				self.command('set.host.boot',[ node.name, "action=os" ])

		# sync vlan
		if sync_vlan:
			self.command('sync.host.vlan', list(sync_vlan))


RollName = "kvm"
