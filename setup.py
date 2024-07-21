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
    name='fetch_ing_price',
    description="Fetch Stock prices from the ING website",
    url="https://github.com/matthiasbeyer/fetch-ing-prices/",
    version='0.1.0',
    py_modules=["fetch_ing_price"],
    install_requires=read_requirements("requirements.txt"),
    entry_points={"console_scripts": ["fetch_ing_price = fetch_ing_price:main"]},
)

