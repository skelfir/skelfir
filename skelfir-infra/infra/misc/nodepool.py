import pulumi
import pulumi_digitalocean as do


class KubernetesNodePool:
	def __new__(self, *args, **kwargs):
		disabled = kwargs.get('opts', {}).get('disabled', False)
		if disabled:
			node_pool = None
		else:
			node_pool = do.KubernetesNodePool(*args, **kwargs)
		return node_pool
