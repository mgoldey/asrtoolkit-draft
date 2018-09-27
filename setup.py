#!/usr/bin/env python
"""
Creates asrtoolkit
"""
from setuptools import setup

setup(
  name='asrtoolkit',
  version='0.1',
  description='ASR toolkit for processing ',
  url='http://github.com/asrtool',
  author='Matthew Goldey',
  author_email='matthew.goldey@gmail.com',
  install_requires=['edit_distance', 'termcolor', 'asr_evaluation'],
  keywords=['word', 'error', 'rate', 'asr', 'speech', 'recognition'],
  entry_points={'console_scripts': ['convert_text = asrtoolkit.convert_text:main']},
  license='Apache v2',
  packages=['asrtoolkit'],
  zip_safe=True
)
