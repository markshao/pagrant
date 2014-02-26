from setuptools import setup, find_packages

setup(
    name='pagrant',
    version="1.0.4",
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
    install_requires=['fabric',
                      'nose',
                      'colorama',
                      'six',
                      'requests',
                      'jenkinsapi',
                      'ecdsa',
                      'texttable',
                      'websocket']
)
