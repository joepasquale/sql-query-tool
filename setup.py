from distutils.core import setup

setup(
    name='SQL Query Tool',
    version='1.0.0',
    packages=['app',],
    license='MIT License',
    author='Joe Pasquale',
    install_requires = ['pyodbc','flask','waitress']
)
