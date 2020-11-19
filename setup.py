import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='ei',
    version='0.0.3',
    author='Yuankui Lee',
    author_email='toregnerate@gmail.com',
    description='Embedding IPython for debugging',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/djosix/ei',
    packages=['ei'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
