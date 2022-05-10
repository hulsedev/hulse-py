from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="hulse",
    description="The Python client for the Hulse platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.2",
    packages=find_packages(),
    install_requires=["requests", "click", "transformers", "torch"],
    license="MIT",
    entry_points={
        "console_scripts": [
            "hulse = hulse.cli:cli",
        ],
    },
)
