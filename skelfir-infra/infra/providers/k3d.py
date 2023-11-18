import yaml
import subprocess

from pulumi import Output
#from pulumi import ResourceOptions
from pulumi.dynamic import Resource
from pulumi.dynamic import CreateResult
from pulumi.dynamic import ResourceProvider

cluster_config_file = '/tmp/local-cluster-config.yml'
default_cluster_config = {
	'agents': 1,
	'servers': 1,
	'kind': 'Simple',
	'name': 'local-dev-cluster',
	'apiVersion': 'k3d.io/v1alpha2'
}


def run(command):
	p = subprocess.run(command.split(), check=True, capture_output=True)
	if p.returncode != 0:
		raise Exception()
	return p


def write_config(config):
	with open(cluster_config_file, 'w') as f:
		yaml.dump(config, f)


def create_k3d_cluster(name):
	command = 'k3d cluster create {name} --config {cluster_config_file}'
	command = command.format(name=name, cluster_config_file=cluster_config_file)
	p = run(command)
	return p


def delete_k3d_cluster(name):
	command = 'k3d cluster delete {name}'
	command = command.format(name=name)
	p = run(command)
	return p


def get_kubeconfig(name):
	command = 'k3d kubeconfig get {name}'
	command = command.format(name=name)
	p = run(command)
	return p.stdout.decode()


class K3dProvider(ResourceProvider):
	def create(self, inputs):
		config = inputs.get('config', default_cluster_config)
		cluster_name = config['name']
		write_config(config)
		create_k3d_cluster(cluster_name)
		kubeconfig = get_kubeconfig(cluster_name)
		return CreateResult(
			cluster_name,
			outs={
				'name': cluster_name,
				'kubeconfig': kubeconfig
			}
		)

	def delete(self, id, inputs):
		delete_k3d_cluster(inputs['name'])


class K3dCluster(Resource):
	name: Output[str]
	kubeconfig: Output[str]

	def __init__(self, name, config=None, opts=None):
		args = {'config': config, 'name': None, 'kubeconfig': None}
		super().__init__(K3dProvider(), name, args, opts)
