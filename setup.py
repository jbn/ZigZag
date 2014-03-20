import os
from distutils.core import setup

README_FILE = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='ZigZag',
    version='0.1.3',
    packages=['zigzag'],
    license='BSD-new license',
    description='Python package finding peaks and valleys of time series data.',
    long_description=open(README_FILE).read(),
    author='John Bjorn Nelson',
    author_email='jbn@pathdependent.com',
    url='https://github.com/jbn/ZigZag',
    install_requires=[
        'numpy >= 1.7.0'
    ],
    data_files=['README.rst']
)
