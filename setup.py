# -*- coding: utf-8 -*-
from setuptools import setup
import sys


if sys.version_info < (3, 3):
    raise RuntimeError('roboronya requires Python 3.3+')

setup(
    author='Emmanuel García',
    author_email='emmanuel.garcia.solis@gmail.com',
    description='Hangouts bot just for fun.',
    entry_points={
        'console_scripts': [
            'roboronya = roboronya.roboronya:main',
        ],
    },
    install_requires=[
        'giphypop==0.2',
        'hangups==0.4.1',
        'pytest==3.0.3',
        'requests==2.6.0',
    ],
    license='MIT',
    name='roboronya',
    packages=['roboronya'],
    scripts=[],
    tests_require=[
        'pytest==3.0.3',
    ],
    url='https://github.com/synnick/roboronya',
    version='0.1',
)
