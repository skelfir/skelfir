import pulumi
from pulumi_kubernetes.helm import v3 as helm


def create(
	namespace=None,
	values=None,
	parent=None,
	depends_on=None,
	provider=None,
):
	return helm.Chart(
		'metrics-server',
		helm.ChartOpts(
			namespace=namespace.metadata.name,
			chart='metrics-server',
			version='3.8.2',
			values=values,
			fetch_opts=helm.FetchOpts(
				repo='https://kubernetes-sigs.github.io/metrics-server/'
			)
		),
		opts=pulumi.ResourceOptions(
			parent=parent,
			provider=provider,
			depends_on=depends_on
		)
	)
