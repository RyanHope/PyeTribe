from setuptools import setup
import os.path

__version__ = '0.1.0'

descr_file = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='pyetribe',
    version=__version__,
    
    packages=['pyetribe'],

    description='A package for communicating with EyeTribe eye trackers.',
    long_description=open(descr_file).read(),
    author='Ryan Hope',
    author_email='rmh3093@gmail.com',
    url='https://github.com/RyanHope/PyeTribe',
    classifiers=[
				'License :: OSI Approved :: GNU General Public License (GPL)',
				'Framework :: Twisted',
				'Programming Language :: Python :: 3',
				'Topic :: Scientific/Engineering',
				'Topic :: Utilities'
    ],
	license='GPL-3',
	install_requires=[
					'panglery',
					'twisted'
	],
 )
