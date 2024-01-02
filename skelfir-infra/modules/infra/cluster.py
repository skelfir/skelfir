import pulumi
import pulumi_digitalocean as do

from providers.k3d import K3dCluster


stack = pulumi.get_stack()

def create(config):
	if stack == "local":
		cluster = None
		cluster = K3dCluster('k3d-cluster', config)
	else:
		#cluster_cfg = config.require_object('cluster')
		#base_node_pool = do.KubernetesNodePool(
		#	auto_scale=True,
		#	min_nodes=1,
		#	max_nodes=cluster_cfg['base_node_pool']['node_count'],
		#	name=cluster_cfg['base_node_pool']['name'],
		#	size=cluster_cfg['base_node_pool']['size'],
		#	node_count=cluster_cfg['base_node_pool']['node_count']
		#)

		cluster = do.KubernetesCluster(
			config['name'],
			name=config['name'],
			region=config['region'],
			version=config['version'],
			node_pool={
				'auto_scale': True,
				'max_nodes': 1,
				'min_nodes': 1,
				'name': config['base_node_pool']['name'],
				'size': config['base_node_pool']['size'],
				'node_count': config['base_node_pool']['node_count']
			},
			opts=pulumi.ResourceOptions(
				depends_on=[],
			),
		)
	return cluster, {"cluster_id": cluster.id}
