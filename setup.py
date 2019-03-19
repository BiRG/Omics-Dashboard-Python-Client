import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-your-username",
    version="0.0.1",
    author="BiRG @ Wright State University",
    author_email="foose.3@wright.edu",
    description="A python client for the Omics Dashboard web service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BiRG/Omics-Dashboard-Python-Client",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'h5py',
        'pandas',
        'numpy',
        'typing'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
