from setuptools import setup
from setuptools import find_packages

setup(
    name='labtoys',
    version='0.3.4',
    description='Package for use with laboratory equipment',
    author='Pawel Pudo',
    author_email='ppudo@outlook.com',
    url='https://github.com/ppudo/labtoys_python.git',
    install_requires=[ 'pywin32==221' ],
    packages=find_packages(),
    keywords=['scpi', 'rigol', 'ds1000z', 'delta elektronika', 'psc_eth', 'cts', 'ascii-protokolls',
                'keysight', 'daq', '34972A', 'tektrinix', 'mso5', 'CANoe' ],
    license='MIT'
)
