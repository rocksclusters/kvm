# $Id: __init__.py,v 1.1 2012/03/17 02:52:29 clem Exp $
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
copyfile = """/opt/rocks/bin/python -c 'import os
import os.path
import sys

srchost = \\"%s\\"
srcfile = \\"%s\\"
srcstat = %s
destfile = \\"%s\\"

if os.path.exists(srcfile) and os.stat(srcfile) == srcstat:
	sys.exit(0)

try:
	os.makedirs(os.path.dirname(destfile))
except:
	pass
cmd = \\"scp -q \\" + srchost + \\":\\" + srcfile + \\" \\" + destfile
cmd += \\" > /dev/null 2>&1\\"
os.system(cmd)' """

statcmd = """/opt/rocks/bin/python -c 'import os
try:
	print os.stat(\\"%s\\")
except:
	pass' """


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

		if not file:
			filename = '%s.saved' % host

			fromdiskprefix = vm.getLargestPartition(fromphyshost)
			fromdir = os.path.join(fromdiskprefix, 'xen/disks')
			fromsavefile = os.path.join(fromdir, filename)
		else:
			fromsavefile = file

		print "Saving the VM's current state."

		#
		# save the VM's running state
		#
		self.command('save.host.vm', [ host, "file=%s" % fromsavefile] )

		fromsavefilestat = self.command('run.host', [ fromphyshost,
			statcmd % fromsavefile ]).strip()

		print "Copying the VM's current state to %s." % (tophyshost)

		#
		# copy the VM save file to the physical node
		# running state
		#
		todiskprefix = vm.getLargestPartition(tophyshost)
		todir = os.path.join(todiskprefix, 'xen/disks')
		tosavefile = os.path.join(todir, filename)

		cmd = copyfile % (fromphyshost, fromsavefile, fromsavefilestat,
			tosavefile)
		debug = self.command('run.host',
			[ tophyshost, 'command=%s' % cmd ])

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
				filestat = self.command('run.host',
					[ fromphyshost,
					statcmd % filename ]).strip()

				print "Moving virtual disk (%s) to %s" % \
					(filename, tophyshost)

				toprefix = vm.getLargestPartition(tophyshost)
				todir = os.path.join(toprefix, 'xen/disks')
				tofile = os.path.join(todir, name)

				cmd = copyfile % (fromphyshost, filename,
					filestat, tofile)
				debug = self.command('run.host',
					[ tophyshost, 'command=%s' % cmd ])
				# print 'run.host output: ', debug

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
		# remove the VM configuration file on the 'from' physical host
		#
		cmd = 'rm -f /etc/xen/rocks/%s' % host
		self.command('run.host', [ fromphyshost, 'command=%s' % cmd ])

		#
		# restore the VM's running state
		#
		print "Restarting the VM on %s." % (tophyshost)
		self.command('restore.host.vm', [ host, "file=%s" % tosavefile])


