from setuptools import setup, find_packages

setup(
    name="mad8-pandas",
    version="0.1.1",
    description="load mad8 output with pandas",
    packages=find_packages(include=["pand8"]),
    install_requires=["pandas", "fortranformat", "numpy"],
    url="https://github.com/st-walker/mad8-pandas",
    license="MIT",
    keywords="mad8 pandas twiss",
    author="Stuart Walker",
    author_email="stuart.walker@desy.de",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ]
)
