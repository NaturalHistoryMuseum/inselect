import sys

# Generic setup data used for both the distutils setup and the cx_Freeze setup.
# win32.extra_packages and win32.include_files indicate extra packages/files that are
# not automatically detected by cx_Freeze. If running into problems, try including the whole
# of numpy/scipy.
setup_data = {
    'name': 'inselect',
    'version': '0.1',
    'packages': ['inselect'],
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
                'icon': 'data\inselect.ico',
                'base': 'Win32GUI',
                'shortcutName': 'Inselect', # See http://stackoverflow.com/questions/15734703/use-cx-freeze-to-create-an-msi-that-adds-a-shortcut-to-the-desktop
                'shortcutDir': 'ProgramMenuFolder'
            },
            {
                'script': 'inselect.py',
                'targetName': 'inselect_cli.exe',
                'icon': 'data\inselect.ico',
                'base': 'Console'
            },
        ],
        'extra_packages': [
            'matplotlib.backends.backend_qt4agg',
#            'scipy.special._ufuncs_cxx',
#            'scipy.sparse.csgraph._validation',
#            'scipy.integrate.vode',
#            'scipy.integrate.lsoda'
        ],
        'include_files': [
            (r'{site_packages}\skimage', 'skimage'),
#            (r'{site_packages}\numpy\core\libifcoremd.dll', 'libifcoremd.dll'),
#            (r'{site_packages}\numpy\core\libmmd.dll', 'libmmd.dll')
            (r'{site_packages}\numpy', 'numpy'),
            (r'{site_packages}\scipy', 'scipy')
        ],
        'excludes': ['Tkinter', 'ttk', 'Tkconstants', 'tcl']
    }
}


def distutils_setup():
    """disttutils setup"""
    from distutils.core import setup

    with open('requirements.txt') as f:
        required = f.read().splitlines()

    setup(
        name=setup_data['name'],
        version=setup_data['version'],
        packages=setup_data['packages'],
        entry_points=setup_data['entry_points'],
        install_requires=required
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
                'icon': 'data\inselect.ico'
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