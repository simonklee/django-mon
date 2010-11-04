from distutils.core import setup
import os

setup(
    name = 'django-mon',
    packages = ['mon'],
    version='0.1.0',
    description='django-app to monitor sensor data',
    long_description=open('README').read(),
    author='Simon Zimmermann',
    author_email='simonz05@gmail.com',
    url='http://github.com/simonz05/django-mon',
    install_requires=[],
    license='GPL',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
