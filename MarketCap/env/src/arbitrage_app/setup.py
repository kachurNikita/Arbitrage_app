from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Market_app',
    scripts=['main.py', 'test_arbitrage_app.py'],
    version='1.0',
    description='Simple Market app',
    author='Kachur Nikita',
    author_email='ashtonashtonkachur@gmail.com',
    install_requires = requirements
)   