import yaml
import subprocess

from pulumi import Output
from pulumi.dynamic import Resource
from pulumi.dynamic import CreateResult
from pulumi.dynamic import ResourceProvider

from utils import Command


def run(command):
	p = subprocess.run(command.split(), check=True, capture_output=True)
	if p.returncode != 0:
		raise Exception()
	return p


def write_config(config):
	with open('/tmp/local-dev-cluster-config.yml', 'w') as f:
		yaml.dump(config, f)


def create_k3d_cluster(name):
	command = 'k3d cluster create {name} --config /tmp/local-dev-cluster-config.yml'
	command = command.format(name=name)
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
	return yaml.safe_load(p.stdout.decode())


class K3dProvider(ResourceProvider):
	def create(self, inputs):
		cluster_name = inputs['config']['name']
		write_config(inputs['config'])
		create_k3d_cluster(cluster_name)
		kubeconfig = get_kubeconfig(cluster_name)
		clusters = kubeconfig["clusters"]
		cluster_0 = clusters[0]
		return CreateResult(
			cluster_name,
			outs={
				'name': cluster_name,
				'kube_configs': [kubeconfig],
				"endpoint": kubeconfig["clusters"][0]["cluster"]["server"]
			}
		)

	def delete(self, id, inputs):
		delete_k3d_cluster(inputs['name'])


class K3dCluster(Resource):
	name: Output[str]
	kube_configs: Output[list[dict]]

	def __init__(self, name, config, opts=None):
		args = {
			"name": name,
			"config": config,
			"endpoint": None,
			"kube_configs": None,
		}
		super().__init__(K3dProvider(), name, args, opts)
