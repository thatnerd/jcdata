from distutils.core import setup

# setup.py syntax - https://docs.python.org/2/distutils/setupscript.html


# Running setup.py from PyCharm - https://www.jetbrains.com/help/pycharm/2016.1/creating-and-running-setup-py.html
# Package setup - https://docs.python.org/2/distutils/examples.html
## Whether to use specific modules or packages - http://programmers.stackexchange.com/questions/243044/single-python-file-distribution-module-or-package

# Installing packages - https://docs.python.org/2/install/

# For uploading to PyPl - https://docs.python.org/2/distutils/packageindex.html

# Specifying project dependencies:
## http://python-packaging.readthedocs.io/en/latest/dependencies.html
## https://packaging.python.org/requirements/

setup(
    name='JCData',
    version='0.0.1',
#    py_modules=['Mod123'],
#    url='https://github.com/abcd',
#    license='MIT',
#    author='abc',
#    author_email='abc@gmail.com',
    description='JC Sewer Data',
    install_requires=[
        'docopt',
        'pymongo'
    ]
)
