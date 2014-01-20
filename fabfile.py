# coding=utf-8

from fabric import colors
from fabric.context_managers import settings
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


def test_install():
    local("easy_install -U pip")
    local("pip install setuptools --upgrade")
    with settings(warn_only=True):
        local("pip uninstall ares_util --yes")
    local("pip install --use-wheel --no-index --find-links dist ares_util")


def test():
    local("nosetests --with-coverage --cover-package=ares_util --cover-tests --cover-erase --with-doctest")
    _print_success("Done.")


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