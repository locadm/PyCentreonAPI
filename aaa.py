from setuptools import setup, find_packages

setup(
    name='PyCentreonAPI',
    version='0.2.1',
    packages=find_packages(),
    entry_points='''
        [console_scripts]
    ''',
    license="BSD",  # TODO change the license
    classifiers=[
    ],
    install_requires=[
        "requests",
    ],
    tests_require=[
    ],
)
