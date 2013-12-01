# coding=utf-8


#$ python setup.py sdist
#$ python setup.py bdist_wheel
#
#$ pip install --no-index dist/*.zip
#$ pip install --use-wheel --no-index --find-links dist ares_util
#
#$ pip uninstall ares_util
#$ easy_install -U pip
#$ pip install setuptools --upgrade
#
#$ python setup.py sdist upload -r pypi
#$ python setup.py bdist_wheel upload -r pypi
from fabric import colors
from fabric.contrib.console import confirm
from fabric.operations import local


def _print_success(message):
    try:
        from colorama import init, Back

        init()
        print(Back.GREEN + colors.white(u"%s" % message, bold=True))
    except ImportError:
        print(colors.green(u"%s" % message, bold=True))


def update_package_tools():
    local("easy_install -U pip")
    local("pip install setuptools --upgrade")

    _print_success("Updated.")


def build():
    # https://coderwall.com/p/qawuyq
    local("nosetests --with-coverage --cover-package=ares_util --cover-tests --cover-erase --with-doctest")
    local("pandoc --from=markdown --to=rst README.md -o README.rst")
    local("python setup.py sdist")
    local("python setup.py bdist_wheel")

    _print_success("Done.")


def publish():
    if confirm(u'Really publish?', default=False):
        local('python setup.py sdist upload -r pypi')
        local('python setup.py bdist_wheel upload -r pypi')

        _print_success("Published.")