#!/usr/bin/env python
import os

from setuptools import setup


def long_description():
    path = os.path.dirname(__file__)
    path = os.path.join(path, 'README.rst')
    try:
        with open(path) as f:
            return f.read()
    except:
        return ''


__doc__ = long_description()


setup(
    name='dailymotion-unofficial',
    version=__version__,
    url='https://github.com/amirouche/dailymotion-sdk-python-unofficial/',
    license='MIT',
    author='Amirouche Boubekki',
    author_email='amirouche.boubekki@gmail.com',
    description='Python API of Dailymotion REST API',
    long_description=__doc__,
    py_modules=['dailymotion'],
    zip_safe=False,
    platforms='any',
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
)
