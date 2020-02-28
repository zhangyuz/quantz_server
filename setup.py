# -*- coding: utf-8 -*-
from os.path import dirname, join
from setuptools import find_packages, setup


def read_file(file):
    with open(file, "rt") as f:
        content = f.read()
        print(content)
        return content


with open(join(dirname(__file__), 'quantz_server/VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='quantz_server',
    version=version,
    description='QuantZ backend server by Yuz',
    packages=find_packages(exclude=[]),
    author='Zhang Yuzheng',
    author_email='me@zhangyuzheng.com',
    license='Apache License v2',
    package_data={'': ['*.*']},
    install_requires=read_file("requirements.txt").strip(),
    zip_safe=False,
    #    entry_points={
    #        "console_scripts": [
    #            "ma_filter = quantz.ma_filter_main:run",
    #            "growing_value_filter = quantz.growing_value_filter_main:run"
    #        ]
    #    },
)
