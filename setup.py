#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from src import manifest

setup(
    name=manifest.name,
    use_scm_version=True,
    setup_requires=['setuptools_scm', 'pytest_runner'],
    description=manifest.description,
    author=manifest.author,
    author_email=manifest.email,
    url=manifest.url,
    packages=find_packages(exclude=('tests',)),
    entry_points='''
        [console_scripts]
        nepo=src.cli:entry_point
    ''',
    install_requires=[
        'click',
        'click-didyoumean',
        'click-help-colors',
        'crayons',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-random-order',
        'mock',
    ],
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
