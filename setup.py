# coding=utf-8

import os

from setuptools import setup, find_packages

# https://coderwall.com/p/qawuyq
os.system("pandoc --from=markdown --to=rst README.md -o README.rst")

# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
setup(
    name='ares_util',
    version='0.0.4',
    description='A tool for information system allowing a retrieval '
                'of information on economic entities registered in '
                'the Czech Republic (ARES - Access to Registers of Economic Subjects / Entities).',
    long_description=(open('README.rst').read()),
    url='https://github.com/illagrenan/ares_util',
    license='MIT',
    author='Vašek Dohnal',
    author_email='vaclav.dohnal@gmail.com',

    # The exclude makes sure that a top-level tests package doesn’t get
    # installed (it’s still part of the source distribution)
    # since that would wreak havoc.
    packages=find_packages(exclude=['tests*']),


    install_requires=['xmltodict', ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers'
    ],
)

os.remove('README.rst')