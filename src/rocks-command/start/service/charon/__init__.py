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
#

import os
import sys
import subprocess
import xml.sax.handler
import time
import logging
import threading
import signal

import rocks.vm
import rocks.vmconstant
import rocks.commands
import rocks.sql
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt



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







	def run(self, params, args):
		foreground, = self.fillParams([ ('foreground', 'n') ])

		if not self.str2bool(foreground):
			self.daemonize()

		# create logger
		self.logger = logging.getLogger('charon')
		self.logger.setLevel(logging.DEBUG)
		# create file handler which logs even debug messages
		fh = logging.FileHandler('/var/log/charon.log')
		fh.setLevel(logging.DEBUG)
		self.logger.addHandler(fh)

		# try to reconnect to the DB disgusting code!!
		time.sleep(0.2)
		tempdb = rocks.sql.Application()
		tempdb.connect()
		self.db.database = tempdb.link
		self.db.link     = tempdb.link.cursor()
		
		self.logger.critical('charon started at %s\n' % time.asctime())

		# we need to check the status of all the VMs
		# TODO this needs to be triggered for every new physical node reinstallation
		vircon_list = {}
		signal.signal(signal.SIGUSR1, signalUsr1Handler)

		self.db.execute("""select n.name from nodes as n
				where n.id not in
				(select vmn.node from vm_nodes as vmn)""")

		for host, in self.db.fetchall():
			# we save same queries to the DB temporary storing 
			# here all attributes
			attrs = self.db.getHostAttrs(host)
			if attrs.get('managed') == 'true' and \
				attrs.get('kvm') == 'true':
				vircon_list[rocks.vmconstant.connectionURL % host] = None
			# add frontend which is unmanaged :-o
			if attrs.get('Kickstart_PrivateHostname') == host and \
				attrs.get('kvm') == 'true':
				vircon_list[rocks.vmconstant.connectionURL % host] = None

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

		self.logger.debug("Entering passive wait for event")	
		while True:
			# first let's check if some container went down 
			# Unfortunately in RHEL 6.X libvirt-python is missing the 
			# registerCloseCallback and unregisterCloseCallback
			# so we need to pool the connections
			#
			for url in vircon_list:
				vc = vircon_list[url]
				if not vc:
					# this is a dead domain let's see if it resurected
					vc = self.connectDomain(url)
					if vc:
						# resurrected
						self.logger.debug("Hosts %s is monitored" % url)
						vircon_list[url] = vc
					else:
						# the deaddomain is still dead
						pass

				elif not vc.isAlive():
					# once was alive but now is dead
					self.logger.debug("Host %s is not monitored" % url)
					vircon_list[url] = None
					try:
						vc.close()
					except:
						pass
			#TODO sleep more
			time.sleep(1)




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
			if "unable to connect" in str(e):
				return None
			else:
				raise e
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
	if event == 6:
		# this is a shutdown we need to call the hook function if defined
		logger.critical("Host %s was stopped" % dom.name())
		#TODO do something

	logger.debug("myDomainEventCallback2 EVENT: Domain %s(%s) %s %s" % (dom.name(), dom.ID(),
	                                                             eventToString(event),
	                                                             detailToString(event, detail)))


def signalUsr1Handler(signum, frame):
	logger = logging.getLogger('charon')
	logger.debug('Signal handler called with signal' + str(signum))
