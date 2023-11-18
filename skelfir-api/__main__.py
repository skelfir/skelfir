import pulumi
import pulumi_docker as docker

#registry = docker.ImageRegistry('docker.io')

image = docker.Image(
	'my-image',
	build='.',
	image_name='logileifs/skelfir-api',
	#registry=registry,
)

pulumi.export('baseImageName', image.base_image_name)
pulumi.export('fullImageName', image.image_name)
