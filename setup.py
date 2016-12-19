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
            'PyQt5>=5.6.0'
        ],
        'barcodes': ['gouda>=0.1.11', 'pylibdmtx>=0.1.5', 'pyzbar>=0.1.3'],
        'windows': ['pywin32>=220'],
        'development': ['coveralls>=1.1', 'mock>=2.0.0', 'nose>=1.3.7'],
    },
    'entry_points': {
        'gui_scripts':
            ['inselect = inselect.gui.app:main'],
        'console_scripts':
            ['{0} = inselect.scripts.{0}:main'.format(script) for script in SCRIPTS],
    },
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
        'Programming Language :: Python :: 3.5',
    ],
}


def setuptools_setup():
    """setuptools setup"""
    from setuptools import setup
    setup(**setup_data)


def _qt_files(site_packages):
    """Returns a list of tuples (src, dest) of Qt dependencies to be installed.
    Elements are instances of Path.
    site_packages should be an instance of Path to the site-packages directory.

    IF we leave cx_Freeze to do its thing then the entirety of PyQt5, Qt5 and
    uic are included in the installer. The only way to avoid horrible bloat is
    to hand-tune which files we include.

    This whole system is fucked beyond belief.
    """
    from pathlib import Path

    return [
        # Qt DLLs
        (
            site_packages.joinpath('PyQt5/Qt/bin').joinpath(dep),
            dep
        )
        for dep in ('Qt5Core.dll', 'Qt5Gui.dll', 'Qt5Widgets.dll')
    ] + [
        # Qt plugins
        (
            site_packages.joinpath('PyQt5/Qt/plugins/platforms').joinpath(dep),
            Path('platforms').joinpath(dep)
        )
        for dep in ('qwindows.dll',)
    ] + [
        # PyQt extension modules
        (
            site_packages.joinpath('PyQt5').joinpath(dep),
            Path('PyQt5').joinpath(dep)
        )
        for dep in ('__init__.py', 'Qt.pyd', 'QtCore.pyd', 'QtGui.pyd', 'QtWidgets.pyd')
    ]


def cx_setup():
    """cx_Freeze setup. Used for building Windows installers"""
    import scipy

    from pathlib import Path
    from distutils.sysconfig import get_python_lib

    from cx_Freeze import setup, Executable

    from pylibdmtx import pylibdmtx
    from pyzbar import pyzbar

    # Useful paths
    environment_root = Path(sys.executable).parent
    site_packages = Path(get_python_lib())
    project_root = Path(__file__).parent

    # Files as tuples (source, dest)
    include_files = [
        # Evil, evil, evil
        # cx_Freeze breaks pywintypes and pythoncom on Python 3.5
        # https://bitbucket.org/anthony_tuininga/cx_freeze/issues/194/error-with-frozen-executable-using-35-and
        (site_packages.joinpath('win32/lib/pywintypes.py'), 'pywintypes.py'),
        (site_packages.joinpath('pythoncom.py'), 'pythoncom.py'),

        # Binary dependencies that are not detected
        (environment_root.joinpath('Library/bin/mkl_core.dll'), 'mkl_core.dll'),
        (environment_root.joinpath('Library/bin/mkl_intel_thread.dll'), 'mkl_intel_thread.dll'),
        (environment_root.joinpath('Library/bin/libiomp5md.dll'), 'libiomp5md.dll'),

        # Stylesheet
        (project_root.joinpath('inselect/gui/inselect.qss'), 'inselect.qss'),
    ] + [
        # DLLs that are not detected because they are loaded by ctypes
        (dep._name, Path(dep._name).name)
        for dep in pylibdmtx.EXTERNAL_DEPENDENCIES + pyzbar.EXTERNAL_DEPENDENCIES
    ] + _qt_files(site_packages)

    # Convert instances of Path to strs
    include_files = [(str(source), str(dest)) for source, dest in include_files]

    # Directories as strings
    include_files += [
        # Fixes scipy freeze
        # http://stackoverflow.com/a/32822431/1773758
        str(Path(scipy.__file__).parent),
    ]

    # Packages to exclude.
    exclude_packages = [
        str(p.relative_to(site_packages)).replace('\\', '.') for p in
        site_packages.rglob('*/tests')
    ]

    setup(
        name=setup_data['name'],
        version=setup_data['version'],
        options={
            'build_exe': {
                'packages':
                    setup_data.get('packages', []) + [
                        'sklearn.neighbors', 'win32com.gen_py', 'win32timezone',
                    ],
                'excludes': [
                    # '_bz2',    # Required by sklearn
                    '_decimal', '_elementtree', '_hashlib', '_lzma',
                    '_ssl', 'curses',
                    'distutils', 'email', 'http', 'lib2to3', 'mock', 'nose',
                    'PyQt5',
                    # 'pydoc',    # Required by sklearn
                    'tcl', 'Tkinter', 'ttk', 'Tkconstants',
                    # 'unittest',    # Required by numpy.core.multiarray
                    'win32com.HTML', 'win32com.test', 'win32evtlog', 'win32pdh',
                    'win32trace', 'win32wnet',
                    'xml', 'xmlrpc',
                    'inselect.tests',
                ] + exclude_packages,
                'includes': [
                ],
                'include_files': include_files,
                'include_msvcr': True,
                'optimize': 2,
            },
            'bdist_msi': {
                'upgrade_code': '{fe2ed61d-cd5e-45bb-9d16-146f725e522f}'
            }
        },
        executables=[
            Executable(
                script='inselect/scripts/inselect.py',
                targetName='inselect.exe',
                icon='icons/inselect.ico',
                base='Win32GUI',
                shortcutName='Inselect',     # See http://stackoverflow.com/a/15736406
                shortcutDir='ProgramMenuFolder'
            )
        ] + [
            Executable(
                script='inselect/scripts/{0}.py'.format(script),
                targetName='{0}.exe'.format(script),
                icon='icons/inselect.ico',
                base='Console'
            )
            for script in SCRIPTS
        ],
    )


if (3, 5) <= sys.version_info:
    if 'bdist_msi' in sys.argv:
        cx_setup()
    else:
        setuptools_setup()
else:
    sys.exit('Only Python >= 3.5 is supported')
