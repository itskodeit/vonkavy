from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in vonkavy/__init__.py
from vonkavy import __version__ as version

setup(
	name="vonkavy",
	version=version,
	description="Poultry Management App",
	author="KODEIT",
	author_email="smaftah@kodeit.co.tz",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
