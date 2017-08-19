from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os
from setuptools import setup, find_packages


HERE = os.path.dirname(os.path.abspath(__file__))

# import ``__veresion__`` from code base
exec(open(os.path.join(HERE, 'image_cache', 'version.py')).read())


with open('requirements.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]


TEST_REQUIRES = [
    'pytest', 'pytest-pep8', 'PIL', 'numpy'
]

DISTNAME = 'image-cache'
DESCRIPTION = 'A quick and dirty image cache.'
with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

AUTHOR = 'Joshua D. Loyal'
AUTHOR_EMAIL = 'joshua.d.loyal@gmail.com'
MAINTAINER = 'Joshua D. Loyal'
MAINTAINER_EMAIL = 'joshua.d.loyal@gmail.com'
URL = 'https://github.com/joshloyal/image-cache'
LICENSE = 'MIT'
VERSION = __version__


def setup_package():
    metadata = dict(name=DISTNAME,
                    author=AUTHOR,
                    author_email=AUTHOR_EMAIL,
                    maintainer=MAINTAINER,
                    maintainer_email=MAINTAINER_EMAIL,
                    description=DESCRIPTION,
                    license=LICENSE,
                    url=URL,
                    version=VERSION,
                    long_description=LONG_DESCRIPTION,
                    packages=find_packages(),
                    install_requires=INSTALL_REQUIRES,
                    test_requires=TEST_REQUIRES,
                    keywords='images',
                    classifiers=[
                        "Intended Audience :: Developers",
                        "Intended Audience :: Science/Research",
                        "License :: OSI Approved :: MIT License",
                        "Operating System :: POSIX :: Linux",
                        "Operating System :: MacOS :: MacOS X",
                        "Programming Language :: Python :: 3.6"])
    setup(**metadata)


if __name__ == "__main__":
    setup_package()
