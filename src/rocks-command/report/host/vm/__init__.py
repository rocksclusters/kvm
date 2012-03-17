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
# Revision 1.50  2011/07/23 02:31:44  phil
# Viper Copyright
#
# Revision 1.49  2010/10/15 19:20:36  bruno
# make sure only 1 DNS server is supplied to loader
#
# Revision 1.48  2010/09/07 23:53:33  bruno
# star power for gb
#
# Revision 1.47  2009/07/16 22:46:58  bruno
# if there is no boot action for a VM, assume install
#
# Revision 1.46  2009/06/30 16:30:26  bruno
# fixes to support for virtual compute nodes that are managed by a
# physical frontend
#
# Revision 1.45  2009/06/01 23:38:29  bruno
# can use a physical partition for a VMs disk
#
# Revision 1.44  2009/05/21 21:14:43  bruno
# tweaks
#
# Revision 1.43  2009/05/12 00:45:16  bruno
# append networking info onto the install boot args
#
# Revision 1.42  2009/05/01 19:07:34  mjk
# chimi con queso
#
# Revision 1.41  2009/04/14 16:12:17  bruno
# push towards chimmy beta
#
# Revision 1.40  2009/04/08 22:27:58  bruno
# retool the xen commands to use libvirt
#
# Revision 1.39  2009/02/14 00:02:36  bruno
# clean up bootaction selection
#
# Revision 1.38  2009/01/14 01:08:26  bruno
# kill the 'install=y' flag
#
# Revision 1.37  2009/01/14 00:20:56  bruno
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
# Revision 1.36  2009/01/09 20:42:51  bruno
# change pxeaction/pxeboot to bootaction/boot.
#
# Revision 1.35  2008/12/16 00:45:11  bruno
# merge vm_profiles and pxeaction tables into bootaction table
#
# Revision 1.34  2008/11/03 23:08:26  bruno
# phil's opensolaris xen fix
#
# Revision 1.33  2008/10/27 21:14:51  bruno
# get the disk creation size correct
#
# Revision 1.32  2008/10/18 00:56:23  mjk
# copyright 5.1
#
# Revision 1.31  2008/09/25 17:56:54  bruno
# can't have spaces after the 'related' tag. otherwise, the xen usersguide
# will not build
#
# Revision 1.30  2008/09/25 17:39:55  bruno
# phil's command tweaks
#
# Revision 1.29  2008/09/02 15:41:51  phil
# Support full disks (The Rocks Way) and a particular partition (Others)
#
# Revision 1.28  2008/09/01 18:50:04  phil
# Correctly write the host configuration file
#
# Revision 1.27  2008/09/01 18:28:33  phil
# Xen requires the disk to exist before calling bootloader. Put logic back into
# xen config to create, if it doesn't exist.  Remove this logic from rocks-pygrub
#
# Revision 1.26  2008/09/01 15:45:28  phil
# Use bootprofiles to determine how to boot this VM
#
# Revision 1.25  2008/08/29 21:16:54  phil
# Fix some parsing
#
# Revision 1.24  2008/08/29 19:00:12  phil
# use rocks-pygrub wrapper
#
# Revision 1.23  2008/08/28 02:37:25  phil
# Use pygrub for extracting the kernel from the image
#
# Revision 1.22  2008/08/14 19:32:05  phil
# properly retrieve the device name for mapping a vlan interface to the physical interface on which it is
# located
#
# Revision 1.21  2008/08/13 00:06:31  phil
# look for vlan interface names of the form vlan*
#
# Revision 1.20  2008/07/29 16:47:24  bruno
# more vlan support for xen VMs
#
# Revision 1.19  2008/07/22 00:16:20  bruno
# support for VLANs
#
# Revision 1.18  2008/07/01 22:57:08  bruno
# fixes to the xen reports which generate xen configuration files
#
# Revision 1.17  2008/04/25 17:17:17  bruno
# set the root to be the first partition on the boot disk and get the device
# name from the database
#
# Revision 1.16  2008/04/21 16:37:35  bruno
# nuked the vm_macs table -- now using the networks table to store/retrieve
# mac addresses for VMs
#
# Revision 1.15  2008/04/17 16:38:21  bruno
# incorporate phil's vm changes
#
# Revision 1.14  2008/04/15 23:08:13  bruno
# order the macs and disks
#
# Revision 1.13  2008/03/14 22:10:39  bruno
# touch up
#
# Revision 1.12  2008/03/06 23:42:04  mjk
# copyright storm on
#
# Revision 1.11  2008/02/27 17:43:24  bruno
# remove debug code
#
# Revision 1.10  2008/02/21 21:36:25  bruno
# get the mode correct
#
# Revision 1.9  2008/02/19 23:20:25  bruno
# katz made me do it.
#
# Revision 1.8  2008/02/12 00:01:26  bruno
# fixes
#
# Revision 1.7  2008/02/08 23:29:59  bruno
# tune
#
# Revision 1.6  2008/02/07 20:08:24  bruno
# retooled the commands and database tables to handle moving running VMs
#
# Revision 1.5  2008/02/01 21:38:54  bruno
# closer
#
# Revision 1.4  2008/01/30 22:01:35  bruno
# closer
#
# Revision 1.3  2008/01/30 00:54:32  bruno
# need to make 'create' a real boolean
#
# Revision 1.2  2008/01/29 01:22:00  bruno
# support forcing a reinstall of a VM
#
# Revision 1.1  2008/01/29 00:06:45  bruno
# changed 'rocks config' to 'rocks report'
#
# Revision 1.2  2007/12/10 20:59:25  bruno
# fixes to get a VMs configured and running on newly installed xen-based
# physical machines.
#
# Revision 1.1  2007/12/03 19:48:51  bruno
# xen for V
#
#

import os
import sys
import string
import re
import tempfile
import rocks.commands
import rocks.vm

header = """
import os
import os.path
import sys
"""

#### Strings that will be placed in .cfg file that drives rocks-pygrub
installConfig = """
installKernel = %s
installRamdisk = %s
installBootArgs = %s
"""
bootConfig = """
bootKernel = %s
bootRamdisk = %s
bootArgs = %s
"""

forceConfig = """
forceInstall = True
"""

class Command(rocks.commands.report.host.command):
	"""
	Outputs a configuration file used by rocks-pygrub in order to boot a VM.
	
	<arg name='host' type='string'>
	One VM host name (e.g., compute-0-0-0).
	</arg>

	<example cmd='report host vm compute-0-0-0'>
	Create the VM configuration file for host compute-0-0-0
	</example>

	<example cmd='report host vm compute-0-0-0'>
	Create the VM configuration file for host compute-0-0-0.
	</example>
	"""

	def getDisks(self, host):
		#
		# get the VM disk specifications
		#
		rows = self.db.execute("""select vd.vbd_type, vd.prefix,
			vd.name, vd.device, vd.mode, vd.size from
			vm_disks vd, vm_nodes vn, nodes n where
			vd.vm_node = vn.id and vn.node = n.id and
			n.name = '%s' """ % host)

		disks = self.db.fetchall()
		if not disks:
			return

		vmdisks = []
		index = 0
		bootdisk = None
		bootdevice = None
		for vbd_type,prefix,name,device,mode,size in disks:
			#
			# if the disk specification is a 'regular' file, then
			# make sure the file for the disk space exists. if
			# it doesn't, create a sparse file for the disk space.
			#
			file = os.path.join(prefix, name)

			if vbd_type in [ 'file', 'tap:aio' ]:
				self.addOutput(host, 'disk = %s' % file)
				self.addOutput(host, 'disksize = %s' % size)
			elif vbd_type == 'phy':
				self.addOutput(host, 'disk = /dev/%s' % name)

	def getBootProfile(self, host, profile):
		"""Return what's defined by the named profile, Return
			string versions, empty strings if DB has Null entries"""

		kernel = '' 
		ramdisk =  ''
		bootargs = '' 
		if not profile:
			return kernel, ramdisk, bootargs

		# Read the profile
		rows = self.db.execute("""select kernel, ramdisk, args
			from bootaction where action = '%s' """ % profile)
		if rows > 0:
			kernel, ramdisk, bootargs = self.db.fetchone()

		if not kernel:
			kernel = ''
		if not ramdisk:
			ramdisk = ''
		if not bootargs:
			bootargs = ''

		return kernel, ramdisk, bootargs


	def outputVMConfig(self, host):
		#
		# lookup the boot and run profiles for this VM host. 
		# Also look up the bootaction for this VM host.
		#      if the bootaction is like 'install%' force install
		#          on next boot
		
		runAction = None
		installAction = None
		rows = self.db.execute("""select runaction, installaction
			from nodes where name = '%s' """ % host)
		if rows > 0:
			(runAction, installAction) = self.db.fetchone()
		
		# boot profile
		kern, ramdsk, bootargs = self.getBootProfile(host, runAction)
		self.addOutput(host, 'bootKernel = %s' % kern)
		self.addOutput(host, 'bootRamdisk = %s' % ramdsk)
		self.addOutput(host, 'bootArgs = %s' % bootargs)

		# install profile
		kern, ramdsk, bootargs = self.getBootProfile(host,
			installAction)

		#
		# append networking info onto the install boot args for
		# virtual frontends
		#
		ip = None
		netmask = None
		dns = None
		gateway = None
		if host in self.getHostnames( [ 'frontend' ]):
			subnet = 'public'
			
			rows = self.db.execute("""select net.ip, s.netmask from
				networks net,
				nodes n, subnets s where n.name='%s' and
				n.id = net.node and net.subnet = s.id and
				s.name = '%s' """ % (host, subnet))

			if rows > 0:
				(ip, netmask) = self.db.fetchone()

			dns = self.db.getHostAttr(host,
					'Kickstart_PublicDNSServers')

			for (key, val) in self.db.getHostRoutes(host).items():
				if key == '0.0.0.0' and val[0] == '0.0.0.0':
					gateway = val[1]

		if ip:
			bootargs += ' ip=%s ' % ip
		if netmask:
			bootargs += ' netmask=%s ' % netmask
		if dns:
			#
			# the user can enter in multiple DNS servers that are
			# separated by a comma. we can only supply one DNS
			# to anaconda, so let's just select the first one.
			#
			bootargs += ' dns=%s ' % dns.split(',')[0]
		if gateway:
			bootargs += ' gateway=%s ' % gateway

		self.addOutput(host, 'installKernel = %s' % kern)
		self.addOutput(host, 'installRamdisk = %s' % ramdsk)
		self.addOutput(host, 'installArgs = %s' % bootargs)

		# disk specifications
		self.getDisks(host)

		# Install?
		# look up the boot action
		bootaction = None
		rows = self.db.execute("""select b.action from boot b, nodes n
			where n.name = '%s' and n.id = b.node """ % host)

		if rows > 0:
			bootaction, = self.db.fetchone()
		else:
			#
			# if there is no bootaction for a node, assume
			# 'install'
			#
			bootaction = 'install'

		if bootaction == 'install':
			self.addOutput(host, 'forceInstall = yes')
	
				
	def run(self, params, args):
		hosts = self.getHostnames(args)

		if len(hosts) < 1:
			self.abort('must supply host')

		self.beginOutput()
		for host in hosts:
			try:
				self.outputVMConfig(host)
			except TypeError:
				pass

		self.endOutput(padChar='')
	

