# $Id: plugin_host_vm.py,v 1.3 2012/11/27 00:49:07 phil Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 6.1.1 (Sand Boa)
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
# $Log: plugin_host_vm.py,v $
# Revision 1.3  2012/11/27 00:49:07  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.2  2012/05/06 05:49:16  phil
# Copyright Storm for Mamba
#
# Revision 1.1  2012/03/17 02:52:29  clem
# I needed to commit all this code! First version of the rocks command for kvm.
# Soon all the other code
#
# Revision 1.7  2011/07/23 02:31:43  phil
# Viper Copyright
#
# Revision 1.6  2010/09/07 23:53:32  bruno
# star power for gb
#
# Revision 1.5  2009/05/01 19:07:33  mjk
# chimi con queso
#
# Revision 1.4  2008/12/16 00:45:05  bruno
# merge vm_profiles and pxeaction tables into bootaction table
#
# Revision 1.3  2008/10/27 20:18:28  bruno
# call the bootprofile dump commands when 'rocks dump' is called
#
# Revision 1.2  2008/10/18 00:56:23  mjk
# copyright 5.1
#
# Revision 1.1  2008/04/29 17:35:41  bruno
# put the vm dump plugin in the right directory
#
# Revision 1.1  2008/04/21 16:36:54  bruno
# added dump command for restore roll
#
#

import rocks.commands

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'vm'
		
	def requires(self):
		return [ 'interface' ]
		
	def run(self, args):
		self.owner.addText(self.owner.command('dump.host.vm', []))
		

