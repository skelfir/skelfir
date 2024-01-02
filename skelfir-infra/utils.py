import shlex
import subprocess


def exec(cmd, capture=True, shell=True):
	res = subprocess.run(
		shlex.split(cmd),
		shell=shell,
		capture_output=capture,
	)
	return res


class Command(str):
	def run(self, capture=True):
		res = exec(self, capture=capture)
		return res
