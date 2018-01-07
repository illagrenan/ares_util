# -*- encoding: utf-8 -*-
# ! python3

import sys

import os
import shutil
import warnings
import webbrowser
from invoke import task

PROJECT_NAME = 'ares_util'


@task
def clean(ctx):
    """remove build artifacts"""
    shutil.rmtree('{PROJECT_NAME}.egg-info'.format(PROJECT_NAME=PROJECT_NAME), ignore_errors=True)
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('htmlcov', ignore_errors=True)
    shutil.rmtree('__pycache__', ignore_errors=True)


@task
def lint(ctx):
    """check style with flake8"""
    ctx.run("flake8 {PROJECT_NAME}/ tests/".format(PROJECT_NAME=PROJECT_NAME))


@task
def test(ctx):
    ctx.run("py.test")


@task
def test_all(ctx):
    """run tests on every Python version with tox"""
    ctx.run("tox")


@task
def check(ctx):
    """Check setup"""
    ctx.run("python setup.py --no-user-cfg --verbose check --metadata --restructuredtext --strict")


@task
def coverage(ctx):
    """check code coverage quickly with the default Python"""
    ctx.run("coverage run --source {PROJECT_NAME} -m py.test".format(PROJECT_NAME=PROJECT_NAME))
    ctx.run("coverage report -m")
    ctx.run("coverage html")

    if not os.getenv('TRAVIS') and (sys.stdout.isatty() and sys.stdin.isatty() and sys.stderr.isatty()):
        # Running in a real terminal
        webbrowser.open('file://' + os.path.realpath("htmlcov/index.html"), new=2)


@task
def test_install(ctx):
    """try to install built package"""
    ctx.run("pip uninstall {PROJECT_NAME} --yes".format(PROJECT_NAME=PROJECT_NAME), warn=True)
    ctx.run("pip install --use-wheel --no-cache-dir --no-index --find-links=file:./dist {PROJECT_NAME}".format(PROJECT_NAME=PROJECT_NAME))
    ctx.run("pip uninstall {PROJECT_NAME} --yes".format(PROJECT_NAME=PROJECT_NAME))


@task
def build(ctx):
    """build package"""
    ctx.run("python setup.py build")
    ctx.run("python setup.py sdist")
    ctx.run("python setup.py bdist_wheel")


@task
def publish(ctx):
    """publish package"""
    warnings.warn("Deprecated", DeprecationWarning, stacklevel=2)

    check()
    ctx.run('python setup.py sdist upload -r pypi')  # Use python setup.py REGISTER
    ctx.run('python setup.py bdist_wheel upload -r pypi')


@task
def publish_twine(ctx):
    """publish package"""
    check()
    ctx.run('twine upload dist/* --skip-existing')


@task
def publish_test(ctx):
    """publish package"""
    check()
    ctx.run('python setup.py sdist upload -r https://testpypi.python.org/pypi')  # Use python setup.py REGISTER
    ctx.run('python setup.py bdist_wheel upload -r https://testpypi.python.org/pypi')
