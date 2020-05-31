
import setuptools

import ylog

try:
    import importlib
except ImportError:
    install_requires.append('importlib')  # Python 2.6 compatibility

setuptools.setup(
    name='ylogx',
    version=ylog.VERSION,
    author='Niklas Andersson',
    author_email='nandersson900@gmail.com',
    description=('ylog is a versatile yet minimalistic Python '
                 'logging client for cloud and on-prem environments'),
    license='LGPL',
    url='https://github.com/Niklas9/ylog',
    zip_safe=False,
    install_requires=[],
    tests_require=[
        'nose==1.3.7',
        'coverage==5.1'
    ],
    packages=['ylog'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha'
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python'
        'Programming Language :: Python :: 2'
        'Programming Language :: Python :: 2.6'
        'Programming Language :: Python :: 2.7'
        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3.4'
        'Programming Language :: Python :: 3.5'
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X'
    ],
)
