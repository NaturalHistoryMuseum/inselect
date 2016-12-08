#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import inselect


REQUIREMENTS = [
    # TODO How to specify OpenCV? 'cv2>=3.1.0',
    'numpy>=1.11.1,<1.12',
    'Pillow>=3.4.2,<3.5',
    'python-dateutil>=2.6.0,<2.7',
    'pytz>=2016.7',
    'PyYAML>=3.12,<3.2',
    'schematics>=1.1.1,<1.2',
    'scikit-learn>=0.18.1,<0.19',
    'scipy>=0.18.1,<0.19',
    'unicodecsv>=0.14.1,<0.15',
]


SCRIPTS = ('export_metadata', 'ingest', 'read_barcodes', 'save_crops', 'segment')


setup_data = {
    'name': 'inselect',
    'version': inselect.__version__,
    'author': (u'Lawrence Hudson, Alice Heaton, Pieter Holtzhausen, '
               u'Stéfan van der Walt'),
    'author_email': 'l.hudson@nhm.ac.uk',
    'maintainer': 'Lawrence Hudson',
    'maintainer_email': 'l.hudson@nhm.ac.uk',
    'url': 'https://github.com/NaturalHistoryMuseum/inselect/',
    'license': 'Modified BSD',
    'description': inselect.__doc__,
    'long_description': inselect.__doc__,
    'packages': [
        'inselect', 'inselect.gui', 'inselect.gui.plugins',
        'inselect.gui.views', 'inselect.gui.views.boxes', 'inselect.lib',
        'inselect.lib.templates', 'inselect.scripts',
    ],
    'include_package_data': True,
    'test_suite': 'inselect.tests',
    'scripts': ['inselect/scripts/{0}.py'.format(script) for script in SCRIPTS],
    'install_requires': REQUIREMENTS,
    'extras_require': {
        'gui': [
            'ExifRead>=2.1.2', 'humanize>=0.5.1', 'psutil>=5.0.0',
            'QtPy>=1.1.2', 'PyQt>=5.6.0'
        ],
        'barcodes': ['gouda>=0.1.11', 'pylibdmtx>=0.1.5', 'pyzbar>=0.1.3'],
        'windows': ['pywin32>=220'],
        'development': ['coveralls>=1.1', 'mock>=2.0.0', 'nose>=1.3.7'],
    },
    'entry_points': {
        'gui_scripts':
            ['inselect = inselect.app:main'],
        'console_scripts':
            ['{0} = inselect.scripts.{0}:main'.format(script) for script in SCRIPTS],
    },
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
        'Programming Language :: Python :: 3.5',
    ],
    'win32': {
        'executables': [
            {
                'script': 'inselect.scripts.inselect.py',
                'targetName': 'inselect.exe',
                'icon': 'icons/inselect.ico',
                'base': 'Win32GUI',
                'shortcutName': 'Inselect',     # See http://stackoverflow.com/a/15736406
                'shortcutDir': 'ProgramMenuFolder'
            }
        ] + [
            {
                'script': 'inselect/scripts/{0}.py'.format(script),
                'targetName': '{0}.exe'.format(script),
                'icon': 'icons/inselect.ico',
                'base': 'Console'
            }
            for script in SCRIPTS
        ],
        # Strings in braces within 'include_files' tuples expanded in cx_setup
        'include_files': [
            ('{environment_root}/Library/bin/mkl_core.dll', 'mkl_core.dll'),
            ('{environment_root}/Library/bin/mkl_intel_thread.dll', 'mkl_intel_thread.dll'),
            ('{environment_root}/Library/bin/libiomp5md.dll', 'libiomp5md.dll'),
            ('{project_root}/inselect/inselect.qss', 'inselect.qss'),
        ],
        'extra_packages': ['win32com.gen_py'],
        'excludes': [
            'Tkinter', 'ttk', 'Tkconstants', 'tcl', '_ssl',
        ]
    }
}


def setuptools_setup():
    """setuptools setup"""
    from setuptools import setup
    setup(**setup_data)


def cx_freeze_setup():
    """cx_Freeze setup. Used for building installers for Mac OS X and for
    Windows
    """
    from itertools import chain
    from pathlib import Path

    from cx_Freeze import setup, Executable

    from pylibdmtx import pylibdmtx
    from pyzbar import pyzbar

    # Dependencies that are not automatically detected
    include_files = [
        # (str(Path(sys.executable).parent.joinpath('Library/bin/mkl_core.dll')), 'mkl_core.dll'),
        # (str( Library/bin/libiomp5md.dll')), 'libiomp5md.dll'),
        (str(Path(__file__).parent.joinpath('inselect/inselect.qss')), 'inselect.qss'),
    ] + [
        # DLLs that are not detected because they are loaded by ctypes
        (dep._name, Path(dep._name).name)
        for dep in chain(
            pylibdmtx.EXTERNAL_DEPENDENCIES, pyzbar.EXTERNAL_DEPENDENCIES
        )
    ]

    # scipy
    # http://stackoverflow.com/questions/32694052/scipy-and-cx-freeze-error-importing-scipy-you-cannot-import-scipy-while-being
    import scipy
    include_files += [
        str(Path(scipy.__file__).parent),
    ]

    # Setup
#    from pprint import pprint
    setup(
        name=setup_data['name'],
        version=setup_data['version'],
        description=setup_data['description'],
        options={
            'build_exe': {
                'packages': (
                    setup_data['packages'] +
                    (['win32com.gen_py'] if sys.platform == 'win32' else [])
                ),
                'excludes': [
                    'Tkinter', 'ttk', 'Tkconstants', 'tcl', '_ssl',
                    'setuptools', 'pkg_resources',
                ],
                'bin_excludes': [
                    'libqtaudio_coreaudio.dylib',
                ],
                'bin_path_excludes': [
                    '/Library/Frameworks/Python.framework/',
                    str(Path(sys.executable).parent.parent.joinpath('site-packages/setuptools-27.2.0-py3.5.egg/pkg_resources')),
                ] + [
                    str(Path(sys.executable).parent.parent.joinpath('lib', '{0}.framework'.format(section)))
                    for section in ('QtCore', 'QtGui', 'QtNetwork', 'QtOpenGL', 'QtWidgets', 'QtSql', 'QtSvg', 'QtTest', 'QtXml', 'QtDBus', 'QtPrintSupport')
                ],
                'include_files': include_files,
                'include_msvcr': sys.platform == 'win32',
                'optimize': 2,
            },
            'bdist_msi': {
                'upgrade_code': '{fe2ed61d-cd5e-45bb-9d16-146f725e522f}',
            }
        },
        executables=[
            Executable(**exe) for exe in [{
                'script': 'inselect.scripts.inselect.py',
                'targetName': 'inselect.exe',
                'icon': 'icons/inselect.ico',
                'base': 'Win32GUI' if sys.platform == 'win32' else None,
                'shortcutName': 'Inselect',     # See http://stackoverflow.com/a/15736406
                'shortcutDir': 'ProgramMenuFolder',
            }] + [
                {
                    'script': 'inselect/scripts/{0}.py'.format(script),
                    'targetName': '{0}.exe'.format(script),
                }
                for script in SCRIPTS
            ]
        ],
    )


if (3, 5) <= sys.version_info:
    if 'bdist_msi' in sys.argv or 'bdist_dmg' in sys.argv or 'bdist_mac' in sys.argv:
        cx_freeze_setup()
    else:
        setuptools_setup()
else:
    sys.exit('Only Python >= 3.5 is supported')
