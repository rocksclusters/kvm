# $Id: __init__.py,v 1.5 2012/11/27 00:49:11 phil Exp $
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
# Revision 1.5  2012/11/27 00:49:11  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.4  2012/05/09 16:48:37  clem
# ported to rocks 5.5
#
# Revision 1.3  2012/05/06 05:49:18  phil
# Copyright Storm for Mamba
#
# Revision 1.2  2012/04/10 19:02:00  clem
# deprecated import sha removed
#
# Revision 1.1  2012/03/17 02:52:31  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.7  2011/08/16 15:05:13  anoop
# Bug fix.
# - Airboss service couldn't connect to the database
#   because it would fail to parse the password line in my.cnf
#   file correctly.
# - OperationalError needs to be scoped to the MySQLdb class. It
#   isn't available in the global context.
#
# Revision 1.6  2011/07/23 02:31:46  phil
# Viper Copyright
#
# Revision 1.5  2010/10/19 19:09:58  bruno
# a VM may not have a VLAN id associated with it (e.g., it may be controlled
# by a physical frontend). in that case, don't check the vlanid field. thanks
# to phil for identifying this bug.
#
# Revision 1.4  2010/09/07 23:53:33  bruno
# star power for gb
#
# Revision 1.3  2010/08/05 22:22:32  bruno
# optionally get the status of the VMs
#
# Revision 1.2  2010/08/05 20:06:29  bruno
# more airboss naming
#
# Revision 1.1  2010/08/04 23:37:44  bruno
# in with the airboss, out with the vm controller
#
# Revision 1.15  2010/08/03 23:57:28  bruno
# tweaks
#
# Revision 1.14  2010/07/29 21:28:44  bruno
# make sure to cleanup completed children
#
# Revision 1.13  2010/07/14 19:44:43  bruno
# open a new connection to the database on each received command. this prevents
# the case where the connect can become 'stale'.
#
# Revision 1.12  2010/07/07 23:18:39  bruno
# added 'power on + install' command
#
# Revision 1.11  2010/06/30 19:51:22  bruno
# fixes
#
# Revision 1.10  2010/06/30 17:59:58  bruno
# can now route error messages back to the terminal that issued the command.
#
# can optionally set the VNC viewer flags.
#
# Revision 1.9  2010/06/29 00:25:41  bruno
# a little code restructuring and now the console can handle reboots
#
# Revision 1.8  2010/06/25 20:29:20  bruno
# don't send a space character at the end of a console session
#
# Revision 1.7  2010/06/25 19:36:16  bruno
# tweaks
#
# Revision 1.6  2010/06/25 19:09:06  bruno
# tweak
#
# Revision 1.5  2010/06/24 23:43:51  bruno
# use libvirt to determine the VNC port number for a VM client
#
# Revision 1.4  2010/06/23 22:23:37  bruno
# fixes
#
# Revision 1.3  2010/06/22 21:41:14  bruno
# basic control of VMs from within a VM
#
# Revision 1.2  2010/06/21 22:47:06  bruno
# use new ssl python library
#
# Revision 1.1  2010/06/15 19:38:45  bruno
# start/stop the vmcontrol service
#
#

import socket
import ssl
import M2Crypto
import M2Crypto.BIO
import os
import sys
import MySQLdb
import subprocess
import select
import rocks.vm
import rocks.vmextended
import rocks.commands
import xml.sax.handler
import subprocess
import shlex
import time

sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt

#
# 'V' 'M' -- 86, 77 is decimal representation of 'V' 'M' in ASCII
#
port = 8677

#
# this class is used to get the VNC port number of a VM's console
#
class VirtHandler(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.port = '0'
 
	def startElement(self, name, attributes):
		if name == "graphics":
			self.port = attributes["port"]


class Command(rocks.commands.start.service.command):
	"""
	Starts the VM Control service. This service validates commands from
	remote hosts and, if the command is accepted, the command is parsed
	and applied to VMs that are managed by this host.

	<param type='boolean' name='foreground'>
	If set to to 'yes', this service will stay in the foreground. Default
	is 'no'.
	</param>
	"""

	def Abort(self, msg):
		print 'abort: msg: ', msg
		sys.stdout.flush()
		

	def reconnect(self):
		#
		# reconnect to the database
		#

		# First try to read the cluster password (for apache)

		passwd = ''

		try:
			file = open('/opt/rocks/etc/my.cnf','r')
			for line in file.readlines():
				l = line[:-1].split('=')
				if len(l) > 1 and l[0].strip() == "password":
					passwd = l[1].strip()
					break
			file.close()
		except:
			pass

		try:
			host = rocks.DatabaseHost
		except:
			host = 'localhost'

		# Now make the connection to the DB

		try:
			if os.geteuid() == 0:
				username = 'apache'
			else:
				username = pwd.getpwuid(os.geteuid())[0]

			# Connect over UNIX socket if it exists, otherwise go
			# over the network.

			if os.path.exists('/var/opt/rocks/mysql/mysql.sock'):
				Database = MySQLdb.connect(db='cluster',
					host='localhost',
					user=username,
					passwd='%s' % passwd,
					unix_socket='/var/opt/rocks/mysql/mysql.sock')
			else:
				Database = MySQLdb.connect(db='cluster',
					host='%s' % host,
					user=username,
					passwd='%s' % passwd,
					port=40000)

		except ImportError:
			Database = None
		except MySQLdb.OperationalError:
			Database = None
	
		return (Database)


	def get_fename(self, host_name):
		#
		# return the frontend name associated with this 
		# host_name
		#
		fe_name = ''

		try:
			host = self.db.getHostname(host_name)
		except:
			host = None
		
		if not host:
			return fe_name

		vm = rocks.vm.VM(self.db)
		if vm.isVM(host):
			#
			# get the cluster name
			#
			rows = self.db.execute("""select cluster_name 
				from clusters cl, nodes n, networks net 
				where n.name = '%s' and n.id = net.node 
				and cl.vlanid = net.vlanid"""  % host)

			if rows == 0:
				#
				# this is a virtual node belonging to the physical
				# frontend, or it's a really bad error!!
				#
				print "airbos does not support turning on and off "\
					"nodes which belongs to the physical frontend"

			elif rows > 0:
				fe_name, = self.db.fetchone()

		return fe_name


	def getVNCport(self, client, physnode):
		import rocks.vmconstant
		h = libvirt.open(rocks.vmconstant.connectionURL % physnode)

		for id in h.listDomainsID():
			if id == 0:
				#
				# skip dom0
				#
				continue

			domU = h.lookupByID(id)
			if domU.name() == client:
				parser = xml.sax.make_parser()
				handler = VirtHandler()
				parser.setContentHandler(handler)
				parser.feed(domU.XMLDesc(0))

				return handler.port

		return ''


	def openTunnel(self, client, physnode, fds):
		#
		# open an ssh tunnel
		#
		vncport = self.getVNCport(client, physnode)
		if not vncport:
			print 'could not get VNC port for %s' % client
			sys.stdout.flush()
			return None

		print '\tconnecting console on physical host %s port %s' % \
			(physnode, vncport)

		pid = os.fork()
		if pid == 0:
			fds[0].close()

			os.close(0)
			os.close(1)

			os.dup(fds[1].fileno())
			os.dup(fds[1].fileno())

			cmd = ['ssh', 'ssh', physnode, 'nc', 'localhost',
				vncport]

			os.execlp(*cmd)

			file = open('/tmp/vs.debug', 'w')
			file.write('died')
			file.close()
			os._exit(1)

		#
		# parent
		#
		fds[1].close()
		return fds[0].fileno()


	def console(self, s, clientfd, dst_mac):
		client = self.db.getHostname(dst_mac)
		if not client:
			self.sendresponse(s, -1,
				'MAC address %s not in database' % dst_mac)
			return

		vm = rocks.vmextended.VMextended(self.db)
		(physnodeid, physnode) = vm.getPhysNode(client)

		if not physnode:
			msg = 'could not find the physical host that controls'
			msg += ' the VM for MAC address %s' % dst_mac
			self.sendresponse(s, -1, msg)
			return

		fds = socket.socketpair()
		fd = self.openTunnel(client, physnode, fds)
		if not fd:
			msg = 'could not open a ssh tunnel to the physical '
			msg += 'host %s' % physnode
			self.sendresponse(s, -1, msg)
			return

		#
		# the connection is good. send back a status of 0 and an
		# empty 'reason' message
		#
		self.sendresponse(s, 0, '')

		done = 0
		while not done:
			retval = 0

			(i, o, e) = select.select([fd], [], [], 0.00001)
			if fd in i:
				buf = os.read(fd, 8192)
				if len(buf) == 0:
					try:
						fd.close()
					except:
						pass

					#
					# the VNC server on the remote end
					# shutdown. this may be because the
					# node rebooted. try to reestablish
					# a connection
					#
					done = 1
				try:
					self.sendresponse(s, 0, buf)
				except:
					done = 1
					continue

			(i, o, e) = select.select([clientfd], [], [], 0.00001)
			if clientfd in i:
				try:
					buf = s.read()
					if len(buf) == 0:
						done = 1
						continue

					
					bytes = 0
					while bytes != len(buf):
						bytes += os.write(fd,
							buf[bytes:])
				except:
					done = 1
					continue

		return

	def cdrom(self, socket, dst_mac, op):
		"""invoke the rocks set host vm cdrom"""

		client = self.db.getHostname(dst_mac)

		ops = op.split(' ')

		if len(ops) == 1:
			cmd = """/opt/rocks/bin/rocks set host vm cdrom %s cdrom='none'"""\
					% client
		elif len(ops) == 2:
			filename = ops[1]
			# TODO do more checking on the cdrom file name
			if '..' in filename:
				self.sendresponse(socket, -1, "invalid path")
				return

			cmd = """/opt/rocks/bin/rocks set host vm cdrom %s cdrom='%s'"""\
                                        % (client, filename)
		elif len(ops) > 2:
			self.sendresponse(socket, -1, "invalid path")
			return

		p = subprocess.Popen(shlex.split(cmd),
			stdin = subprocess.PIPE,
			stdout = subprocess.PIPE,
			stderr = subprocess.STDOUT)
		p.wait()

		response = ''
		for line in p.stdout.readlines():
			response += line

		status = 0
		if len(response) > 0:
			status = -1

		self.sendresponse(socket, status, response)


	def power(self, s, action, dst_mac):
		cmd = '/opt/rocks/bin/rocks %s host vm %s' % (action, dst_mac)

		p = subprocess.Popen(shlex.split(cmd),
			stdin = subprocess.PIPE,
			stdout = subprocess.PIPE,
			stderr = subprocess.STDOUT)
		p.wait()

		response = ''
		for line in p.stdout.readlines():
			response += line

		status = 0
		if len(response) > 0:
			status = -1

		self.sendresponse(s, status, response)


	def parse_msg(self, buf):
		b = buf.split('\n')

		op = b[0].strip()

		if len(b) > 1:
			dst_mac = b[1].strip()
		else:
			dst_mac = ''

		return (op, dst_mac)


	def check_signature(self, clear_text, signature, fe_name):
		#
		# get the keys for this fe_name
		#
		rows = self.db.execute("""select pk.public_key
				from public_keys pk, nodes n
				where pk.node = n.id and
				n.name = '%s'""" % fe_name)

		if rows == 0:
			#
			# no keys were found
			#
			return 0

		try:
			import hashlib
			digest = hashlib.sha1(clear_text).digest()
		except ImportError:
			import sha
			digest = sha.sha(clear_text).digest()

		for public_key, in self.db.fetchall():
			bio = M2Crypto.BIO.MemoryBuffer(public_key)
			key = M2Crypto.RSA.load_pub_key_bio(bio)

			try:
				verify = key.verify(digest, signature)
				if verify == 1:
					return 1
			except:
				pass

		return 0


	def daemonize(self):
		#
		# The python Daemon dance. From Steven's "Advanced Programming
		# in the UNIX env".
		#
		pid = os.fork()
		if pid > 0:
			sys.exit(0)

		#
		# now decouple from parent environment
		#

		#
		# So we can remove/unmount the dir the daemon started in.
		#
		os.chdir("/")

		#
		# Create a new session and set the process group.
		#
		os.setsid()
		os.umask(0)

		#
		# do a second fork
		#
		pid = os.fork()
		if pid > 0:
			#
			# exit from second parent
			#
			sys.exit(0)

		#
		# redirect standard file descriptors
		#
		sys.stdout.flush()
		sys.stderr.flush()
		si = file('/dev/null', 'r')
		so = file('/var/log/airboss.log', 'a+')
		se = so
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())


	def sendresponse(self, s, status, response):
		msg = 'status:%d\n' % status
		msg += response

		#
		# send the length of the message
		#
		msglen = '%08d\n' % len(msg)

		bytes = 0
		while bytes != len(msglen):
			bytes += s.write(msglen[bytes:])

		#
		# now send the contents of the message
		#
		bytes = 0
		while bytes != len(msg):
			bytes += s.write(msg[bytes:])



	def listmacs(self, s, fe_name, status):


		resp = ''
		self.db.execute("""select n.name, net.mac, ali.name as alias
				from clusters cl, networks net, vm_nodes vmn, nodes n
				left join aliases ali on n.id = ali.node
				where n.id = net.node and n.id = vmn.node
				and net.vlanid = cl.vlanid
				and cl.cluster_name = '%s'""" % fe_name)

		aliases = {}
		macs = {}


		for (name, mac, alias) in self.db.fetchall():
			macs[name] = mac
			if alias:
				if name in aliases:
					aliases[name].append(alias)
				else:
					aliases[name] = [alias]

		if status:
			vm = rocks.vmextended.VMextended(self.db)

		for name in sorted(macs.keys()):
			resp += macs[name] + ' '
			if status:
				state = 'nostate'
				resp += vm.getStatus(name) + ' '

			resp += name
			if name in aliases:
				resp += ',' + ','.join(aliases[name])

			resp += '\n'

		self.sendresponse(s, 0, resp)


	def dorequest(self, conn):
		s = ssl.wrap_socket(conn,
			server_side = True,
			keyfile = '/etc/pki/libvirt/private/serverkey.pem',
			certfile = '/etc/pki/libvirt/servercert.pem',
			ssl_version = ssl.PROTOCOL_SSLv23)
		
		#
		# read the length of the clear text
		#
		buf = ''
		while len(buf) != 9:
			buf += s.read(1)

		try:
			clear_text_len = int(buf)
		except:
			s.close()
			conn.close()
			return

		#
		# now read the clear text
		#
		clear_text = ''
		while len(clear_text) != clear_text_len:
			msg = s.read(clear_text_len - len(clear_text))
			clear_text += msg

		(op, dst_mac) = self.parse_msg(clear_text) 

		print '\top:\t\t%s' % op
		print '\tdst_mac:\t%s' % dst_mac
		sys.stdout.flush()

		#
		# get the digital signature
		#
		buf = ''
		while len(buf) != 9:
			buf += s.read(1)

		try:
			signature_len = int(buf)
		except:
			s.close()
			conn.close()
			return

		signature = ''
		while len(signature) != signature_len:
			msg = s.read(signature_len - len(signature))
			signature += msg

		#
		# check the signature
		#
		fe_name = self.get_fename(dst_mac)

		if fe_name == '':
			self.sendresponse(s, -1,
				'host %s not in database' % dst_mac)
			s.close()
			conn.close()
			return

		if self.check_signature(clear_text, signature, fe_name):
			print '\tmessage signature is valid'
			sys.stdout.flush()

			if op == 'power off':
				self.power(s, 'stop', dst_mac)
			elif op == 'power on':
				self.power(s, 'start', dst_mac)
			elif op == 'power on + install':
				self.command('set.host.boot', [ dst_mac,
					'action=install'])
				self.power(s, 'start', dst_mac)
			elif op == 'list macs + status':
				self.listmacs(s, fe_name, 1)
			elif op == 'list macs':
				self.listmacs(s, fe_name, 0)
			elif op == 'console':
				self.console(s, conn.fileno(), dst_mac)
			elif op.startswith('cdrom'):
				self.cdrom(s, dst_mac, op)
			else:
				print '\tcommand is invalid'
				sys.stdout.flush()
				self.sendresponse(s, -1, 'command is invalid')
		else:
			print '\tmessage signature is invalid'
			sys.stdout.flush()

			self.sendresponse(s, -1, 'message signature is invalid')
		try:
			s.shutdown(socket.SHUT_RDWR)
			conn.shutdown(socket.SHUT_RDWR)
		except:
			pass

		s.close()
		conn.close()


	def cleanupchildren(self):
		done = 0
		while not done:
			try:
				(pid, status) = os.waitpid(0, os.WNOHANG)
				if pid == 0:
					done = 1
			except:
				done = 1


	def run(self, params, args):
		foreground, = self.fillParams([ ('foreground', 'n') ])

		if not self.str2bool(foreground):
			self.daemonize()

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setblocking(0)
		sock.bind(('', port))
		sock.listen(1)

		print 'airboss started at %s\n' % time.asctime()
		sys.stdout.flush()

		done = 0
		while not done:
			conn = None
			while not conn:
				try:
					conn, addr = sock.accept()
				except:
					self.cleanupchildren()
					time.sleep(0.1)

			print 'received message from: ', addr
			sys.stdout.flush()

			#
			# for a child process to handle the request
			#
			pid = os.fork()
			if pid == 0:
				#
				# after this program becomes a daemon, we need
				# to get a new connect to the database. that
				# is because the parent closes the initial
				# database connection
				#
				database = self.reconnect()

				if not database:
					print "couldn't connect to the " + \
						"database"
					sys.stdout.flush()
				else:
					self.db.database = database
					self.db.link = database.cursor()
					self.dorequest(conn)
					database.close()

				os._exit(0)
			else:
				conn.close()

