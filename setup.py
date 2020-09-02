from os import path
from setuptools import find_packages, setup


current_dir = path.abspath(path.dirname(__file__))
with open(path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='find-gcp-keys',
    author='Denis Loginov',
    description='Find and report valid Google Service Account keys on your filesystem',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='BSD 3-clause "New" or "Revised" License',
    url='https://github.com/dinvlad/find-gcp-keys',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Utilities',
    ],
    python_requires='>=3.7.0',
    packages=find_packages(
        exclude=[
            'tests',
        ],
    ),
    setup_requires=[
        'setuptools_scm',
    ],
    use_scm_version={
        'root': '.',
        'relative_to': __file__,
    },
    install_requires=[
        'google-auth >= 1.21.0',
    ],
    entry_points={
        'console_scripts': [
            'find-gcp-keys = find_gcp_keys.__main__:main',
        ],
    },
)
