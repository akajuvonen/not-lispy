from setuptools import setup, find_packages


setup(
    name='not-lispy',
    version='0.10.0',
    description='A Lisp interpreter in Python',
    author='Antti Juvonen',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['click', 'attrs'],
    entry_points='''
    [console_scripts]
    notlispy-repl=not_lispy:repl
    notlispy=not_lispy.lisp:execute
    ''')
