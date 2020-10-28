import setuptools
from elkpy import __version__
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elkpy",
    version=__version__,
    author="Ruben Svensson",
    author_email="ruben@elk.audio",
    description="A basic controller for sushi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elk-audio/elkpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'protobuf',
    ],
    python_requires='>=3.6',
)
