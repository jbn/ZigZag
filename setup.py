from distutils.core import setup

setup(
    name='ZigZag',
    version='0.1.2',
    packages=['zigzag'],
    license='BSD-new license',
    description='Python package finding peaks and valleys of time series data.',
    long_description=open('README.rst').read(),
    author='John Bjorn Nelson',
    author_email='jbn@pathdependent.com',
    url='https://github.com/jbn/ZigZag',
    install_requires=[
        'numpy >= 1.7.0'
    ],
)
