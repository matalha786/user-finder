from setuptools import setup, find_packages

setup(
    name="user-finder-zeta",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "rich",
        "requests",
        "argparse"
    ],
    entry_points={
        "console_scripts": [
            "user-finder-zeta=main:main",
        ],
    },
)
