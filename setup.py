import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cotter",
    version="0.0.4",
    author="Cotter",
    author_email="putri@cotter.app",
    description="Cotter Login SDK for python scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cotterapp/python-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "python-jose", "cryptography"]
)
