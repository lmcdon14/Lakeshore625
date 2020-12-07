from setuptools import find_packages, setup
from package import Package

setup(
    author="Landen McDonald",
    author_email="mcdonaldl@ornl.gov",
    packages=find_packages(),
    include_package_data=True,
    cmdclass={
        "package": Package
    }
)