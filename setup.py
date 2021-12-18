# coding=utf-8

import io

from setuptools import setup

setup(
    name='ares_util',
    version='0.2.2',
    description='A tool for information system allowing a retrieval '
                'of information on economic entities registered in '
                'the Czech Republic (ARES - Access to Registers of Economic Subjects / Entities).',
    long_description=io.open('README.rst', 'r', encoding='utf-8').read(),
    url='https://github.com/illagrenan/ares_util',
    license='MIT',
    author='Vasek Dohnal',
    author_email='vaclav.dohnal@gmail.com',
    packages=['ares_util'],
    install_requires=['xmltodict', 'requests'],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1'
    ],
    test_suite='tests',
    tests_require=['responses']
)
