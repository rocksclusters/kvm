# $Id: __init__.py,v 1.3 2012/11/27 00:49:10 phil Exp $
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
# Revision 1.3  2012/11/27 00:49:10  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.2  2012/05/06 05:49:17  phil
# Copyright Storm for Mamba
#
# Revision 1.1  2012/03/17 02:52:31  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.2  2011/07/23 02:31:45  phil
# Viper Copyright
#
# Revision 1.1  2010/10/07 19:58:37  bruno
# power on and off virtual clusters
#
#

import rocks.commands
import os
import time
import M2Crypto

class command(rocks.commands.set.cluster.command):
	MustBeRoot = 0


class Command(command):
	"""
	Turn the power on or off for each client host in a virtual cluster.
	This command will *not* affect a virtual frontend.

	<arg type='string' name='host' repeat='0'>
	The host name of a virtual frontend.
	</arg>

	<param type='string' name='action'>
	The power setting. This must be one of 'on', 'off' or 'install'.
	The 'install' action will turn the power on and force the host to
	install.
	</param>

	<param type='string' name='key' optional='0'>
	A private key that will be used to authenticate the request. This
        should be a file name that contains the private key.
	</param>

	<param type='string' name='delay'>
	Sets the time (in seconds) to delay between each power command.
	Default is '1'.
	</param>
		
	<example cmd='set cluster power frontend-0-0-0 action=on'>
	Turn on the power for each client node that is associated with
	frontend-0-0-0.
	</example>
	"""

	def run(self, params, args):
		(action, key, d) = self.fillParams([
			('action', ),
			('key', ),
			('delay', '1')
			])

		try:
			delay = float(d)
		except:
			self.abort('"delay" must be a floating point number')
		
		hosts = self.getHostnames(args)
		if len(hosts) > 1:
			self.abort('must supply only one host')
		host = hosts[0]

		fe_hosts = self.getHostnames( [ 'frontend' ] )
		if host not in fe_hosts:
			self.abort('host name must be a frontend')

		if action not in [ 'on', 'off', 'install' ]:
			self.abort('invalid action. ' +
				'action must be "on", "off" or "install"')

		if not key:
			self.abort('must supply a key')

		if not os.path.exists(key):
			self.abort("can't access the private key '%s'" % key)

		rsakey = M2Crypto.RSA.load_key(key)

		macs = self.command('list.host.macs', [ host,
				'key=%s' % key, 'output-header=no' ])
		for mac in macs.split():
			try:
				h = self.db.getHostname(mac)

				#
				# 'rocks list host macs' returns the MAC
				# addresses of all the nodes in the cluster,
				# including the frontend. and we don't want to
				# execute the power command on the frontend.
				#
				if h in fe_hosts:
					continue
			except:
				pass	

			self.command('set.host.power', [ mac,
				'action=%s' % action, 'key=%s' % key ])

			if delay > 0:
				time.sleep(delay)



RollName = "kvm"
