import pulumi

from pulumi_kubernetes.helm import v3 as helm


def create(
	namespace=None,
	values=None,
	loadbalancer=None,
	certificate_id=None,
	parent=None,
	provider=None,
	depends_on=None
):
	if loadbalancer:
		loadbalancer_id = loadbalancer.id
	else:
		loadbalancer_id = 'some-id'

	annotations = values["envoy"]["service"]["annotations"]
	annotations["kubernetes.digitalocean.com/load-balancer-id"] = loadbalancer_id
	annotations["service.beta.kubernetes.io/do-loadbalancer-certificate-id"] = certificate_id

	ingress_contour = helm.Chart(
		'contour',
		helm.ChartOpts(
			namespace=namespace.metadata.name,
			chart='contour',
			version="15.0.1",
			values=values,
			transformations=[],
			fetch_opts=helm.FetchOpts(
				repo='https://charts.bitnami.com/bitnami'
			)
		),
		opts=pulumi.ResourceOptions(
			parent=parent,
			provider=provider,
			depends_on=depends_on,
			custom_timeouts=pulumi.CustomTimeouts(
				create="30m",
				delete="30m"
			)
		)
	)
