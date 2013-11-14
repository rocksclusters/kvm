#!/usr/bin/env python

import os
import sys
import M2Crypto
import socket
import subprocess
import shlex

try:
	import hashlib
	has_hashlib = 1
except:
	import sha
	has_hashlib = 0

try:
	import ssl
	has_ssl = 1
except:
	has_ssl = 0

import select
import re

class VMControl:

	def __init__(self, controller, key, vncviewer='vncviewer', vncflags=''):
		self.controller = controller
		self.key = key
		self.port = 8677
		self.vncviewer = vncviewer
		self.vncflags = vncflags
		return


	def closeconnection(self, sock, s):
		try:
			s.shutdown(socket.SHUT_RDWR)
		except:
			pass

		try:
			sock.shutdown(socket.SHUT_RDWR)
		except:
			pass

		try:
			s.close()
		except:
			pass

		try:
			sock.close()
		except:
			pass


	def launchconsole(self, sock, s):
		reason = ''

		#
		# setup an endpoint that VNC will use to talk to us
		#
		vnc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#
		# find a free port
		#
		success = 0
		for i in range(1, 100):
			vncport = 5900 + i
			try:
				vnc.bind(('localhost', vncport))
				success = 1
				break
			except:
				pass

		if not success:
			return 'failed'

		vnc.listen(1)

		cmd = '%s HOST localhost PORT %d %s' % \
			(self.vncviewer, vncport, self.vncflags)
		subprocess.Popen(shlex.split(cmd))

		#
		# parent
		#
		conn, addr = vnc.accept()

		done = 0
		while not done:
			#
			# read from the VM controller
			#
			(i, o, e) = select.select([sock.fileno()], [], [],
				0.00001)
			if sock.fileno() in i:
				try:
					(status, output) = self.recvresponse(s)

					if len(output) == 0:
						# 
						# EOF. the VM controller
						# shutdown the connection.
						# let's see if the remote
						# machine rebooted
						# 
						reason = 'retry'
						done = 1
						continue
						
					bytes = conn.send(output)
					while bytes != len(output):
						bytes += conn.send(
							output[bytes:])
				except:
					done = 1
					continue

			#
			# read from the VNC client
			#
			(i, o, e) = select.select([conn.fileno()], [], [],
				0.00001)
			if conn.fileno() in i:
				try:
					input = conn.recv(1024)

					bytes = s.write(input)
					while bytes != len(input):
						bytes += s.write(
							input[bytes:])
				except:
					done = 1
					continue

		try:
			conn.shutdown(socket.SHUT_RDWR)
		except:
			pass
		try:
			conn.close()
		except:
			pass
		try:
			vnc.shutdown(socket.SHUT_RDWR)
		except:
			pass
		try:
			vnc.close()
		except:
			pass

		return reason


	def console(self, op, dst_mac):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if has_ssl:
			s = ssl.wrap_socket(sock)
			s.connect((self.controller, self.port))
		else:
			sock.connect((self.controller, self.port))
			s = socket.ssl(sock)

		#
		# start the connection by sending a command to the VM
		# controller
		#
		self.sendcommand(s, op, dst_mac)

		#
		# read the status code from the VM controller
		#
		(status, reason) = self.recvresponse(s)

		if status == 0:
			reason = self.launchconsole(sock, s)

		self.closeconnection(sock, s)

		return (status, reason)


	def power(self, op, dst_mac):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if has_ssl:
			s = ssl.wrap_socket(sock)
			s.connect((self.controller, self.port))
		else:
			sock.connect((self.controller, self.port))
			s = socket.ssl(sock)

		self.sendcommand(s, op, dst_mac)
		(status, reason) = self.recvresponse(s)

		self.closeconnection(sock, s)

		return (status, reason)
		

	def listmacs(self, op, dst_mac):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if has_ssl:
			s = ssl.wrap_socket(sock)
			s.connect((self.controller, self.port))
		else:
			sock.connect((self.controller, self.port))
			s = socket.ssl(sock)

		self.sendcommand(s, op, dst_mac)
		(status, macs) = self.recvresponse(s)

		self.closeconnection(sock, s)

		return (status, macs)


	def sendcommand(self, s, op, dst_mac):
		msg = '%s\n' % op

		#
		# destination MAC
		#
		msg += '%s\n' % dst_mac

		#
		# send the size of the clear text and send the clear text
		# message
		#
		msgsize = '%08d\n' % len(msg)
		bytes = 0
		while bytes != len(msgsize):
			bytes = s.write(msgsize[bytes:])

		bytes = 0
		while bytes != len(msg):
			bytes = s.write(msg[bytes:])

		#
		# now add the signed digest
		#
		if has_hashlib:
			digest = hashlib.sha1(msg).digest()
		else:
			digest = sha.sha(msg).digest()
		signature = self.key.sign(digest, 'ripemd160')

		#
		# send the length of the signature
		#
		msgsize = '%08d\n' % len(signature)
		bytes = 0
		while bytes != len(msgsize):
			bytes += s.write(msgsize[bytes:])

		bytes = 0
		while bytes != len(signature):
			bytes += s.write(signature)


	def recvresponse(self, s):
		#
		# pick up response
		#
		buf = ''
		while len(buf) != 9:
			buf += s.read(1)

		try:
			msg_len = int(buf)
		except:
			msg_len = 0

		buf = ''
		while len(buf) != msg_len:
			buf += s.read(msg_len - len(buf))

		status = 0

		#
		# check if the message has a status code in it
		#
		a = re.match('^status:[0-9-]+\n', buf)
		if a:
			s = a.group(0).split(':')
			if len(s) > 1:
				try:
					status = int(s[1])
					response = buf[len(a.group(0)):]
				except:
					response = buf
		else:
			response = buf

		return (status, response)


	def cmd(self, op, host):
		#
		# the list of valid commands:
		#
		#	power off
		#	power on
		#	power on + install
		#	list macs
		#	list macs + status
		#	console
		#

		dst_mac = host

		retval = ''

		if op in [ 'power off', 'power on', 'power on + install' ]:
			(status, msg) = self.power(op, dst_mac)
		elif op == 'list macs' or op == 'list macs + status':
			(status, msg) = self.listmacs(op, dst_mac)
		elif op == 'console':
			msg = 'retry'
			while msg == 'retry':
				(status, msg) = self.console(op, dst_mac)
				if msg == 'retry':
					print ''
					print 'Attempting to reestablish ' + \
						'the console connection. ' + \
						'Standby...'

		return (status, msg)

class createKeys:
	def run(self, params):
		if 'key' not in params.keys():
			print 'must supply a filename for the private key'
			sys.exit(-1)
		key = params['key']

		if os.path.exists(key):
			print "the key file '%s' already exists" % key
			sys.exit(-1)

		if 'passphrase' in params.keys():
			if params['passphrase'] in [ 'y', 'yes', '1' ]:
				passphrase = 1
			else:
				passphrase = 0
		else:
			passphrase = 1

		#
		# generate the private key
		#
		cmd = 'openssl genrsa '
		if passphrase:
			cmd += '-des3 '
		cmd += '-out %s 1024' % key
		status = os.system(cmd)
		if status == 0:
			os.chmod(key, 0400)

			#
			# output the public key
			#
			os.system('openssl rsa -in %s -pubout' % key)
		else:
			os.remove(key)


class setHostPower:
	def run(self, params):
		if 'key' not in params.keys():
			print 'must supply a path name to a private key'
			sys.exit(-1)
		key = params['key']

		if not os.path.exists(key):
			print 'private key "%s" does not exist' % key
			sys.exit(-1)

		if 'action' not in params.keys():
			print 'must supply an "action" parameter'
			sys.exit(-1)
		action = params['action']
		
		if action not in [ 'on', 'off', 'install' ]:
			self.abort('invalid action. ' +
				'action must be "on", "off" or "install"')

		if 'host' not in params.keys():
			print 'the "host" parameter is not set'
			sys.exit(-1)
		host = params['host']

		if 'vm-controller' not in params.keys():
			vm_controller = 'localhost'
		else:
			vm_controller = params['vm-controller']

		rsakey = M2Crypto.RSA.load_key(key)

		vm = VMControl(vm_controller, rsakey)

		if action == 'on':
			op = 'power on'
		elif action == 'off':
			op = 'power off'
		elif action == 'install':
			op = 'power on + install'

		(status, reason) = vm.cmd(op, host)

		if status != 0:
			print 'command failed\n%s' % reason
			sys.exit(-1)


class openHostConsole:
	def run(self, params):
		if 'key' not in params.keys():
			print 'must supply a path name to a private key'
			sys.exit(-1)
		key = params['key']

		if not os.path.exists(key):
			print 'private key "%s" does not exist' % key
			sys.exit(-1)

		if 'vm-controller' not in params.keys():
			vm_controller = 'localhost'
		else:
			vm_controller = params['vm-controller']

		if 'vncviewer' not in params.keys():
			vncviewer = 'java -jar TightVncViewer.jar'
		else:
			vncviewer = params['vncviewer']

		if 'vncflags' not in params.keys():
			vncflags = 'Encoding Hextile'
		else:
			vncflags = params['vncflags']

		if 'host' not in params.keys():
			print 'the "host" parameter is not set'
			sys.exit(-1)
		host = params['host']

		rsakey = M2Crypto.RSA.load_key(key)

		vm = VMControl(vm_controller, rsakey, vncviewer, vncflags)

		(status, reason) = vm.cmd('console', host)

		if status != 0:
			print 'command failed\n%s' % reason
			sys.exit(-1)

class listHostMacs:
	def run(self, params):
		if 'key' not in params.keys():
			print 'must supply a path name to a private key'
			sys.exit(-1)
		key = params['key']

		if not os.path.exists(key):
			print 'private key "%s" does not exist' % key
			sys.exit(-1)

		if 'vm-controller' not in params.keys():
			vm_controller = 'localhost'
		else:
			vm_controller = params['vm-controller']

		if 'host' not in params.keys():
			print 'the "host" parameter is not set'
			sys.exit(-1)
		host = params['host']

		if 'status' in params.keys():
			if params['status'] in [ 'y', 'yes', '1' ]:
				state = 1
			else:
				state = 0
		else:
			state = 1

		rsakey = M2Crypto.RSA.load_key(key)

		vm = VMControl(vm_controller, rsakey)

		if state:
			(status, macs) = vm.cmd('list macs + status', host)
		else:
			(status, macs) = vm.cmd('list macs', host)
		if status != 0:
			print 'command failed: %s' % macs
			sys.exit(-1)
			

		for mac in macs.split('\n'):
			if len(mac) > 0:
				print mac


#
# get the parameters
#
params = {}
i = 0
for i in range(len(sys.argv) - 1, 0, -1):
	if '=' in sys.argv[i]:
		p = sys.argv[i].split('=', 1)
		params[p[0]] = p[1]
	else:
		break

command = sys.argv[1:i+1]

if command == [ 'create', 'keys' ]:
	cmd = createKeys()
elif command == [ 'set', 'host', 'power' ]:
	cmd = setHostPower()
elif command == [ 'open', 'host', 'console' ]:
	cmd = openHostConsole()
elif command == [ 'list', 'host', 'macs' ]:
	cmd = listHostMacs()
else:
	print 'command not recognized'
	print
	print 'Supported commands are:\n'
	print '\t%s create keys ' % (sys.argv[0]) + \
		'key=path-to-private-key-file\n\t\t<passphrase=[yes|no]>'
	print '\n\t%s list host macs ' % (sys.argv[0]) + \
		'host=mac-address-of-virtual-frontend\n' + \
		'\t\tkey=path-to-private-key-file <status=[yes|no]>'
	print '\n\t%s open host console ' % (sys.argv[0]) + \
		'host=mac-address-of-virtual-machine\n' + \
		'\t\tkey=path-to-private-key-file'
	print '\n\t%s set host power ' % (sys.argv[0]) + \
		'host=mac-address-of-virtual-machine\n' + \
		'\t\tkey=path-to-private-key-file action=[on|off|install]'
	sys.exit(-1)

cmd.run(params)

