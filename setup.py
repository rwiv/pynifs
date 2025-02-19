import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynifs",
    version="0.1.3",
    description="Unified file access interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rwiv/pynifs",
    packages=setuptools.find_packages(),
    install_requires=[
        "pydantic==2.10.6",
        "boto3==1.36.21",
        "boto3-stubs[s3]==1.36.21",
        "urllib3==2.3.0",
    ],
)
