from setuptools import setup, find_packages
import os

README = os.path.join(os.path.dirname(__file__), 'README.md')
setup(
    name = 'pagrant',
    version = '1.0',
    url = 'https://github.com/markshao/pagrant',
    license = 'MIT',
    author ='markshao, yilan',
    author_email = 'mark.shao@emc.com',
    description = ('a automatic test framwork', "from IIG EMC Inc"),
    long_description = open(README).read() + "\n\n",
    classifiers = [
    	"Programming Language :: Python",
    	("Topic :: Software Developement :: Libraries :: Python Modules"),
    ],
    keywords = 'framework nose testing',
    packages = find_packages(),
    package_data = {'':['*.*'],},
    namespace_packages = ['pagrant'],
    install_requires = ['Fabric>=1.8.0',
                        'esdsa>=0.10',
                        'nose>=1.3.0',
                        'paramiko>=1.12.0',
                        'pycrypto>=2.6.1',
                        'wsgiref>=0.1.2',
                       ],
)