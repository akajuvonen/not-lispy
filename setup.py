from setuptools import setup, find_packages


setup(
    name='not-lispy',
    version='0.2.0',
    description='A Lisp interpreter in Python',
    author='Antti Juvonen',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['click', 'attrs'])
