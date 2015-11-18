
from setuptools import setup

setup(name='btm',
    description='The software to power a Bitcoin \
    ATM that does not need to be serviced nor \
    need to be connected to an exchange',
    url='https://github.com/cjduncana/Unbanked-Bitcoin-ATM',
    packages=['btm', 'btm/models'],
    zip_safe=False,
    classifiers=[
    	'Development Status :: 1 - Planning',
    	'License :: OSI Approved :: \
    	GNU General Public License v2 (GPLv2)',
    	'Natural Language :: English',
    	'Programming Language :: Python :: 2.7'
    ],
    test_suite='nose2.collector.collector',)
