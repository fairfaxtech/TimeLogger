#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="timelogger",
    version="0.1.0",
    author="fairfaxtech",
    description="A simple command-line time tracking tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fairfaxtech/TimeLogger",
    py_modules=["timelogger"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "timelogger=timelogger:cli",
        ],
    },
)