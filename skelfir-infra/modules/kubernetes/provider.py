import pulumi
import pulumi_kubernetes as k8s

def create(kubeconfig=None, context=None, parent=None):
	return k8s.Provider(
		"do-k8s-provider",
		kubeconfig=kubeconfig,
		#context='do-lon1-dev-cluster',
		opts=pulumi.ResourceOptions(
			parent=parent
		)
	)
