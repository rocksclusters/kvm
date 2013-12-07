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




	def getState(self, physhost, host):
		try:
			import rocks.vmconstant
			hipervisor = libvirt.open( rocks.vmconstant.connectionURL % physhost)
		except:
			return 'nostate'
	
		found = 0
		for id in hipervisor.listDomainsID():
			if id == 0:
				#
				# skip dom0
				#
				continue
			
			domU = hipervisor.lookupByID(id)
			if domU.name() == host:
				found = 1
				break

		state = 'nostate'

		if found:
			status = domU.info()[0]	

			if status == libvirt.VIR_DOMAIN_NOSTATE:
				state = 'nostate'
			elif status == libvirt.VIR_DOMAIN_RUNNING or \
					status == libvirt.VIR_DOMAIN_BLOCKED:
				state = 'active'
			elif status == libvirt.VIR_DOMAIN_PAUSED:
				state = 'paused'
			elif status == libvirt.VIR_DOMAIN_SHUTDOWN:
				state = 'shutdown'
			elif status == libvirt.VIR_DOMAIN_SHUTOFF:
				state = 'shutoff'
			elif status == libvirt.VIR_DOMAIN_CRASHED:
				state = 'crashed'

		return state




	def dorequest(self, conn):
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

		self.trace_vm_container()




	def trace_vm_container(self):
		# we need to check the status of all the VMs
		# TODO this needs to be triggered for every new physical node reinstallation
		url_deaddomains = set()
		vircon_list = []

		self.db.execute("""select n.name from nodes as n
				where n.id not in
				(select vmn.node from vm_nodes as vmn)""")

		for host, in self.db.fetchall():
			# we save same queries to the DB temporary storing 
			# here all attributes
			attrs = self.db.getHostAttrs(host)
			if attrs.get('managed') == 'true' and \
				attrs.get('kvm') == 'true':
				url_deaddomains.add(rocks.vmconstant.connectionURL % host)
			# add frontend which is unmanaged :-o
			if attrs.get('Kickstart_PrivateHostname') == host and \
				attrs.get('kvm') == 'true':
				url_deaddomains.add(rocks.vmconstant.connectionURL % host)

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
			# to eliminate element while looping we have to go backward
			for i in xrange(len(vircon_list) - 1, -1, -1):
				vc = vircon_list[i]
				if not vc.isAlive():
					# 
					uri = vc.getURI()
					self.logger.debug("Host %s is not monitored" % uri)
					url_deaddomains.add(uri)
					try:
						vc.close()
					except:
						pass
					del vircon_list[i]
			# let's see if any url_deaddomains is back alive
			for i in set(url_deaddomains):
				vc = self.connectDomain(i)
				if vc:
					# resurrected
					self.logger.debug("Hosts %s is monitored" % i)
					vircon_list.append(vc)
					url_deaddomains.remove(i)
				else:
					# the deaddomain is still dead
					pass
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

