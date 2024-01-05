# This module provisions a local docker registry
# it is totally optional and its only purpose
# is to decrease push/pull time of docker images

# local cluster must be correctly configured
# see: https://k3d.io/v5.6.0/usage/registries/
import pulumi

import pulumi_docker as docker

config = pulumi.Config()
stack = pulumi.get_stack()

def create(depends_on=None):
	cluster_cfg = config.require_object('cluster')
	cluster_name = cluster_cfg['name']
	if stack != "local":
		return
	network_name = f'k3d-{cluster_name}'
	registry_image = docker.RemoteImage(
		'registry-image',
		keep_locally=True,
		name='registry:2'
	)
	registry_container = docker.Container(
		'registry-container',
		image=registry_image.image_id,
		name='local-registry',
		restart='always',
		must_run=False,
		ports=[{'internal': 5000, 'external': 5000}],
		networks_advanced=[{'name': network_name}],
		opts=pulumi.ResourceOptions(
			depends_on=depends_on,
			retain_on_delete=False,
		)
	)
	pulumi.export('registry', registry_container.name)
