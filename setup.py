import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dialpy-fmi", # Replace with your own username
    version="0.0.1",
    author="Antti J Manninen",
    author_email="antti.manninen@fmi.fi",
    description="DIAL processing package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dl-fmi/dialpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
)
