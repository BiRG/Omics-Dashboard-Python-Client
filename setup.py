import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="omics-dashboard-client",
    version="19.03a",
    author="BiRG @ Wright State University",
    author_email="foose.3@wright.edu",
    description="A python client for the Omics Dashboard web service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BiRG/Omics-Dashboard-Python-Client",
    packages=setuptools.find_packages(),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=[
        'requests>=2.10.0',
        'h5py>=2.6.0',
        'pandas>=0.18.0',
        'numpy>=1.11.0',
        'scipy>=0.18.0',
        'typing>=3.5.0'
    ],
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
