from setuptools import setup, find_packages

setup(
    name="pand8",
    version="0.1.0",
    description="load mad8 output with pandas",
    install_requires=["pandas", "fortranformat", "numpy"],
    license="MIT",
)
