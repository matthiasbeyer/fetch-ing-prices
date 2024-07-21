import io
import os
from setuptools import setup, find_packages

def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]

setup(
    name='fetch-ing-prices',
    description="Fetch Stock prices from the ING website",
    url="https://github.com/matthiasbeyer/fetch-ing-prices/",
    version='0.1.0',
    packages=find_packages(include=['fetch-ing-prices']),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        'console_scripts': ['fetch-ing-prices=fetch-ing-prices.__main__:main']
    }
)

