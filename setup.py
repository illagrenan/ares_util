# coding=utf-8

import io

from setuptools import setup

setup(
    name='ares_util',
    version='0.1.10.1',
    description='A tool for information system allowing a retrieval '
                'of information on economic entities registered in '
                'the Czech Republic (ARES - Access to Registers of Economic Subjects / Entities).',
    long_description=io.open("README.rst", 'r', encoding="utf-8").read(),
    url='https://github.com/illagrenan/ares_util',
    license='MIT',
    author='Vasek Dohnal',
    author_email='vaclav.dohnal@gmail.com',
    packages=['ares_util'],
    install_requires=['xmltodict', 'future', 'requests'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers'
    ],
)
