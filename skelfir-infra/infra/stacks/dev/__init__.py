import pulumi
import base64 as b64

import pulumi_kubernetes as k8s
import pulumi_digitalocean as do
from pulumi_kubernetes.core import v1 as core
from pulumi_kubernetes.helm import v3 as helm

config = pulumi.Config()

#skelfir_vpc = do.Vpc(
#	"example",
#	ip_range="10.10.10.0/16",
#	region=config.require('region')
#)

#db_cfg = config.require_object('db')
#db = do.Droplet(
#	db_cfg['name'],
#	monitoring=True,
#	name=db_cfg['name'],
#	size=db_cfg['size'],
#	image=db_cfg['image'],
#	region=config.require('region'),
#)


#cluster_cfg = config.require_object('cluster')
#base_node_pool = do.KubernetesNodePool(
#	auto_scale=True,
#	min_nodes=1,
#	max_nodes=cluster_cfg['base_node_pool']['node_count'],
#	name=cluster_cfg['base_node_pool']['name'],
#	size=cluster_cfg['base_node_pool']['size'],
#	node_count=cluster_cfg['base_node_pool']['node_count']
#)


cluster_cfg = config.require_object('cluster')
cluster = do.KubernetesCluster(
	cluster_cfg['name'],
	name=cluster_cfg['name'],
	region=cluster_cfg['region'],
	version=cluster_cfg['version'],
	node_pool={
		'auto_scale': True,
		'max_nodes': 1,
		'min_nodes': 1,
		'name': cluster_cfg['base_node_pool']['name'],
		'size': cluster_cfg['base_node_pool']['size'],
		'node_count': cluster_cfg['base_node_pool']['node_count']
	}
)

#def get_kubeconfig(status):
#	if status == "running":
#		clusterDataSource = cluster.name.apply(
#			lambda name: do.get_kubernetes_cluster(name)
#		)
#		return clusterDataSource.kube_configs[0].raw_config
#	else:
#		return cluster.kube_configs[0].raw_config

#kube_config = cluster.status.apply(lambda status: get_kubeconfig(status))

# workaround for expiring DOKS cluster token
# see: https://github.com/pulumi/pulumi-digitalocean/issues/78#issuecomment-639669865
kube_config_template = """
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {ca_cert}
    server: {cluster_endpoint}
  name: {cluster_name}
contexts:
- context:
    cluster: {cluster_name}
    user: {cluster_name}-{user}
  name: {cluster_name}
current-context: {cluster_name}
kind: Config
users:
- name: {cluster_name}-{user}
  user:
    token: {api_token}
"""

# workaround for expiring DOKS cluster token
# see: https://github.com/pulumi/pulumi-digitalocean/issues/78#issuecomment-639669865
def create_kubeconfig(cluster, api_token, user='admin'):
	mapping = {
		'ca_cert': cluster.kube_configs[0].cluster_ca_certificate,
		'cluster_endpoint': cluster.endpoint,
		'cluster_name': cluster.name,
		'api_token': api_token,
		'user': user,
	}
	return pulumi.Output.format(kube_config_template, **mapping)


#kube_config = cluster.kube_configs[0].raw_config.apply(lambda x: x)
kube_config = create_kubeconfig(
	cluster,
	pulumi.Config('digitalocean').require_secret('token')
)

k8s_provider = k8s.Provider(
	'do-k8s',
	kubeconfig=kube_config,
	#context='do-lon1-dev-cluster',
	opts=pulumi.ResourceOptions(
		parent=cluster
	)
)


def omit_crd_status(obj, opts):
	if obj['kind'] == 'CustomResourceDefinition':
		obj.pop('status')


ingress_ns_name = 'ingress'
ingress_ns = core.Namespace(
	'ingress-namespace',
	metadata={'name': ingress_ns_name},
	opts=pulumi.ResourceOptions(
		parent=cluster,
		depends_on=[cluster],
		provider=k8s_provider,
	)
)
#ingress_ns_name = ingress_ns.metadata.name.apply(lambda x: x)


#def fix_service_namespace(obj, opts):
#	if obj['kind'] == 'Service':
#		obj['metadata']['namespace'] = ingress_ns_name


# Managed Lets Encrypt certificate is already registered with DigitalOcean
certificate = do.get_certificate(name="skelfir")

ingress_contour = helm.Chart(
	'contour',
	helm.ChartOpts(
		namespace=ingress_ns_name,
		chart='contour',
		version="15.0.1",
		values={
			"envoy": {
				"service": {
					"annotations": {
						'service.beta.kubernetes.io/do-loadbalancer-protocol': 'http',
						'service.beta.kubernetes.io/do-loadbalancer-tls-ports': '443',
						'service.beta.kubernetes.io/do-loadbalancer-algorithm': 'round_robin',
						'service.beta.kubernetes.io/do-loadbalancer-redirect-http-to-https': 'true',
						'service.beta.kubernetes.io/do-loadbalancer-certificate-id': certificate.uuid,
						'service.beta.kubernetes.io/do-loadbalancer-disable-lets-encrypt-dns-records': 'true',
					},
					# Map the HTTPS port to HTTP - workaround for LB TLS termination
					# see: https://github.com/projectcontour/contour/issues/2441#issuecomment-625853628
					"targetPorts": {
						"https": "http"
					},
				}
			}
		},
		transformations=[],
		fetch_opts=helm.FetchOpts(
			repo='https://charts.bitnami.com/bitnami'
		)
	),
	opts=pulumi.ResourceOptions(
		parent=ingress_ns,
		provider=k8s_provider,
		depends_on=[ingress_ns],
		custom_timeouts=pulumi.CustomTimeouts(
			create="30m",
			delete="30m"
		)
	)
)

ingress_svc = ingress_contour.resources['v1/Service:ingress/contour-envoy']
#ingress_status = ingress_svc.status
ingress_ip = ingress_svc.status.apply(lambda s: s.load_balancer.ingress[0].ip)
#ingress_annotations = ingress_svc.metadata.annotations
load_balancer_id = ingress_svc.metadata.annotations.apply(
	lambda x: x.get('kubernetes.digitalocean.com/load-balancer-id')
)

metrics = helm.Chart(
	'metrics-server',
	helm.ChartOpts(
		#skip_await=True,
		namespace='kube-system',
		chart='metrics-server',
		version='3.8.2',
		values={
			'apiService': {
				'create': True
			},
			'replicas': 1,
			#'extraArgs': {
			#	'kubelet-insecure-tls': True,
			#	'kubelet-preferred-address-types': 'InternalIP'
			#}
		},
		fetch_opts=helm.FetchOpts(
			repo='https://kubernetes-sigs.github.io/metrics-server/'
		)
	),
	opts=pulumi.ResourceOptions(
		parent=cluster,
		provider=k8s_provider,
		depends_on=[cluster]
	)
)

betterstack_ns = core.Namespace(
	'betterstack-namespace',
	metadata={'name': 'betterstack'},
	opts=pulumi.ResourceOptions(
		parent=cluster,
		depends_on=[cluster],
		provider=k8s_provider,
	)
)

betterstack = helm.Chart(
	'betterstack',
	helm.ChartOpts(
		namespace='betterstack',
		chart='betterstack-logs',
		version='1.1.1',
		values={
			'metrics-server': {
				'enabled': False
			},
			'vector': {
				'customConfig': {
					'sinks': {
						'better_stack_http_sink': {
							'auth': {'token': '4fdA9Yq65r2hKcrajt9P3hBE'}
						},
						'better_stack_http_metrics_sink': {
							'auth': {'token': '4fdA9Yq65r2hKcrajt9P3hBE'}
						},
					},
					'sources': {
						'better_stack_kubernetes_logs': {
							# exclude logs from kube-system namespace
							'extra_namespace_label_selector': "kubernetes.io/metadata.name!=kube-system"
						},
						'better_stack_kubernetes_metrics_nodes': {
							'endpoint': 'https://metrics-server.kube-system/apis/metrics.k8s.io/v1beta1/nodes',
							'tls': {'verify_certificate': False}
						},
						'better_stack_kubernetes_metrics_pods': {
							'endpoint': 'https://metrics-server.kube-system/apis/metrics.k8s.io/v1beta1/pods',
							'tls': {'verify_certificate': False}
						}
					}
				}
			}
		},
		fetch_opts=helm.FetchOpts(
			repo='https://betterstackhq.github.io/logs-helm-chart'
		)
	),
	opts=pulumi.ResourceOptions(
		parent=cluster,
		provider=k8s_provider,
		depends_on=[metrics, betterstack_ns]
	)
)

#skelfir_lb = do.LoadBalancer.get('skelfir-lb', load_balancer_id)

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

dev_subdomain = do.DnsRecord(
	'skelfir-dev-subdomain',
	domain='skelfir.com',
	name='dev',
	type="A",
	value=ingress_ip.apply(lambda x: x),
	opts=pulumi.ResourceOptions(
		parent=cluster,
		depends_on=[ingress_contour]
	)
)

api_subdomain = do.DnsRecord(
	'skelfir-api-subdomain',
	domain='skelfir.com',
	name='api',
	type="A",
	value=ingress_ip.apply(lambda x: x),
	opts=pulumi.ResourceOptions(
		parent=cluster,
		depends_on=[ingress_contour]
	)
)

web_subdomain = do.DnsRecord(
	'skelfir-web-subdomain',
	domain='skelfir.com',
	name='web',
	type="A",
	value=ingress_ip.apply(lambda x: x),
	opts=pulumi.ResourceOptions(
		parent=cluster,
		depends_on=[ingress_contour]
	)
)

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


exports = {
	#'db_ip': db.ipv4_address,
	#'app': app.id,
	#'cluster': cluster,
	#'ingress': ingress,
	#'ingress_res': ingress_res,
	#'ingress_status': ingress_status,
	#'ingress_svc': ingress_svc,
	#'ingress_annotations': ingress_annotations,
	'load_balancer_id': load_balancer_id,
	'certificate_id': certificate.uuid,
	#'skelfir_lb': skelfir_lb,
	'cluster_id': cluster.id,
	'ingress_ip': ingress_ip,
	'kube_config': kube_config,
	#'db_fqdn': db_subdomain.fqdn,
	'cluster_fqdn': dev_subdomain.fqdn,
}
