from setuptools import setup, find_packages

import os

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-assetbuilding',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Provides tools to build assets',
    long_description='Please read the README.md file!',
    url='http://projects.it.hs-hannover.de/',
    author='Tim Fechner',
    author_email='tim.fechner@hs-hannover.de',
    zip_safe=False,
    install_requires=[
        'libsass==0.13.3',
        'jsmin==2.2.2',
        'watchdog==0.8.3'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3.x',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
