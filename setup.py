import os
from setuptools import setup

def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

setup(
    name="evdutyfree",
    version="0.0.1",
    description="Unofficial module for interacting with EVDuty EV charger api",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords="",
    author="Jean-Marc G",
    author_email="none@none.none",
    url="https://github.com/planetefrench/evduty-free",
    license="Apache 2",
    packages=["evdutyfree"],
    install_requires=["requests>=2.22.0", "simplejson>=3.16.0", "aenum>=3.1.8"],
    python_requires=">=3.7",
    classifiers=["Programming Language :: Python :: 3",],
)