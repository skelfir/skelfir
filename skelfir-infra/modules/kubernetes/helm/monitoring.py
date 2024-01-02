import pulumi
from pulumi_kubernetes.helm import v3 as helm


def create(
	namespace=None,
	values=None,
	parent=None,
	provider=None,
	depends_on=None
):
	betterstack_token = pulumi.Config('betterstack').require_secret('token')
	sinks = values["vector"]["customConfig"]["sinks"]
	sinks["better_stack_http_sink"]["auth"]["token"] = betterstack_token
	return helm.Chart(
		'betterstack',
		helm.ChartOpts(
			namespace=namespace.metadata.name,
			chart='betterstack-logs',
			version='1.1.1',
			values=values,
			fetch_opts=helm.FetchOpts(
				repo='https://betterstackhq.github.io/logs-helm-chart'
			)
		),
		opts=pulumi.ResourceOptions(
			parent=parent,
			provider=provider,
			depends_on=depends_on
		)
	)
