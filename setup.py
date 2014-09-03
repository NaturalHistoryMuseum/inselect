from distutils.core import setup

setup(
    name='inselect',
    version='0.1',
    packages=['inselect'],
    entry_points = {
        'console_scripts': [
            'inselect = inselect.app:launch'
        ]
    },
    install_requires = [
        'numpy>=1.6',
        'six>=1.7.3',
        'scikit-image>=0.10',
        'matplotlib>=1.0',
        'pyside>=1.2',
        'scipy>=0.14.0'
    ]
)
