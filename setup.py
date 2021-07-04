from setuptools import setup

setup(name='diplomacy-messenger',
      version='0.1',
      description='Messenger bot for WebDiplomacy',
      url='http://github.com/Bazzas-Personal-Stuff/diplomacy-messenger/',
      author='Bailey Gibbons',
      install_requires=[
            'bs4',
            'requests',
            'discord',
            'python-dotenv'
      ],
      zip_safe=False)

