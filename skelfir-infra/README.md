[![Pulumi](https://github.com/skelfir/infra/actions/workflows/push.yml/badge.svg?branch=main)](https://github.com/skelfir/infra/actions/workflows/push.yml)

# Skelfir infra
Infrastructure provisioning for skelfir.com

## Infrastructure overview
![alt text](https://github.com/skelfir/skelfir/blob/main/skelfir-infra/skelfir_infra_overview.png?raw=true)

## Project structure
```
.
├── __main__.py
├── README.md
├── poetry.toml
├── poetry.lock
├── pyproject.toml
├── Pulumi.yaml
├── Pulumi.local.yaml
├── Pulumi.dev.yaml
├── infra/
├── modules/
├── configs/
└── providers/
```
1. Entrypoint is `__main__.py`
2. `modules/` contains the logical units of the infrastructure as python modules, such as `modules/cluster.py` which contains the code for provisioning a Kubernetes cluster.
3. `modules/infra/` contains cloud provider specific logic, such as loadbalancer provisioning, spinning up VMs and networking.
4. `modules/kubernetes/` contains anything that is kubernetes cluster related.
4. `providers/` contains custom providers/resources such as the bespoke K3D cluster provider and resource.
5. `configs/` contains external configuration files such as values files for helm charts and templates that need rendering.
6. All configuration that is directly relevant to the infrastructure itself, such as node pool config for the k8s cluster, region or encrypted secrets goes to the relevant stack's config file ,`Pulumi.local.yaml` for the local stack.
### Stacks
There are 3 configured stacks
1. `local` - ephemeral local environment using k3d for local kubernetes.
2. `dev` - ephemeral environment to spin up and destroy on demand replicates `prod` almost 100%
3. `prod` - the production environment

## Getting started
1. Create a virtualenv - `mkvirtualenv -p python3.11 skelfir-infra`
2. Activate the virtualenv - `activate skelfir-infra`
3. Make sure poetry is installed - `pipx install poetry`
4. Install the dependencies - `poetry install`
5. Make sure to have a DigitalOcean token in the right place (pulumi config or env variable)
6. Preview the infrastructure state - `pulumi preview`
7. Apply changes - `pulumi up --stack <STACK_NAME>`
