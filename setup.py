from setuptools import setup
from staticflatpages import __version__

setup(
    name='django-staticflatpages',
    version=__version__,
    description="like flatpages, but with templates.",
    long_description=open('README.rst').read(),
    author='Brad Montgomery',
    author_email='brad@bradmontgomery.net',
    url='https://github.com/bradmontgomery/django-staticflatpages',
    license='MIT',
    packages=['staticflatpages'],
    include_package_data=True,
    package_data={'': ['README.rst']},
    zip_safe=False,
    install_requires=['django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
