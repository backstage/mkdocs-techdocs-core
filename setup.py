"""
Copyright 2020 The Backstage Authors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from setuptools import setup, find_packages
from os import path

# Read the contents of the README file in the current directory
this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

# Read the contents of the requirements.txt file
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="mkdocs-techdocs-core",
    version="0.1.1",
    description="The core MkDocs plugin used by Backstage's TechDocs as a wrapper around "
    "multiple MkDocs plugins and Python Markdown extensions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="mkdocs",
    url="https://github.com/backstage/mkdocs-techdocs-core",
    author="TechDocs Core",
    author_email="pulp-fiction@spotify.com",
    license="Apache-2.0",
    python_requires=">=3.7",
    install_requires=required,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    entry_points={"mkdocs.plugins": ["techdocs-core = src.core:TechDocsCore"]},
)
