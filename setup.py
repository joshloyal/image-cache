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


setup(name='image-cache',
      version='0.0.1',
      description='A quick and dirty image cache.',
      author='Joshua D. Loyal',
      author_email='joshua.d.loyal@gmail.com',
      url='https://github.com/joshloyal/image-cache',
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      test_require=['pytest', 'pytest-pep8',
                    'PIL', 'numpy'],
      keywords='images',
      )
