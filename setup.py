from setuptools import setup, find_packages


setup(
    name="prettypi",
    version="0.1.2",

    description="A Python library for pretty printing and enhanced console output.",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author="Vodkas",
    license="MIT",
    packages=find_packages(exclude=("tests")),
    install_requires=[
        "setuptools",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
