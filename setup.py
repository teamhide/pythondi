# encoding: utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythondi",
    version="1.0.3",
    author="Hide",
    author_email="padocon@naver.com",
    description="Python dependency injection library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teamhide/pythondi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
