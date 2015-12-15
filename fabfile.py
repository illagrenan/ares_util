# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import shutil
import sys

import six

if not six.PY2:
    print("Run Fabfile only under Python 2.x")
    sys.exit(0)

from fabric.context_managers import settings
from fabric.contrib.console import confirm
from fabric.decorators import task
from fabric.operations import local

try:
    from color_printer.colors import green, red
except ImportError:
    green = red = print


@task()
def update_package_tools():
    local("easy_install -U pip")
    local("pip install setuptools --upgrade")
    local("pip install wheel --upgrade")

    green("Updated.")


@task()
def install_requirements():
    local("pip install -r requirements.txt --upgrade --use-wheel")

    green("Installed || Updated.")


@task()
def clean():
    try:
        shutil.rmtree('ares_util.egg-info')
        shutil.rmtree('build')
        shutil.rmtree('dist')
        shutil.rmtree('__pycache__')
    except WindowsError as e:
        red(e.message)

    green("Cleaned")


@task()
def test_install():
    with settings(warn_only=True):
        local("pip uninstall ares_util --yes")
        green("Uninstall OK.")

    local("pip install --use-wheel --no-index --find-links dist ares_util")
    local("pip uninstall ares_util --yes")

    green("Install test OK.")


@task()
def test():
    local("nosetests --with-coverage --cover-package=ares_util --cover-tests --cover-erase --with-doctest")

    green("Test OK.")


@task()
def pytest():
    local("py.test ares_util --doctest-modules --cov=ares_util -v --showlocals")

    green("Test OK.")


@task()
def build():
    # pip install docutils
    local("python setup.py check --verbose --strict --restructuredtext")

    local("python setup.py build")
    local("python setup.py sdist")
    local("python setup.py bdist_wheel")
    local("python setup.py bdist_wininst")

    green("Build OK.")


@task()
def publish():
    if confirm(u'Really publish?', default=False):
        local('twine upload dist/*')

        green("Published.")


@task()
def publish_insecure():
    if confirm(u'Really publish?', default=False):
        local('python setup.py sdist upload -r pypi')
        local('python setup.py bdist_wheel upload -r pypi')

        green("Published.")
