import pulumi
import pulumi_digitalocean as do

stack = pulumi.get_stack()


def provision_loadbalancer(parent=None):
	if stack == "local":
		return None
	return do.LoadBalancer(
		"skelfir-lb",
		region="lon1",
		forwarding_rules=[
			do.LoadBalancerForwardingRuleArgs(
				entry_port=80,
				entry_protocol="http",
				target_port=80,
				target_protocol="http",
			)
		],
		opts=pulumi.ResourceOptions(
			parent=parent
		)
	)


def provision_dnsrecord(
	domain="skelfir.com",
	name=None,
	type="A",
	value=None,
	parent=None
):
	if stack == "local":
		return None
	return do.DnsRecord(
		f"skelfir-{name}-subdomain",
		domain=domain,
		name=name,
		type="A",
		value=value,
		opts=pulumi.ResourceOptions(
			parent=parent,
			depends_on=[]
		)
	)


class SkelfirNetwork(pulumi.ComponentResource):
	def __init__(self, name, opts = None):
		super().__init__('skelfir:network:SkelfirNetwork', name, None, opts)
		# Not necessary to provision a VPC since
		# DigitalOcean automatically creates one
		#skelfir_vpc = do.Vpc(
		#	"example",
		#	ip_range="10.10.10.0/16",
		#	region=config.require('region')
		#)

		skelfir_lb = provision_loadbalancer(parent=self)

		dev_subdomain = provision_dnsrecord(
			name="dev",
			value=skelfir_lb.ip.apply(lambda ip: ip),
			parent=skelfir_lb,
		)

		api_subdomain = provision_dnsrecord(
			name="api",
			value=skelfir_lb.ip.apply(lambda ip: ip),
			parent=skelfir_lb,
		)

		web_subdomain = provision_dnsrecord(
			name="web",
			value=skelfir_lb.ip.apply(lambda ip: ip),
			parent=skelfir_lb,
		)

		self.loadbalancer = skelfir_lb
		#self.loadbalancer_id = skelfir_lb.id
		#self.loadbalancer_ip = skelfir_lb.ip
		self.dev_subdomain = dev_subdomain
		self.register_outputs({
			#"loadbalancer_id": skelfir_lb.id,
			#"loadbalancer_ip": skelfir_lb.ip,
			"dev_subdomain": dev_subdomain,
		})


def create(ip_address=None, parent=None):
	network = SkelfirNetwork("skelfir-network")
	exports = {}
	if stack == "local":
		exports["ingress_ip"] = "127.0.0.1"
		exports["cluster_fqdn"] = "localhost"
		#pulumi.export('ingress_ip', '127.0.0.1')
		#pulumi.export("cluster_fqdn", "localhost")
	else:
		exports["ingress_ip"] = network.loadbalancer.ip
		exports["loadbalancer_id"] = network.loadbalancer.id
		exports["cluster_fqdn"] = network.dev_subdomain.fqdn
		#pulumi.export('ingress_ip', network.loadbalancer.ip)
		#pulumi.export('loadbalancer_id', network.loadbalancer.id)
		#pulumi.export('cluster_fqdn', network.dev_subdomain.fqdn)
	return network, exports
