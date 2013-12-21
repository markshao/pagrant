from __future__ import with_statement

import os

from setuptools import setup, find_packages


README = os.path.join(os.path.dirname(__file__), 'README.md')
REQUIREMENT = os.path.join(os.path.dirname(__file__), 'requirements.txt')


def dependency():
    with open(REQUIREMENT) as f:
        filter(lambda x: x != '', f.read().split("\n"))


setup(
    name='pagrant',
    version='1.0',
    url='https://github.com/markshao/pagrant',
    license='MIT',
    author='markshao,yilan',
    author_email='mark.shao@emc.com',
    description=('a automatic test framwork', "from IIG EMC Inc"),
    long_description=open(README).read() + "\n\n",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Developement :: Libraries :: Python Modules",
    ],
    keywords='framework nose testing',
    packages=find_packages(exclude=['test']),
    package_data={'': ['*.*'], },
    namespace_packages=['pagrant'],
    install_requires=dependency(),
)