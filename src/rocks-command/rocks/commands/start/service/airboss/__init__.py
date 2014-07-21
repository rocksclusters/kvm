#!/opt/rocks/bin/python
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

import socket
import ssl
import M2Crypto
import M2Crypto.BIO
import logging
import syslog
import os
import sys
import select
import threading
import xml.sax.handler
import daemon.runner

import SocketServer


import rocks.db.vmextend
import rocks.commands
import rocks.commands.start.service


sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt

#
# 'V' 'M' -- 86, 77 is decimal representation of 'V' 'M' in ASCII
#
port = 8677

logfile = "/var/log/airboss.log"
logger = logging.getLogger("Airboss")

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

	def run(self, params, args):
		foreground, = self.fillParams([ ('foreground', 'n') ])
		foreground = self.str2bool(foreground)

		app = Airboss()
		AirbossTCPHandler.command = self
		formatter = logging.Formatter(
			"%(asctime)s - %(levelname)s - %(message)s")
		logger.setLevel(logging.DEBUG)

		if foreground:
			# just run the app no need for daemonization
			ch = logging.StreamHandler(sys.stdout)
			ch.setLevel(logging.DEBUG)
			ch.setFormatter(formatter)
			logger.addHandler(ch)
			app.run()
		else:
			# redirecting the logger to the logfile
			handler = logging.FileHandler(logfile)
			handler.setLevel(logging.INFO)
			handler.setFormatter(formatter)
			logger.addHandler(handler)
			# redirection stdout and err to the logger
			# in case we get a stack trace
			daemon_runner = MydaemonRunnner(app)
			# This ensures that the logger file handle does not 
			# get closed during daemonization
			daemon_runner.daemon_context.files_preserve = \
							[handler.stream]
			# close all the fs descriptor before forking
			syslog.closelog()
			# we don't need the runnner to parse input line
			# since we already did it
			daemon_runner._start()
		

class MydaemonRunnner(daemon.runner.DaemonRunner):
	"""we need to subclass the (stupid) DaemonRunner so that it does
	not wipe the stdout and stderr everytimes it re-start"""


	def __init__(self, app):
		""" Set up the parameters of a new runner.

		The `app` argument must have the following attributes:

		* `stdin_path`, `stdout_path`, `stderr_path`: Filesystem
		  paths to open and replace the existing `sys.stdin`,
		  `sys.stdout`, `sys.stderr`.

		* `pidfile_path`: Absolute filesystem path to a file that
		  will be used as the PID file for the daemon. If
		  ``None``, no PID file will be used.

		* `pidfile_timeout`: Used as the default acquisition
		  timeout value supplied to the runner's PID lock file.

		* `run`: Callable that will be invoked when the daemon is
		  started.
		    cut and past from python libs
		"""
		self.parse_args()
		self.app = app
		self.daemon_context = daemon.daemon.DaemonContext()
		self.daemon_context.stdin = open(app.stdin_path, 'r')
		self.daemon_context.stdout = open(app.stdout_path, 'a+')
		self.daemon_context.stderr = open(
		    app.stderr_path, 'a+', buffering=0)

		self.pidfile = None
		if app.pidfile_path is not None:
		    self.pidfile = daemon.runner.make_pidlockfile(
		        app.pidfile_path, app.pidfile_timeout)
		self.daemon_context.pidfile = self.pidfile



class AirbossTCPHandler(SocketServer.BaseRequestHandler):
	"""
	The RequestHandler class for Airboss.
	
	It is instantiated once per connection by the server, and handle
	is called thereafter.

	Most of the method have been copyed from the old Command class
	now they could use instance variable to store state.
	"""

	# hold a reference to the rocks.commands.Command class
	command = None

	def get_fename(self, node):
		#
		# return the frontend name associated with this 
		# host_name
		#
		if node.vm_defs:
			#
			# get the cluster name
			#
			self.clusters = self.command.newdb.getVClusters()
			for fe_name in self.clusters.getFrontends():
				if node.name == fe_name or \
					node.name in self.clusters.getNodes(fe_name):
					return fe_name
			logger.debug('Unable to find %s in vclusters' % node.name)

		return None


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
			logger.error('could not get VNC port for %s' % client)
			return None

		logger.debug('connecting console on physical host %s port %s' % \
			(physnode, vncport))

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


	def console(self, s, clientfd, node):

		if not node.vm_defs or not node.vm_defs.physNode:
			msg = 'could not find the physical host that controls'
			msg += ' the VM for MAC address %s' % dst_mac
			self.sendresponse(s, -1, msg)
			return

		physnode = node.vm_defs.physNode.name

		fds = socket.socketpair()
		fd = self.openTunnel(node.name, physnode, fds)
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

	def cdrom(self, socket, node, op):
		"""invoke the rocks set host vm cdrom"""
		ops = op.split(' ')

		if len(ops) == 1:
			filename = 'none'
		elif len(ops) == 2:
			filename = ops[1]
			# TODO do more checking on the cdrom file name
			if '..' in filename:
				self.sendresponse(socket, -1, "invalid path")
				return
		elif len(ops) > 2:
			self.sendresponse(socket, -1, "invalid path")
			return

		response = self.command.command('set.host.vm.cdrom', 
				[node.name, 'cdrom=%s' % filename])

		status = 0
		if len(response) > 0:
			status = -1

		self.sendresponse(socket, status, response)


	def power(self, s, action, node_name):

		try:
			response = self.command.command(action + '.host.vm', \
						[node_name])

		except rocks.util.CommandError, e:
			self.sendresponse(s, -1, str(e))
			return

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
		rows = self.command.db.execute("""select pk.public_key
				from public_keys pk, nodes n
				where pk.node = n.id and
				n.name = '%s'""" % fe_name)

		if rows == 0:
			#
			# no keys were found
			#
			logger.debug('no keys found for %s' % fe_name)
			return False

		try:
			import hashlib
			digest = hashlib.sha1(clear_text).digest()
		except ImportError:
			import sha
			digest = sha.sha(clear_text).digest()

		for public_key, in self.command.db.fetchall():
			bio = M2Crypto.BIO.MemoryBuffer(public_key)
			key = M2Crypto.RSA.load_pub_key_bio(bio)

			try:
				verify = key.verify(digest, signature)
				if verify == 1:
					return True
			except Exception, e:
				logger.debug('host %s key %s failed (%s)' % 
						(fe_name, public_key, str(e)))
				pass

		return False



	def sendresponse(self, s, status, response):
		msg = 'status:%d\n' % status
		msg += response

		#
		# send the length of the message
		#
		msglen = '%08d\n' % len(msg)

		s.sendall(msglen)

		#
		# now send the contents of the message
		#
		s.sendall(msg)


	def listmacs(self, s, fe_name, status):
		"""send a listmacs response"""

		node_names = self.clusters.getNodes(fe_name) + [fe_name]
		vlan = self.clusters.getVlan(fe_name)

		resp = ''
		for node in self.command.newdb.getNodesfromNames(node_names, 
				preload=['networks', 'aliases', 'vm_defs']):

			for net in node.networks:
				if net.vlanID == vlan:
					resp += net.mac + ' '

			if status:
				resp += rocks.db.vmextend.getStatus(node) + ' '

			resp += node.name
			for alias in node.aliases:
				resp += ',' + alias.name

			resp += '\n'

		self.sendresponse(s, 0, resp)



	def handle(self):
		# self.request is the TCP socket connected to the client
		logger.debug('received connection from: ' + str(self.client_address))

		s = ssl.wrap_socket(self.request,
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
			return

		#
		# now read the clear text
		#
		clear_text = ''
		while len(clear_text) != clear_text_len:
			msg = s.read(clear_text_len - len(clear_text))
			clear_text += msg

		(op, dst_mac) = self.parse_msg(clear_text) 

		logger.debug('op:\t\t%s' % op)
		logger.debug('dst_mac:\t%s' % dst_mac)

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
			return

		signature = ''
		while len(signature) != signature_len:
			msg = s.read(signature_len - len(signature))
			signature += msg


		# get the node from the DB
		try:
			node = self.command.newdb.getNodesfromNames([dst_mac], 
				preload=['vm_defs', 'networks', 'public_keys'])[0]
		except Exception, e:
			logger.error('host %s not found (%s)', dst_mac, str(e))
			s.close()
			return

		#
		# check the signature
		#
		fe_name = self.get_fename(node)
		if not fe_name:
			self.sendresponse(s, -1,
				'host %s is not part of a virtaul cluster' % 
						dst_mac)
			s.close()
			return

		if self.check_signature(clear_text, signature, fe_name):
			logger.info('valid op: ' + op + ' from: ' + \
					str(self.client_address))

			if op == 'power off':
				self.power(s, 'stop', node.name)
			elif op == 'power on':
				self.power(s, 'start', node.name)
			elif op == 'power on + install':
				self.command.command('set.host.boot', [ node.name,
					'action=install'])
				self.power(s, 'start', node.name)
			elif op == 'list macs + status':
				self.listmacs(s, fe_name, 1)
			elif op == 'list macs':
				self.listmacs(s, fe_name, 0)
			elif op == 'console':
				self.console(s, self.request.fileno(), node)
			elif op.startswith('cdrom'):
				self.cdrom(s, node, op)
			else:
				logger.error('command is invalid')
				self.sendresponse(s, -1, 'command is invalid')
		else:
			logger.info('invalid op: '+ op + ' from: ' + \
					str(self.client_address))

			self.sendresponse(s, -1, 'message signature is invalid')
		try:
			s.shutdown(socket.SHUT_RDWR)
		except:
			pass

		s.close()
		self.command.newdb.closeSession()



class Airboss():
	"""this class is used by the daemon.runner.DaemonRunner
	to create a proper unix daemon"""

	def __init__(self):
		self.stdin_path = '/dev/null'
		self.stdout_path = logfile
		self.stderr_path = logfile
		self.pidfile_path =  '/var/run/airboss.pid'
		self.pidfile_timeout = 5
		self.server = None


	def run(self):
		"""run method of the daemon"""

		host = ""
		logger.info('airboss daemon starting')
		# we need this to reconnect to the DB
		AirbossTCPHandler.command.newdb.reconnect()
		# we need this to reconnect to the logger or it will try to send logs 
		# to the wrong FD number (very very stupid)
		#self.server = SocketServer.ThreadingTCPServer((host, port), AirbossTCPHandler)
		self.server = SocketServer.TCPServer((host, port), AirbossTCPHandler)
		self.server.allow_reuse_address = True
		self.server.serve_forever()
		logger.info('airboss daemon terminated abnormally')


	def stop(self):
		"""called when the daemon is stopped"""
		if self.server:
			self.server.shutdown()


RollName = "kvm"
