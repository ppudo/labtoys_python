from setuptools import setup
from setuptools import find_packages

setup(
    name='labtoys',
    version='0.2.1',
    description='Package for use with laboratory equipment',
    author='Pawel Pudo',
    author_email='ppudo@outlook.com',
    url='https://github.com/ppudo/labtoys_python.git',
    install_requires=[],
    packages=find_packages(),
    keywords=['scpi', 'rigol', 'ds1000z', 'delta elektronika', 'psc_eth' ],
    license='MIT'
)
