from pathlib import Path

import yaml
import pulumi

from modules import infra
from modules import kubernetes

config = pulumi.Config()
exports = {}


def load_ext_config(file_name, raw=False):
	configs_path = Path.cwd().joinpath('configs')
	file_path = configs_path.joinpath(file_name)
	with open(file_path) as f:
		if raw:
			data = f.read()
		else:
			data = yaml.safe_load(f)
	return data

skelfir_network, network_exports = infra.network.create()
exports = {**exports, **network_exports}

cluster_cfg = config.require_object('cluster')
cluster, cluster_exports = infra.cluster.create(cluster_cfg)
exports = {**exports, **cluster_exports}

# workaround for expiring DOKS cluster token
# see: https://github.com/pulumi/pulumi-digitalocean/issues/78#issuecomment-639669865
kube_config = kubernetes.kubeconfig.create(
	cluster,
	template=load_ext_config("kubeconfig-template.yaml", raw=True)
)
exports["kube_config"] = kube_config

k8s_provider = kubernetes.provider.create(
	kubeconfig=kube_config,
	parent=cluster
)

ingress_ns, metrics_ns = kubernetes.namespace.create(
	names=["ingress", "metrics"],
	parent=cluster,
	depends_on=[cluster],
	provider=k8s_provider
)

certificate_id = infra.certificate.get_id()
exports["certificate_id"] = certificate_id
ingress_contour = kubernetes.helm.ingress.create(
	namespace=ingress_ns,
	values=load_ext_config("contour-values.yaml"),
	loadbalancer=skelfir_network.loadbalancer,
	certificate_id=certificate_id,
	parent=ingress_ns,
	provider=k8s_provider,
	depends_on=[ingress_ns, skelfir_network]
)

metrics = kubernetes.helm.metrics.create(
	namespace=metrics_ns,
	values=load_ext_config("metrics-server-values.yaml"),
	parent=metrics_ns,
	depends_on=[metrics_ns],
	provider=k8s_provider
)

# betterstack is the monitoring and log aggregation solution
betterstack = kubernetes.helm.monitoring.create(
	namespace=metrics_ns,
	values=load_ext_config("betterstack-values.yaml"),
	parent=metrics_ns,
	provider=k8s_provider,
	depends_on=metrics.ready
)

# No need to do this when domain has
# already been registered with DigitalOcean
#domain = do.Domain(
#	"logileifs-domain",
#	name='logileifs.com',
#	#ip_address=ingress_ip.apply(lambda x: x),
#	opts=pulumi.ResourceOptions(
#		depends_on=[ingress]
#	)
#)

#db_subdomain = do.DnsRecord(
#	'db-dev-subdomain',
#	domain='skelfir.com',
#	name='db.dev',
#	type='A',
#	value=db.ipv4_address.apply(lambda x: x),
#	opts=pulumi.ResourceOptions(
#		parent=db,
#		depends_on=[db]
#	)
#)

for key, value in exports.items():
	pulumi.export(key, value)
