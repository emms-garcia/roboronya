# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


if sys.version_info < (3, 3):
    raise RuntimeError('roboronya requires Python 3.3+')


class PytestCommand(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

with open('README.md') as f:
    README = f.read()

with open('requirements.txt') as f:
    REQUIREMENTS = list(map(str.strip, f.readlines()))

setup(
    author='Emmanuel García',
    author_email='emmanuel.garcia.solis@gmail.com',
    cmdclass={
        'test': PytestCommand,
    },
    description='Hangouts bot just for fun.',
    entry_points={
        'console_scripts': [
            'roboronya = roboronya.__main__:main',
        ],
    },
    install_requires=REQUIREMENTS,
    license='MIT',
    long_description=README,
    name='roboronya',
    packages=['roboronya'],
    scripts=[],
    tests_require=[
        'pytest==3.0.3',
    ],
    url='https://github.com/synnick/roboronya',
    version='0.1',
)
