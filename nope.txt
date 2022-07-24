import codecs
import re
import os
import sys

from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy as np  # for np.get_include()


###############################################################################

NAME = 'ZigZag'

PACKAGES = find_packages(where=".")

META_PATH = os.path.join("zigzag", "__init__.py")



###############################################################################

SELF_DIR = os.path.abspath(os.path.dirname(__file__))


def read_file_safely(*path_parts):
    with codecs.open(os.path.join(SELF_DIR, *path_parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read_file_safely(META_PATH)

META_VARS_RE = re.compile(r"^__([_a-zA-Z0-9]+)__ = ['\"]([^'\"]*)['\"]", re.M)

META_VARS = dict(META_VARS_RE.findall(META_FILE))

###############################################################################

README_FILE = os.path.join(os.path.dirname(__file__), 'README.rst')


CYTHON_DEBUG = '1' if 'CYTHON_DEBUG' in os.environ else '0'


EXT = Extension("*",
                ["./zigzag/*.pyx"],
                define_macros=[('CYTHON_TRACE', CYTHON_DEBUG),
                               ('CYTHON_TRACE_NOGIL', CYTHON_DEBUG),
                               ('CYTHON_BINDING', CYTHON_DEBUG),
                               ('CYTHON_FAST_PYCCALL', '1')],
                include_dirs=[".", np.get_include()])


if __name__ == "__main__":
    setup(
        name=NAME,
        ext_modules=cythonize([EXT],
                              compiler_directives={'embedsignature': True,
                              'language_level': str(sys.version_info.major),
                              'linetrace': True}),
        package_data = {'zigzag': ['*.pxd']},
        include_package_data=True,
        #description=META_VARS["description"],
        #license=META_VARS["license"],
        url=META_VARS["uri"],
        version=META_VARS["version"],
        #author=META_VARS["author"],
        #author_email=META_VARS["email"],
        #maintainer=META_VARS["author"],
        #maintainer_email=META_VARS["email"],
        long_description=read_file_safely("README.rst"),
        packages=PACKAGES,
        package_dir={"": "."},
        zip_safe=False,
    )
