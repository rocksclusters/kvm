# $Id: __init__.py,v 1.8 2012/11/27 00:49:07 phil Exp $
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
# Revision 1.8  2012/11/27 00:49:07  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.7  2012/05/06 05:49:15  phil
# Copyright Storm for Mamba
#
# Revision 1.6  2012/04/13 02:25:22  clem
# some nimor fixes to the documentation of the command
#
# Revision 1.5  2012/04/12 18:43:08  clem
# no more need to sync the network after add cluster, cleanup of useless code
#
# Revision 1.4  2012/04/10 22:41:18  clem
# virtual frontend should be destroied at the first reboot so they can boot as action=os
# no need to restart the network after rocks add cluster
#
# Revision 1.3  2012/03/24 02:40:47  clem
# New virtio driver for disk network
# New fixed version of the start up boot options
# New networking with bridges on every physical dev
#
# Revision 1.2  2012/03/23 01:26:38  clem
# only hvm is supported at the moment
#
# Revision 1.1  2012/03/17 02:52:29  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.30  2011/08/18 00:58:19  anoop
# Minor cleanup.
# Re-up the Release number
#
# Revision 1.29  2011/07/23 02:31:43  phil
# Viper Copyright
#
# Revision 1.28  2011/07/18 20:21:34  phil
# Give some diagnostics when creating a cluster.
# Support HVM_Features attribute to turn on/off services.
#
# Revision 1.27  2011/04/08 23:22:50  phil
# Ability to put frontend on arbitrary vm-container and set its name.
# If no Vm-containers specified and none exist, put "computes" on frontend so
# one can build a virtual cluster on a single physical node.
#
# Revision 1.26  2011/02/14 04:38:39  phil
# Explicitly state default for virtualization type
#
# Revision 1.25  2011/02/14 04:36:22  phil
# create cluster needs  a virt-type parameter, too.
#
# Revision 1.24  2011/01/04 23:53:01  bruno
# fix help
#
# Revision 1.23  2010/09/07 23:53:32  bruno
# star power for gb
#
# Revision 1.22  2010/08/30 22:58:41  bruno
# get rid of the FQDN requirement for 'rocks add cluster'
#
# Revision 1.21  2010/08/05 22:48:49  bruno
# associate an alias for the FQDN with the frontend VM (rather than assigning
# the FQDN to the public interface).
#
# Revision 1.20  2009/05/21 21:14:43  bruno
# tweaks
#
# Revision 1.19  2009/05/01 19:07:33  mjk
# chimi con queso
#
# Revision 1.18  2009/04/22 17:52:28  bruno
# allow the user to set the size of the frontend disk size.
#
# Revision 1.17  2009/03/30 19:15:46  bruno
# change first free VLAN id from 3 back to 2. this reverses a previous change.
# we found that the root cause of the problem was identical MAC addresses for
# the public side of virtual frontends. we not have a strategy to allocate
# unique MAC addresses for virtual clusters.
#
# Revision 1.16  2009/03/21 22:22:55  bruno
#  - lights-out install of VM frontends with new node_rolls table
#  - nuked 'site' columns and tables from database
#  - worked through some bugs regarding entities
#
# Revision 1.15  2009/02/12 05:15:35  bruno
# add and remove virtual clusters faster
#
# Revision 1.14  2009/02/09 00:29:04  bruno
# parallelize 'rocks sync host network'
#
# Revision 1.13  2009/01/14 00:20:55  bruno
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
# Revision 1.12  2009/01/07 18:55:41  bruno
# change first free VLAN id from 2 to 3.
#
# it seems that there are often problems with VLAN 2 going up and down while
# VLAN 3 is solid.
#
# Revision 1.11  2008/12/16 00:45:04  bruno
# merge vm_profiles and pxeaction tables into bootaction table
#
# Revision 1.10  2008/10/31 19:56:55  bruno
# one more fix
#
# Revision 1.9  2008/10/27 19:25:01  bruno
# folded 'rocks * host vm boot' commands into 'rocks * host vm'
#
# Revision 1.8  2008/10/18 00:56:22  mjk
# copyright 5.1
#
# Revision 1.7  2008/09/22 20:21:28  bruno
# add 'vlan' to the list of parameters
#
# Revision 1.6  2008/09/04 20:06:06  bruno
# thanks phil!
#
# Revision 1.5  2008/09/04 19:54:37  bruno
# use 'rocks set vm boot' to install VM frontends
#
# Revision 1.4  2008/09/04 15:54:16  bruno
# xen tweaks
#
# Revision 1.3  2008/08/27 22:22:02  bruno
# add a 'Hosted VM' appliance
#
# Revision 1.2  2008/08/22 23:25:56  bruno
# closer
#
# Revision 1.1  2008/08/20 22:52:58  bruno
# install a virtual cluster of any size in 6 simple steps!
#
#
#

import os
import rocks.commands

class Command(rocks.commands.add.command):
	"""
	Add a VM-based cluster to an existing physical cluster.
	
	<arg type='string' name='ip' optional='0'>
	The IP address for the virtual frontend.
	</arg>

	<arg type='string' name='num-computes' optional='0'>
	The number of compute nodes VMs to associate with the frontend.
	</arg>

	<param type='string' name='ip'>
	Can be used in place of the ip argument.
	</param>

	<param type='string' name='num-computes'>
	Can be used in place of the num-computes argument.
	</param>

	<param type='string' name='virt-type'>
	Defines the virtualization type as either paravirtualized (para) or
        Hardware Virtualized (hvm). KVM supports only hvm if you try to specify
	something else it will abort.
	</param>

	<param type='string' name='cpus-per-compute'>
	The number of CPUs to allocate to each VM compute node. The default
	is 1.
	</param>

	<param type='string' name='disk-per-compute'>
	The size of the disk (in gigabytes) to allocate to each VM compute
	node. The default is 36.
	</param>

	<param type='string' name='disk-per-frontend'>
	The size of the disk (in gigabytes) to allocate to the VM frontend
	node. The default is 36.
	</param>

	<param type='string' name='mem-per-compute'>
	The amount of memory (in megabytes) to allocate to each VM compute
	node. The default is 1024.
	</param>

	<param type='string' name='vlan'>
	The VLAN ID to assign to this cluster. All network communication
	between the nodes of the virtual cluster will be encapsulated within
	this VLAN.
	The default is the next free VLAN ID.
	</param>

	<param type='string' name='container-hosts'>
	A list of VM container hosts that will be used to hold the VM
	compute nodes. This must be a space-separated list (e.g.,
	container-hosts="vm-container-0-0 vm-container-0-1").
	The default is to allocate the compute nodes in a round robin fashion
	across all the VM containers.
	</param>

	<param type='string' name='fe-name'>
	name to for labeling the frontend. defaults to frontend-0-0-n, where
	n is assigned
	</param>

	<param type='string' name='fe-container'>
	Hosting machine for virtual frontend. Defaults to the physical frontend
	</param>

	<param type='bool' name='cluster-naming'>
	If true it will name the compute nodes not based on the physical node
	they are allocated but based on the fe-name.
	If the frontend is called cluster the compute nodes will be named:
	vm-cluster-0
	vm-cluster-1
	vm-cluster-2
	etc.
	</param>

	<example cmd='add cluster 1.2.3.4 2'>
	Create one frontend VM, assign it the IP address '1.2.3.4', and
	create 2 compute node VMs.
	</example>
	"""

	def getFreeVlan(self):
		#
		# make a list of the used vlan ids
		#
		self.db.execute("""select distinctrow vlanid from networks
			order by vlanid""")

		vlanids = []
		for v, in self.db.fetchall():
			if v:
				vlanids.append(v)

		#
		# find a free vlanid
		#
		for i in range(2, 4096):
			if i not in vlanids:
				return i

		return None


	def getVMContainers(self):
		containers = []

		#
		# now get all the VM containers
		#
		self.db.execute("""select n.name from nodes n, memberships m
			where n.membership = m.id and
			m.name = 'VM Container' """)
			
		for container, in self.db.fetchall():
			containers.append(container)

		return containers


	def getFrontend(self):
		fqdn = os.uname()[1]
		return fqdn.split('.')[0]


	def addVlanToHost(self, host, vlan, subnet):
		#
		# configure the vlan on host 
		#
		self.db.execute("""SELECT net.vlanid FROM networks net,nodes n 
			WHERE net.vlanid=%d 
			AND net.node=n.id AND n.name='%s' """ %(vlan,host))
		if self.db.fetchone() :
				# interface already exists. That's OK
				return
		try:
			output = self.command('add.host.interface', [ host,
				'iface=vlan%d' % vlan, 'subnet=%s' % subnet,
				'vlan=%d' % vlan])
		except:
			self.abort ("could not add vlan %d \
			(network=%s) for host %s\n" % (vlan, subnet,host))

	def createFrontend(self, vlan, subnet, ip, disksize, gateway, virtType, FEName, FEContainer):
		
		args = [ FEContainer, 'membership=Frontend', 'num-macs=2',
			'disksize=%s' % disksize, 'vlan=%d,0' % vlan,
			'sync-config=n', 'virt-type=%s' % virtType ]

		if FEName is not None:
			args.append('name=%s' % FEName)
		  
	
		self.addVlanToHost( FEContainer, vlan, subnet)

		output = self.command('add.host.vm', args)

		self.frontendname = None

		line = output.split()
		if line[0] == 'added' and line[1] == 'VM':
			self.frontendname = line[2]
		else:
			self.abort('failed to create a frontend VM on host %s'
				% FEContainer)

		#
		# configure the public network for the VM frontend
		#
		self.command('set.host.interface.subnet', [ self.frontendname,
			'eth1', 'public' ] )
		self.command('set.host.interface.ip', [ self.frontendname,
			'eth1', ip ] )
		if not gateway:
			gateway = self.db.getHostAttr(self.frontendname,
				'Kickstart_PublicGateway')
		self.command('add.host.route', [ self.frontendname, '0.0.0.0',
			gateway, 'netmask=0.0.0.0' ] )

		#
		# set the run and install actions for this VM
		#
		if virtType == 'hvm' :
			self.command('set.host.runaction', [ self.frontendname,
				'os' ] )
		else:
			self.command('set.host.runaction', [ self.frontendname,
				'none' ] )
		self.command('set.host.installaction', [ self.frontendname,
			'install vm frontend' ] )

		#
		# set the default boot action to be 'install'
		#
		self.command('set.host.boot', [ self.frontendname,
			'action=install' ] )

		print  '\tcreated frontend VM named: %s' % self.frontendname


	def createComputes(self, vlan, subnet, computes, containers,
		cpus_per_compute, mem_per_compute, 
		disk_per_compute, virtType, cluster_naming):

		self.computenames = []
		
		# If we have no VM-containers, then put all compute
                # VM's on the frontend

		if containers == []:
			containers.append(self.getFrontend())

		for i in range(0, computes):
			host = containers[i % len(containers)]

			self.addVlanToHost( host, vlan, subnet)
			args = [ host,
				'membership=Hosted VM', 'num-macs=1',
				'cpus=%s' % cpus_per_compute,
				'mem=%s' % mem_per_compute,
				'disksize=%s' % disk_per_compute,
				'vlan=%d' % vlan,
				'sync-config=n', 'virt-type=%s' % virtType ]

			if cluster_naming:
				#
				# compute nodes will be in the form of
				# vm-fename-ID
				#
				args.append('name=vm-' + cluster_naming +\
						'-%d' % i)

			output = self.command('add.host.vm', args)

			line = output.split()
			if line[0] == 'added' and line[1] == 'VM':
				self.computenames.append(line[2])
			else:
				self.abort('failed to create a compute VM ' + 
					'on host %s' % host)

			
			#
			# set the run and install actions for this VM
			#
			self.command('set.host.runaction', [ line[2], 
				'none' ] )
			if virtType == 'hvm' :
				installaction='install'
			else:
				installaction='install vm'

			self.command('set.host.installaction', [ line[2], 
				installaction ] )

			#
			# set the default boot action to be 'install'
			#
			self.command('set.host.boot', [ line[2], 
				'action=install' ] )

			print  '\tcreated compute VM named: %s' % line[2]


	def run(self, params, args):

		(args, ip, num_computes) = self.fillPositionalArgs(
			('ip', 'num-computes'))

		if not ip:
			self.abort('must supply an IP address for the frontend')
		if not num_computes:
			self.abort('must supply the number of compute nodes')

		try:
			computes = int(num_computes)
		except:
			self.abort('num-computes must be an integer')

		#
		# fillParams with the above default values
		#
		(cpus_per_compute, mem_per_compute, disk_per_compute,
			disk_per_frontend, container_hosts, vlan, subnet, gateway,
			virtType, FEName, FEContainer, cluster_naming) = \
			self.fillParams(
				[('cpus-per-compute', 1),
				('mem-per-compute', 1024),
				('disk-per-compute', 36),
				('disk-per-frontend', 36),
				('container-hosts', None),
				('vlan', None),
				('subnet', 'private'),
				('gateway', None),
				('virt-type','hvm'),
				('fe-name',None),
				('fe-container',self.getFrontend()),
				('cluster-naming', 'n')
				])

	
                cluster_naming = self.str2bool(cluster_naming)

		if cluster_naming and not FEName:
			self.abort("you must select a fe-name when using cluster-naming")

		virtType=virtType.lower()
		if virtType != 'hvm':
			self.abort("KVM support only 'hvm' virtualization")

		if vlan:
			try:
				vlanid = int(vlan)
			except:
				self.abort('Vlan ID (%s) must be an integer'
					% vlan)
		else:
			print "Getting Free VLAN --> "
			vlanid = self.getFreeVlan()
			print "<-- Done"

			if not vlanid:
				self.abort('could not find a free Vlan ID')

		if container_hosts:
			containers = container_hosts.split()
		else:
			containers = self.getVMContainers()
	
		#
		# create the frontend VM
		#
		print "Creating Virtual Frontend on Physical Host %s --> " % FEContainer 
		self.createFrontend(vlanid, subnet, ip, disk_per_frontend, gateway, 
				virtType, FEName, FEContainer)
		print "<-- Done."

		#
		# create the compute nodes
		#
		if computes > 0 :
			if cluster_naming:
				cluster_naming = FEName
			else:
				cluster_naming = None
			print "Creating %d Virtual Cluster nodes  --> " % computes 
			self.createComputes(vlanid, subnet, computes, containers,
				cpus_per_compute, mem_per_compute, 
				disk_per_compute, virtType, cluster_naming)
			print "<-- Done."

		#
		# reconfigure and restart the appropriate rocks services
		#
		print "Syncing Network Configuration --> " 
		self.command('sync.config')
		print "<-- Done."


