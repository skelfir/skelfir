import pulumi
import pulumi_digitalocean as do

stack = pulumi.get_stack()

def get_id():
	if stack == "local":
		cert_id = "fake-certificate_id"
	else:
		# Certificate is already registered with DigitalOcean
		# only need to get it
		certificate = do.get_certificate(name="skelfir")
		cert_id = certificate.uuid
	pulumi.export("certificate_id", cert_id)
	return cert_id
