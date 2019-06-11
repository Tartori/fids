import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fids",
    version="0.1.0",
    author="Tartori",
    author_email="julianstampfli4@gmail.com",
    description="A forensic based intrusion detection system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tartori/fids",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
