# coding=utf-8

from setuptools import setup

try:
    from pypandoc import convert

    read_md = lambda f: convert(f, 'rst')
    # http://stackoverflow.com/a/23265673/752142
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
setup(
    name='ares_util',
    version='0.1.6',
    description='A tool for information system allowing a retrieval '
                'of information on economic entities registered in '
                'the Czech Republic (ARES - Access to Registers of Economic Subjects / Entities).',

    # ########################################################################
    #
    # README.rst is generated from README.md:
    #
    # $ pandoc --from=markdown --to=rst README.md -o README.rst
    #
    # ~ OR ~
    #
    # $ fab build
    # ########################################################################
    long_description=read_md('README.md'),

    url='https://github.com/illagrenan/ares_util',
    license='MIT',
    author='Vasek Dohnal',
    author_email='vaclav.dohnal@gmail.com',

    # The exclude makes sure that a top-level tests package doesn’t get
    # installed (it’s still part of the source distribution)
    # since that would wreak havoc.
    # find_packages(exclude=['tests*'])
    packages=['ares_util'],


    install_requires=['xmltodict', 'future', 'requests'],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers'
    ],
)
