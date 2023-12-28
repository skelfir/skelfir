[![Pulumi](https://github.com/skelfir/infra/actions/workflows/push.yml/badge.svg?branch=main)](https://github.com/skelfir/infra/actions/workflows/push.yml)

# infra
Infrastructure creation and updates for skelfir

## Getting started
1. Create a virtualenv - `mkvirtualenv -p python3.11 skelfir-infra`
2. Activate the virtualenv - `activate skelfir-infra`
3. Make sure poetry is installed - `pipx install poetry`
4. Install the dependencies - `poetry install`
5. Make sure to have a DigitalOcean token in the right place (pulumi config or env variable)
6. Preview the infrastructure state - `pulumi preview`
7. Apply changes - `pulumi up`
