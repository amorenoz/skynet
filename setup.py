from setuptools import setup

LONG_DESC = """ Skynet
Skynet is a command line tool that interacts with skydive to ease
debugging and troubleshooting OVN / OVS networks

Under heavy development
"""

setup(name='skynet',
      version='0.1.0',
      description='OVN/OVS Network Visibility tool based on Skydive',
      maintainer='Adrián Moreno',
      maintainer_email='amorenoz@redhat.com',
      packages=['skynet'],
      url='https://gitlab.cee.redhat.com/amorenoz/skynet',
      long_description=LONG_DESC,
      license=["Apache License 2.0"],
      scripts=['bin/skynet'],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Networking',
      ])
