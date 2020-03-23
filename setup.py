"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import re


# Always prefer setuptools over distutils
from setuptools import setup


# Get the long description from the README file
with open("README.md") as f:
    long_description = f.read()


with open("covid/_version.py", "r") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)


setup(
    name='kaggle-covid19-global-forecasting-week-1',
    url='https://github.com/sof38/kaggle-covid19-global-forecasting-week-1',
    author='Sofiane Soussi',
    author_email='sofiane.soussi@gmail.com',
    version=version,
    description="Exploring data from Kaggle competition https://www.kaggle.com/c/covid19-global-forecasting-week-1/",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7.0',
    packages=[
        "covid"
    ],
    install_requires=[]
)
