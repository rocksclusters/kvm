# $Id: __init__.py,v 1.9 2012/11/27 00:49:08 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWindwer)
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
# Revision 1.9  2012/11/27 00:49:08  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.8  2012/05/06 05:49:16  phil
# Copyright Storm for Mamba
#
# Revision 1.7  2012/04/19 05:12:05  clem
# More fixes on the rocks move host vm
# Tested and fixed the test_vm.sh procedure
#
# Revision 1.6  2012/04/13 01:47:12  clem
# More fixes in the move command
#
# Revision 1.5  2012/04/12 18:43:44  clem
# bug fix, vlan interface must be created on the physical destination host
#
# Revision 1.4  2012/04/11 17:39:36  clem
# add a check to see if destination host = to source host
#
# Revision 1.3  2012/04/08 00:49:59  clem
# code refactoring (added a new command sync host vlan)
# Fixed the restore and move command
#
# Revision 1.2  2012/03/31 01:07:28  clem
# latest version of the networking for kvm (vlan out of redhat network script)
# minor fixes here and there to change the disks path from /state/partition1/xen/disks
# to /state/partition1/kvm/disks
#
# Revision 1.1  2012/03/17 02:52:29  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.9  2011/07/23 02:31:44  phil
# Viper Copyright
#
# Revision 1.8  2010/09/07 23:53:32  bruno
# star power for gb
#
# Revision 1.7  2009/05/01 19:07:34  mjk
# chimi con queso
#
# Revision 1.6  2008/10/18 00:56:23  mjk
# copyright 5.1
#
# Revision 1.5  2008/04/17 16:38:21  bruno
# incorporate phil's vm changes
#
# Revision 1.4  2008/03/06 23:42:04  mjk
# copyright storm on
#
# Revision 1.3  2008/02/19 23:20:24  bruno
# katz made me do it.
#
# Revision 1.2  2008/02/12 00:01:25  bruno
# fixes
#
# Revision 1.1  2008/02/07 20:08:24  bruno
# retooled the commands and database tables to handle moving running VMs
#
#

import os
import rocks.commands
import rocks.vm


#
# code to copy a file from one host to another
#

preparedir = """ssh %s mkdir -p `dirname %s`"""
copycmd = """ssh %s cat %s | ssh %s dd of=%s """



class Command(rocks.commands.move.host.command):
	"""
	Move a VM from its current physical node to another.

	<arg type='string' name='host'>
	The name of the VM host to move.
	</arg>

	<arg type='string' name='physhost'>
	The name of the physical host in which to move the VM.
	</arg>

	<arg type='string' name='file'>
	The name of the file that stores the running VM's state.
	</arg>

	<example cmd='move host vm compute-0-0-0 vm-container-1-0'>
	Move VM host compute-0-0-0 to physical host vm-container-1-0.
	</example>
	"""



	def addVlanToHost(self, host, vlan, subnet):
		#TODO this code is copied from add/cluster/__init__.py

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



	def run(self, params, args):
		(args, tophyshost) = self.fillPositionalArgs(('physhost', ))
		file, = self.fillParams( [('file', None)] )
		
		if len(args) != 1:
			self.abort('must supply only one VM host')

		vm = rocks.vm.VM(self.db)

		#
		# validate the 'to' physical host name
		#
		h = self.getHostnames([ tophyshost ])

		hosts = self.getHostnames(args)
		host = hosts[0]
		fromphyshost = vm.getPhysHost(host)

		if tophyshost == fromphyshost:
			self.abort("The source physical host, and the destination " +
				"host are the same: " + tophyshost)

		if not file:
			filename = '%s.saved' % host

			fromdiskprefix = vm.getLargestPartition(fromphyshost)
			fromdir = os.path.join(fromdiskprefix, 'kvm/disks')
			fromsavefile = os.path.join(fromdir, filename)
		else:
			fromsavefile = file

		print "Saving the VM's current state."

		#
		# save the VM's running state
		#
		self.command('save.host.vm', [ host, "file=%s" % fromsavefile] )

		#
		# copy the VM save file to the physical node
		# running state
		#
		todiskprefix = vm.getLargestPartition(tophyshost)
		todir = os.path.join(todiskprefix, 'kvm/disks')
		tosavefile = os.path.join(todir, filename)

		#make the directory
		#I can not use run.command cos it doesn't return the exit status 
		cmd = preparedir % (tophyshost, tosavefile)
		debug = os.system(cmd)
		if debug != 0 :
			self.abort("Unabled to create destination directory on physical host, " 
				+ tophyshost)

		#copy the file
		cmd = copycmd % (fromphyshost, fromsavefile, 
			tophyshost, tosavefile)
		debug = os.system(cmd)
		if debug != 0 :
			self.abort("Unabled to copy vm state on the new physical host, " 
				+ tophyshost)

		#
		# copy the VMs disks to the 'from' host
		#
		rows = self.db.execute("""select vn.id from vm_nodes vn,
			nodes n where n.name = "%s" and vn.node = n.id""" 
			% host)	
		if rows < 1:
			return

		vmnodeid, = self.db.fetchone()

		rows = self.db.execute("""select vbd_type, prefix, name from
			vm_disks where vm_node = %s""" % vmnodeid)

		if rows > 0:
			for vbd_type, prefix, name in self.db.fetchall():
				if vbd_type not in [ 'tap:aio', 'file' ]:
					continue

				print "Copying VM disk file to %s." % tophyshost

				filename = os.path.join(prefix, name)

				print "Moving virtual disk (%s) to %s" % \
					(filename, tophyshost)

				toprefix = vm.getLargestPartition(tophyshost)
				todir = os.path.join(toprefix, 'kvm/disks')
				tofile = os.path.join(todir, name)

	
				#make the directory
				cmd = preparedir % (tophyshost, tofile)
				debug = os.system(cmd)
				if debug != 0 :
					self.abort("Unabled to create destination " 
						+"directory on physical host, " + tophyshost)
		
				#copy the file
				cmd = copycmd % (fromphyshost, filename, tophyshost, tofile)
				debug = os.system(cmd)
				if debug != 0 :
					self.abort("Unabled to copy vm state on the new "
						+ "physical host, " + tophyshost)


				#
				# update the disk specification in the database
				#
				self.db.execute("""update vm_disks set
					prefix = "%s" where vm_node = %s"""
					% (todir, vmnodeid))

		#
		# update which physical node now houses this VM
		#
		rows = self.db.execute("""select id from nodes where
			name = "%s" """ % (tophyshost))
		if rows < 1:
			return

		physhostid, = self.db.fetchone()

		self.db.execute("""update vm_nodes set physnode = %s where
			id = %s """ % (physhostid, vmnodeid))

		#
		# update vlan on physhostid if it is not already present
		#
		rows = self.db.execute("""select vlanid from networks as net, nodes as n 
				where n.id = net.node and n.name='%s'""" % host)
		if rows < 1:
			self.abort("Unable to find vlanid for host " + host)
		vlanid, = self.db.fetchone()

		if vlanid != None:
			# we are moving a virtual cluster node
			# hence we need to move its' vlan as well
			rows = self.db.execute("""select sub.name  
				from networks as net, nodes as n, subnets sub 
				where n.name='%s' and net.vlanid=%s 
				and n.id=net.node and sub.id=net.subnet""" %
				(tophyshost, vlanid))
			if rows < 1:
				self.abort("Unable to find subnet for host migration")
			subnet, = self.db.fetchone()

			self.addVlanToHost(tophyshost, vlanid, subnet)

		#
		# restore the VM's running state
		#
		print "Restarting the VM on %s." % (tophyshost)
		self.command('restore.host.vm', [ host, "file=%s" % tosavefile])



RollName = "kvm"
