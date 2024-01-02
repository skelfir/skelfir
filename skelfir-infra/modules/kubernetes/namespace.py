import pulumi
from pulumi_kubernetes.core import v1 as core

def create(
	names=None,
	parent=None,
	depends_on=None,
	provider=None,
):
	namespaces = []
	for name in names:
		namespace = core.Namespace(
			f"{name}-namespace",
			metadata={"name": name},
			opts=pulumi.ResourceOptions(
				parent=parent,
				depends_on=depends_on,
				provider=provider,
			)
		)
		namespaces.append(namespace)
	return namespaces
