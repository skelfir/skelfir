import pulumi
import pulumi_digitalocean as do
from infra.providers.k3d import K3dCluster


# Impostor class
class KubernetesCluster:
	def __new__(self, *args, **kwargs):
		if pulumi.get_stack() == 'local':
			cluster = K3dCluster(*args, **kwargs)
		else:
			cluster = do.KubernetesCluster(*args, **kwargs)
		return cluster
