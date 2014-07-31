

--
-- create a view with fe_name, vlanid, nodes of the cluster
-- for every cluster to simplify querying
--
DROP VIEW IF EXISTS clusters;
CREATE VIEW clusters AS
SELECT n.name as cluster_name, net.vlanid, n2.name as node_name
FROM networks net, nodes n, vm_nodes vmn, memberships mem, subnets sub,
     nodes n2, networks net2, vm_nodes vmn2
WHERE n.id = net.node AND n.id = vmn.node
	AND mem.name = 'Frontend' AND mem.id = n.membership
	AND net.vlanid > 0 AND sub.name = 'private'
	AND sub.id = net.subnet
	AND n2.id = net2.node
	AND net2.vlanid = net.vlanid
	AND n2.id = vmn2.node;


