from setuptools import setup

setup(
   name='Basic Tor Command-Line Client',
   version='1.0',
   description='A command-line client to download files through Tor and HTTP',
   author='Lars Wallenborn',
   author_email='lars@wallenborn.net',
   packages=['tor-get'],
   install_requires=['requests', 'requests[socks]'],
)
