import os
import setuptools

try:
    with open('README.md', 'rb') as handle:
        description = handle.read()
except IOError as e:
    print('Failed to read README file: {}'.format(e))
    exit(1)

def ReadRequirements(path):
    requirements = []
    if os.path.isfile(path):
        with open(path, encoding='utf-8') as handle:
            for line in handle:
                line = line.strip()
                if len(line) > 0 and not line.startswith('#'):
                    requirements.append(line)
    return requirements

# Packaging tutorial: https://packaging.python.org/tutorials/packaging-projects/
# Package classifiers: https://pypi.org/classifiers/

setuptools.setup(
    name='PyMonitorLib',
    version='0.4.1',
    author='Daniel Weiner',
    author_email='info@phantomnet.net',
    description='Library for creating simple interval processes. This is especially '
                'useful for interval based monitoring application that generate '
                'telemetry at a set interval.',
    long_description=description.decode('utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/Aralocke/PyMonitorLib',
    packages=setuptools.find_packages(),
    install_requires=ReadRequirements('requirements.txt'),
    extras_require={'dev': ReadRequirements('dev-requirements.txt')},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
