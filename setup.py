from setuptools import setup

long_description = 'Python package for using bokeh in Apache Zeppelin Notebook'

REQUIRES = [
      'bokeh >=0.12.7'
]

setup(name='bkzep',
      packages=['bkzep'],
      version='0.6.1',
      description='Python package for using bokeh in Apache Zeppelin Notebook',
      long_description=long_description,
      install_requires=REQUIRES,
      url='https://github.com/zjffdu/bkzep',
      author='Jeff Zhang',
      author_email='zjffdu@apache.org',
      license='Apache Licence V2.0')
