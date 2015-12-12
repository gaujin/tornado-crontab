from encodings import codecs
import io
import os
import re

from setuptools import setup


here = os.path.dirname(__file__)


def read(*names, **kwargs):
    with io.open(os.path.join(here, *names),
                 encoding=kwargs.get("encoding", "utf8")) as f:
        return f.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^version = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with codecs.open(os.path.join(here, "README.rst"), encoding="utf8") as f:
    long_description = f.read()


setup(
    name="tornado-crontab",
    version=find_version("tornado_crontab", "__init__.py"),
    packages=["tornado_crontab"],
    install_requires=["tornado", "crontab"],
    author="Takehito Yamada",
    author_email="tornado-crontab@gaujin.jp",
    url="https://github.com/gaujin/tornado-crontab",
    license="MIT",
    description="CronTab callback for Tornado",
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
