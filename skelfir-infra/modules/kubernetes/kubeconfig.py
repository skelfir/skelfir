import pulumi

# workaround for expiring DOKS cluster token
# see: https://github.com/pulumi/pulumi-digitalocean/issues/78#issuecomment-639669865
def create(cluster, template=None, user='admin'):
	if pulumi.get_stack() == "local":
		kube_config = cluster.kube_configs[0]
	else:
		mapping = {
			'ca_cert': cluster.kube_configs[0].cluster_ca_certificate,
			'cluster_endpoint': cluster.endpoint,
			'cluster_name': cluster.name,
			'api_token': pulumi.Config('digitalocean').require_secret('token'),
			'user': user,
		}
		kube_config = pulumi.Output.format(template, **mapping)
	# should be no need to export kube config
	#pulumi.export("kube_config", kube_config)
	return kube_config
