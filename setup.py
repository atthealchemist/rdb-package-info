#!/usr/bin/env python3

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

from distutils.core import setup


def get_requirements():
    requirements = parse_requirements("requirements.txt", session="test")
    return [str(package.req) for package in requirements]


setup(
    name='rdb-package-info',
    version='1.0',
    description='Test task for BaseAlt',
    author='atthealchemist',
    author_email='at.thealchemist@gmail.com',
    url='https://github.com/atthealchemist/rdb-package-info',
    packages=['modules'],
    install_requires=get_requirements()
)
