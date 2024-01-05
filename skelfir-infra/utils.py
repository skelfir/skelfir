import shlex
import subprocess
from pathlib import Path

import yaml
import pulumi


def exec(command, capture=True, shell=True):
	# https://stackoverflow.com/a/15109975
	if not shell:
		command = shlex.split(command)
	res = subprocess.run(
		command,
		shell=shell,
		capture_output=capture,
	)
	return res


class Command(str):
	def run(self, capture=True, shell=True):
		res = exec(self, capture=capture, shell=shell)
		return res


def load_ext_config(file_name, raw=False):
	configs_path = Path.cwd().joinpath('configs')
	file_path = configs_path.joinpath(file_name)
	with open(file_path) as f:
		if raw:
			data = f.read()
		else:
			data = yaml.safe_load(f)
	return data


def export_all(exports):
	for key, value in exports.items():
		pulumi.export(key, value)
