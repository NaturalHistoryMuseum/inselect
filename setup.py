from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='inselect',
    version='0.1',
    packages=['inselect'],
    entry_points = {
        'console_scripts': [
            'inselect = inselect.app:launch'
        ]
    },
    install_requires=required
)
