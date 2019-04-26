import os
import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 7, 0):
    sys.exit('Python 3.7.0 is the minimum required version')

PROJECT_ROOT = os.path.dirname(__file__)

long_description = ""

with open(os.path.join(PROJECT_ROOT, 'README.rst')) as file_:
    long_description = file_.read()

INSTALL_REQUIRES = [
    'Quart==0.9.0',
    'docker==3.7.2',
    'async_timeout==3.0.1',
    'pydantic==0.24'
]

setup(
    name='microfaas',
    version="0.1.0",
    python_requires='>=3.7.0',
    description="A microservice to provide Functions as a Service (FaaS) with \
       a RESTful API on a small scale with Docker.",
    long_description=long_description,
    url='https://gitlab.com/DDevine/ufaas/',
    author='Daniel Devine',
    author_email='devine@ddevnet.net',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities'
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=INSTALL_REQUIRES,
    tests_require=INSTALL_REQUIRES + [
        'pytest',
        'pytest-asyncio',
    ],
    entry_points={
        'console_scripts': ['ufaas=ufaas.ufaas:main'],
    },
)
