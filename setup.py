import setuptools
import tinyserializable

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tinyserializable",
    version=tinyserializable.__version__,
    author="Spajderix",
    author_email="spajderix@gmail.com",
    description="Library to allow of creation of serializable/deserializable class-based structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Spajderix/tinyserializable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
