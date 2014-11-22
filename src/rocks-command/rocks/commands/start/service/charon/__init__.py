#!/opt/rocks/bin/python
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
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
#

import os
import sys
import subprocess
import xml.sax.handler
import time
import logging
import threading
import signal
import subprocess
import shlex
import sqlalchemy


import rocks.vm
import rocks.vmconstant
import rocks.commands
import rocks.sql
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt


pidfile = '/var/run/charon/charon.pid'
reload_vmcontainers = False

class Command(rocks.commands.start.service.command):
	"""
	Starts the VM Monitoring service. This service is in charge to update 
	the status of all the VM into the database.
	When a machine changes state charon will call the respective call back.


	<param type='boolean' name='foreground'>
	If set to to 'yes', this service will stay in the foreground. Default
	is 'no'.
	</param>
	"""

	def Abort(self, msg):
		""" this is to avoid being terminated because of a self.abort while 
		calling a self.command()"""
		self.logger.critical('abort: msg: ', msg)


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
		# redirect standard file descriptors
		#
		sys.stdout.flush()
		sys.stderr.flush()
		si = file('/dev/null', 'r')
		so = file('/var/log/charon.log', 'a+')
		se = so
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())

	def connectDB(self):
		"""establish a DB connection"""
		try:
			self.newdb.closeSession()
		except Exception as e:
			self.logger.critical("Error closing DB session: " + str(e))
		self.newdb.reconnect()


	def run(self, params, args):
		# this holds the list of vm_containers that we are currently
		# monitoring
		self.vircon_list = {}

		foreground, = self.fillParams([ ('foreground', 'n') ])
		if not self.str2bool(foreground):
			self.newdb.closeSession()
			self.daemonize()

		# create logger
		self.logger = logging.getLogger('charon')
		self.logger.setLevel(logging.DEBUG)
		fh = logging.FileHandler('/var/log/charon.log')

		formatter = logging.Formatter(
			"%(asctime)s - %(levelname)s - %(message)s")
		fh.setFormatter(formatter)
		fh.setLevel(logging.DEBUG)
		self.logger.addHandler(fh)

		# try to reconnect to the DB disgusting code!!
		time.sleep(0.2)
		self.connectDB()
		
		self.logger.critical('charon started at %s\n' % time.asctime())

		# we need to check the status of all the VMs
		# TODO this needs to be triggered for every new physical node reinstallation
		signal.signal(signal.SIGUSR1, signalUsr1Handler)

		if not os.path.exists(os.path.dirname(pidfile)):
			os.makedirs(os.path.dirname(pidfile))
		fd = open(pidfile,'w')
		fd.write(str(os.getpid()))
		fd.close()

		def virEventLoopNativeRun():
			while True:
				libvirt.virEventRunDefaultImpl()
		# Run a background thread with the event loop
		libvirt.registerErrorHandler(handler, 'context')
		libvirt.virEventRegisterDefaultImpl()

		eventLoopThread = threading.Thread(target=virEventLoopNativeRun, 
					name="libvirtEventLoop")
		eventLoopThread.setDaemon(True)
		eventLoopThread.start()

		# populate the vircon_list
		self.load_vmcontainers()

		# enter the main monitoring loop
		self.logger.debug("Charon setup finished. Entering monitoring loop")
		while True:

			# check if we have to update the vircon_list (new nodes installed
			# or removed
			global reload_vmcontainers
			if reload_vmcontainers == True:
				reload_vmcontainers = False
				self.load_vmcontainers()

			#
			# check if some libvirtd on vm_containers went down
			# Unfortunately in RHEL 6.X libvirt-python is missing the
			# registerCloseCallback and unregisterCloseCallback
			# so we need to pool the connections
			#
			for url in self.vircon_list:
				vc = self.vircon_list[url]
				if not vc:
					# this is a dead domain let's see if it resurected
					vc = self.connectDomain(url)
					if vc:
						# resurrected
						self.logger.debug("Hosts %s is monitored" % url)
						self.vircon_list[url] = vc
					else:
						# the deaddomain is still dead
						pass

				elif not vc.isAlive():
					# once was alive but now is dead
					self.logger.debug("Host %s is not monitored" % url)
					self.vircon_list[url] = None
					try:
						vc.close()
					except:
						pass
			#TODO sleep more
			time.sleep(1)



	def load_vmcontainers(self):
		"""sincronize the vircon_list with the rocks database"""

		self.logger.debug("Reloading nodes from database")
		physical_nodes_sql = """select n.name from nodes as n
				where n.id not in
				(select vmn.node from vm_nodes as vmn)"""
		#
		# DB goes in timeout after a while if inactive so we must reconnect
		# in that case
		try:
			self.newdb.execute(physical_nodes_sql)
		except sqlalchemy.exc.OperationalError:
			self.connectDB()
			self.newdb.execute(physical_nodes_sql)

		vm_containers = set()
		for host, in self.newdb.fetchall():
			# storing here all the attributes we avoid repeating DB queries
			attrs = self.newdb.getHostAttrs(host)
			if attrs.get('managed') == 'true' and \
				attrs.get('kvm') == 'true':
				vm_containers.add(rocks.vmconstant.connectionURL % host)
			# add frontend which is unmanaged :-o
			if attrs.get('Kickstart_PrivateHostname') == host and \
				attrs.get('kvm') == 'true':
				vm_containers.add(rocks.vmconstant.connectionURL % host)

		# these need to be added
		tobe_added = vm_containers - set(self.vircon_list.keys())
		# and these to be removed
		tobe_removed = set(self.vircon_list.keys()) - vm_containers
		for url in tobe_added:
			self.logger.debug("Adding vm-container %s" % url)
			self.vircon_list[url] = None
		for url in tobe_removed:
			self.logger.debug("Removing vm-container %s" % url)
			if self.vircon_list[url]:
				try:
					self.vircon_list[url].close()
				except:
					pass
				del self.vircon_list[url]

		# we need to free up the session which is used by the 
		# getHostAttrs(host)
		self.newdb.closeSession()



	def connectDomain(self, url):
		"""attempt to connect to a libvirtd daemon.

		On success returns a virConnection on failure None"""
		try:
			vc = libvirt.openReadOnly(url)
			vc.domainEventRegisterAny(None,
				libvirt.VIR_DOMAIN_EVENT_ID_LIFECYCLE,
				lifeCycleCallBack, None)
			vc.setKeepAlive(5, 3)
		except libvirt.libvirtError, e:
			if not 'unable to connect to server' in str(e):
				# log something
				self.logger.debug("Error connecting to %s: %s" %
					(url, str(e)))
			return None
		return vc




# this function is used to suppress libvirt error message on the std output
def handler(ctxt, err):
	global errno
	errno = err


def eventToString(event):
	eventStrings = ("Defined",
			"Undefined",
			"Started",
			"Suspended",
			"Resumed",
			"Stopped",
			"Shutdown",
			"PMSuspended",
			"Crashed" )
	return eventStrings[event]

def detailToString(event, detail):
	eventStrings = (
		( "Added", "Updated" ),
		( "Removed", ),
		( "Booted", "Migrated", "Restored", "Snapshot", "Wakeup" ),
		( "Paused", "Migrated", "IOError", "Watchdog", "Restored", "Snapshot", "API error" ),
		( "Unpaused", "Migrated", "Snapshot" ),
		( "Shutdown", "Destroyed", "Crashed", "Migrated", "Saved", "Failed", "Snapshot"),
		( "Finished", ),
		( "Memory", "Disk" ),
		( "Panicked", )
		)
	return eventStrings[event][detail]


def lifeCycleCallBack(conn, dom, event, detail, opaque):
	logger = logging.getLogger('charon')
	#logger.debug("myDomainEventCallback2 EVENT: Domain %s(%s) %s %s" % (dom.name(), dom.ID(),
	#							eventToString(event),
	#							detailToString(event, detail)))
 
	if event == 6:
		# this is a shutdown we need to call the hook function if defined
		logger.critical("Host %s was stopped" % dom.name())
		cmd = '/opt/rocks/bin/rocks stop host vm ' + dom.name() 
		cmd += ' terminate=true'

		p = subprocess.Popen(shlex.split(cmd),
			stdin = subprocess.PIPE,
			stdout = subprocess.PIPE,
			stderr = subprocess.STDOUT)
		p.wait()

		response = '\n'.join(p.stdout.readlines())

		if len(response) > 0:
			logger.critical(response)



def signalUsr1Handler(signum, frame):
	"""signal handler for sigusr1 which will trigger a self.load_vmcontainers"""
	global reload_vmcontainers
	reload_vmcontainers = True

RollName = "kvm"
