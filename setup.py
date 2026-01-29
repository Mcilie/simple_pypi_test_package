from setuptools import setup, find_packages

setup(
    name="simple_pypi_test_package",
    version="0.2.0",
    packages=find_packages(),
    package_data={"simple_pypi_test_package": ["model_parts/*"]},
    include_package_data=True,
    author="Mcilie",
    description="EmbeddingGemma-300M model packaged for PyPI distribution",
    python_requires=">=3.7",
)
