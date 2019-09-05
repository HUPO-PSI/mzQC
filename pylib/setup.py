from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='MZQC',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/HUPO-PSI/mzQC/tree/mzqc-pylib/pylib',
    description='This is a description for abc',
    long_description=long_description,
    install_requires=[
        "jsonschema",
        "pronto",
        ],
    include_package_data=True,
)