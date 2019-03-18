"""
.. Dstl (c) Crown Copyright 2019
"""
from setuptools import setup, find_packages

setup(name='noisify',
      version='1.0',
      description='Framework for creating synthetic data with realistic errors for refining data science pipelines.',
      url='',
      author='Declan Crew',
      author_email='dcrew@dstl.gov.uk',
      license='MIT',
      packages=find_packages(),
      install_requires=[],
      test_suite='noisify.tests',
      test_requires=['numpy', 'Pillow', 'pandas'])
