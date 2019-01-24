from setuptools import setup, find_packages

setup(name='sigyn',
      version='0.2',
      description='Framework for creating synthetic data with realistic errors for refining data science pipelines.',
      url='',
      author='Declan Crew',
      author_email='dcrew@dstl.gov.uk',
      license='MIT',
      packages=find_packages(),
      install_requires=[],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
