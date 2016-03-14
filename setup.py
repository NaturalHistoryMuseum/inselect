#!/usr/bin/env python
import sys

import inselect

# Generic setup data used for both the distutils setup and the cx_Freeze setup.
# win32.extra_packages and win32.include_files indicate extra packages/files
# that are not automatically detected by cx_Freeze. If running into problems,
# try including the whole of numpy/scipy.

SCRIPTS = ('export_metadata', 'ingest', 'read_barcodes', 'save_crops', 'segment')

setup_data = {
    'name': 'inselect',
    'version': inselect.__version__,
    'maintainer': 'Lawrence Hudson',
    'maintainer_email': 'l.hudson@nhm.ac.uk',
    'url': 'https://github.com/NaturalHistoryMuseum/inselect/',
    'description': inselect.__doc__,
    'packages': ['inselect', 'inselect.gui.plugins', 'inselect.gui.views',
                 'inselect.gui.views.boxes', 'inselect.lib',
                 'inselect.lib.templates', 'inselect.scripts'],
    'test_suite': 'inselect.tests',
    'scripts': ['inselect/scripts/{0}.py'.format(script) for script in SCRIPTS],
    'install_requires': open('requirements.txt').readlines(),
    'entry_points': {
        'console_scripts': [
            'inselect = inselect.app:launch'
        ]
    },
    'win32': {
        'executables': [
            {
                'script': 'inselect.py',
                'targetName': 'inselect.exe',
                'icon': 'data/inselect.ico',
                'base': 'Win32GUI',
                'shortcutName': 'Inselect',     # See http://stackoverflow.com/a/15736406
                'shortcutDir': 'ProgramMenuFolder'
            }
        ] + [
            {
                'script': 'inselect/scripts/{0}.py'.format(script),
                'targetName': '{0}.exe'.format(script),
                'icon': 'data/inselect.ico',
                'base': 'Console'
            }
            for script in SCRIPTS
        ],
        'include_files': [
            ('{site_packages}/numpy', 'numpy'),
        ],
        'extra_packages': ['win32com.gen_py'],
        'excludes': [
            'Tkinter', 'ttk', 'Tkconstants', 'tcl',
            'future.moves'    # Errors from urllib otherwise
        ]
    }
}


def distutils_setup():
    """disttutils setup"""
    from distutils.core import setup

    setup(
        name=setup_data['name'],
        version=setup_data['version'],
        packages=setup_data['packages'],
        scripts=setup_data['scripts'],
        maintainer=setup_data['maintainer'],
        maintainer_email=setup_data['maintainer_email'],
        url=setup_data['url'],
    )


def cx_setup():
    """cx_Freeze setup. Used for building Windows installers"""
    from cx_Freeze import setup, Executable
    from distutils.sysconfig import get_python_lib

    # Set path to include files
    site_packages = get_python_lib()
    include_files = []
    for i in setup_data['win32']['include_files']:
        include_files.append((
            i[0].format(site_packages=site_packages),
            i[1]
        ))

    # Setup
    setup(
        name=setup_data['name'],
        version=setup_data['version'],
        options={
            'build_exe': {
                'packages': setup_data['packages'] + setup_data['win32']['extra_packages'],
                'excludes': setup_data['win32']['excludes'],
                'include_files': include_files,
            },
            'bdist_msi': {
                'upgrade_code': '{fe2ed61d-cd5e-45bb-9d16-146f725e522f}'
            }
        },
        executables=[Executable(**i) for i in setup_data['win32']['executables']]
    )


# User cx_Freeze to build Windows installers, and distutils otherwise.
if 'bdist_msi' in sys.argv:
    cx_setup()
else:
    distutils_setup()
