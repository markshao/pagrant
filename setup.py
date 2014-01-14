from setuptools import setup, find_packages
from pagrant.version import version_number

setup(
    name='pagrant',
    version=version_number(),
    url='https://github.com/markshao/pagrant',
    license='MIT',
    author='markshao,xiaobo',
    author_email='mark.shao@emc.com',
    description='a distributed test framework',
    scripts=['bin/pagrant'],
    classifiers=[
        "Programming Language :: Python",
    ],
    platforms='any',
    keywords='framework nose testing',
    packages=find_packages(exclude=['test']),
    install_requires=['Fabric==1.8.0',
                      'nose==1.3.0',
                      'colorama==0.2.7']
)
