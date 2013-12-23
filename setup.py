from setuptools import setup, find_packages

setup(
    name='pagrant',
    version='1.5',
    url='https://github.com/markshao/pagrant',
    license='MIT',
    author='markshao,yilan',
    author_email='mark.shao@emc.com',
    description='a distributed test framework',
    scripts=['bin/pagrant'],
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Developement :: Libraries :: Python Modules",
    ],
    platforms='any',
    keywords='framework nose testing',
    packages=find_packages(exclude=['test']),
    #install_requires=['Fabric==1.8.0',
    #                  'nose==1.3.0', ]
)
