# coding=utf-8

from setuptools import setup, find_packages


# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
setup(
    name='ares_util',
    version='0.0.1',
    description='Zakladni informace z ARES API.',
    long_description=(open('README.md').read()),
    url='https://github.com/illagrenan/ares_util',
    license='MIT',
    author='Vašek Dohnal',
    author_email='vaclav.dohnal@gmail.com',

    # The exclude makes sure that a top-level tests package doesn’t get
    # installed (it’s still part of the source distribution)
    # since that would wreak havoc.
    packages=find_packages(exclude=['tests*']),


    install_requires=['xmltodict',],

    py_modules=['ares'],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
)