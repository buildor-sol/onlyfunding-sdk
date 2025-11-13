from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="onlyfunding-sdk",
    version="1.0.0",
    author="onlyfunding",
    author_email="support@onlyfunding.fun",
    description="Official Python SDK for onlyfunding.fun funding rates API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/onlyfunding/onlyfunding-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
)

