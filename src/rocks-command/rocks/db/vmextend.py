#!/opt/rocks/bin/python
#

"""
This class add some functions used only by the kvm roll to the 
rocks.db.helper.DatabaseHelper class


If a KVM package needs this extra function should simply import this 
package which will make the method below available from the class 
rocks.db.helper.DatabaseHelper

"""

import rocks.db.helper
import sqlalchemy.orm
import sys
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt

from rocks.db.mappings.base import *

def getPhysTapDevicefromVnode(self, node):
	"""Given a virtual node it returns a list of dictionaries with
	{'device': phys_device_name, "vlanID": phys_device_vlan,
	"mac": virtual_mac_address} which are needed for this virtual
	host. This list includes only tap device, it does not include
	bridged interfaces"""

	s = self.getSession()
	vlanids = {}
	for net in node.networks:
		# we need to skip interface that are disable
		if not net.disable_kvm:
			vlanids[net.vlanID] = net.mac

	if not vlanids:
		return []

	# on the physical node find the subnet of the device called
	# vlan% with the vlanid == vlanids (networkvlan table)
	# now find the physical device name corresponding to the subnets
	# found in the previous query (Network table)
	networkvlan = sqlalchemy.orm.aliased(Network)
	devices = s.query(Network.device, networkvlan.vlanID).filter(
			Network.node == node.vm_defs.physNode,
			networkvlan.node == node.vm_defs.physNode,
			Network.subnet_ID == networkvlan.subnet_ID,
			sqlalchemy.not_(Network.device.like('vlan%')),
			networkvlan.device.like('vlan%'),
			networkvlan.vlanID.in_(vlanids.keys())).all()

	# this is a bit perverse but now I want to re-add the corresponding
	# mac address of the virtual interface which needs this physical
	# device and vlanID so I know which vrtual mac needs to be attached
	# to this tap device
	retval = []
	for d in devices:
		a = {}
		a['mac'] = vlanids[d.vlanID]
		a.update(d.__dict__)
		retval.append(a)

	return retval


def getPhysBridgedDevicefromVnode(self, node):
	"""Given a virtual node it returns a list of dictionaries with
	{'device': phys_device_name, "vlanID": phys_device_vlan,
	"mac": virtual_mac_address} which are needed for this virtual
	host. This list includes only bridged devices, it does not include
	tap interfaces"""

	s = self.getSession()

	# on the physical node find the subnet of the device called
	# vlan% with the vlanid == vlanids (networkvlan table)
	# now find the physical device name corresponding to the subnets
	# found in the previous query (Network table)
	networkvirtual = sqlalchemy.orm.aliased(Network)
	devices = s.query(Network.device, Network.vlanID, networkvirtual.mac).filter(
			Network.node == node.vm_defs.physNode,
			networkvirtual.node == node,
			Network.subnet_ID == networkvirtual.subnet_ID,
			not_(networkvirtual.disable_kvm),
			# special handling for the case of vlan==0 that for the
			# physical host is vlan==None
			or_(Network.vlanID == networkvirtual.vlanID,
			  and_(Network.vlanID == None, networkvirtual.vlanID == 0),
			  and_(Network.vlanID == None, networkvirtual.vlanID == None),
                        ),
			sqlalchemy.not_(Network.device.like('vlan%')),
			).all()

	# this is a bit perverse but now I want to re-add the corresponding
	# mac address of the virtual interface which needs this physical
	# device and vlanID
	retval = []
	for d in devices:
		a = dict((key, d.__dict__[key]) for key in d.keys())
		retval.append(a)

	return retval

def getVClusters(self):
	""" """

	ret = VClusters()

	query = text("select cluster_name, vlanid, node_name from clusters")

	for (fe, id, node) in self.conn.execute(query):
		if fe not in ret.nodes:
			ret.nodes[fe] = [node]
		else:
			ret.nodes[fe].append(node)
		ret.vlans[fe] = id

	return ret




# Adding this methods to the DatabaseHelper class so they will be available
# to all the python package that will load this package
rocks.db.helper.DatabaseHelper.getPhysBridgedDevicefromVnode = getPhysBridgedDevicefromVnode
rocks.db.helper.DatabaseHelper.getPhysTapDevicefromVnode = getPhysTapDevicefromVnode
rocks.db.helper.DatabaseHelper.getVClusters = getVClusters


class VClusters:
	"""Container class use by"""

	def __init__(self):
		self.nodes={}
		self.vlans={}

	def getFrontends(self):
		"""return a list of virtual cluster frontends"""
		return self.nodes.keys()

	def getNodes(self, fename):
		"""return a list of nodes belonging to this cluster"""
		return self.nodes[fename]

	def getVlan(self, fename):
		"""return the vlanid used by this cluster"""
		return self.vlans[fename]




def getStatus(node):
	"""given a node (of type Node) it returns its status as a string"""

	if not (node.vm_defs and node.vm_defs.physNode):
		return 'nostate-error'

	physhost = node.vm_defs.physNode.name

	try:
		import rocks.vmconstant
		hipervisor = libvirt.open(rocks.vmconstant.connectionURL % physhost)
	except libvirt.libvirtError:
		#import traceback
		#traceback.print_exc()
		return 'nostate-error'

	found = 0
	for id in hipervisor.listDomainsID():
		if id == 0:
			#
			# skip dom0
			#
			continue

		domU = hipervisor.lookupByID(id)
		if domU.name() == node.name:
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
