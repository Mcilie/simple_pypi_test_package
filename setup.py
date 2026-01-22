from setuptools import setup, find_packages

setup(
    name="simple_pypi_test_package",
    version="0.1.0",
    packages=find_packages(),
    author="Mcilie",
    description="A simple test package that prints a welcome message when imported",
    python_requires=">=3.6",
)
