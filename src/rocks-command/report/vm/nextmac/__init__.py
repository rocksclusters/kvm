# $Id: __init__.py,v 1.3 2012/11/27 00:49:09 phil Exp $
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
# Revision 1.3  2012/11/27 00:49:09  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.2  2012/05/06 05:49:17  phil
# Copyright Storm for Mamba
#
# Revision 1.1  2012/03/17 02:52:30  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.2  2011/07/23 02:31:45  phil
# Viper Copyright
#
# Revision 1.1  2010/09/10 19:51:53  bruno
# print out the next free MAC address that can be used for a VM
#
#

import rocks.commands

class Command(rocks.commands.report.command):
	"""
	Outputs the next free MAC address that can be used for a VM.

        <example cmd='report vm nextmac'>
        </example>

	"""

	def makeOctets(self, str):
		#
		# this code is lifted from 'add host vm'
		#
		octets = []
		for a in str.split(':'):
			octets.append(int(a, 16))

		return octets


	def getNextMac(self):
		#
		# this code is lifted from 'add host vm'
		#
		# find the next free VM MAC address in the database
		#

		#
		# get the VM MAC base addr and its mask
		#
		rows = self.db.execute("""select value from global_attributes
			where attr = 'vm_mac_base_addr' """)

		if rows > 0:
			vm_mac_base_addr, = self.db.fetchone()
			base_addr = self.makeOctets(vm_mac_base_addr)
		else:
			self.abort('no VM MAC base address is defined')

		rows = self.db.execute("""select value from global_attributes
			where attr = 'vm_mac_base_addr_mask' """)

		if rows > 0:
			vm_mac_base_addr_mask, = self.db.fetchone()
			mask = self.makeOctets(vm_mac_base_addr_mask)
		else:
			self.abort('no VM MAC base address mask is defined')

		rows = self.db.execute("""select mac from networks where
			mac is not NULL""")

		max = 0
		if rows > 0:
			for m, in self.db.fetchall():
				mac = self.makeOctets(m)

				i = 0
				match = 1
				for a in base_addr:
					if (base_addr[i] & mask[i]) != \
							(mac[i] & mask[i]):
						match = 0
						break
					i += 1

				if match == 0:
					continue

				i = 0
				x = 0
				for a in range(len(mac) - 1, -1, -1):
					y = (mac[a] * (2 ** (8 * i)))
					x += y
					i += 1
					
				if x > max:
					max = x

		newmac = []

		if max == 0:
			#
			# this is the first assignment, use the base_addr as
			# the mac address
			#
			for a in base_addr:
				newmac.append('%02x' % a)
		else:
			max += 1

			#
			# now convert the integer into a mac address
			#
			i = 0
			bitmask = 0xff
			for a in range(len(mac) - 1, -1, -1):
				x = (max & bitmask) >> (8 * i)
				if a == 0:
					#
					# special case for the first MAC octet.
					#
					# the first bit should be zero (the
					# multicast bit).
					#
					if (x & 0x1) == 1:
						x += 1

					# 
					# the second bit should be one (the
					# locally administered bit).
					#
					if (x & 0x2) == 0:
						x |= 0x2
					
				newmac.append('%02x' % x)
				bitmask = bitmask << 8 
				i += 1

			newmac.reverse()

		return ':'.join(newmac)


	def run(self, params, args):
		self.beginOutput()
		self.addOutput('', self.getNextMac())
		self.endOutput(padChar='')
	

