import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynifs",
    version="0.1.1",
    description="Unified file access interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rwiv/pynifs",
    packages=setuptools.find_packages(),
    install_requires=[
        "pydantic==2.10.6",
        "boto3==1.36.21",
    ],
)
