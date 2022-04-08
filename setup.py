from setuptools import find_packages, setup
from dbx_sample import __version__

setup(
    name="dbx_sample",
    packages=find_packages(exclude=["tests", "tests.*"]),
    setup_requires=["wheel"],
    version=__version__,
    description="",
    author=""
)
