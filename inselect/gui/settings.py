"""Settings
"""

from PySide.QtCore import QCoreApplication, QDir, QSettings

# TODO LH Old keys - should probably be removed
# s = QSettings()
# for key in ['about_text', 'annotation_fields', 'about_label', 'icon_size',
#             'label_field', 'export_template']:
#     s.remove(key)

def working_dir():
    # TODO LH Check this logic
    s = QSettings()
    if 'win32' == sys.platform:
        return s.value('working_directory', QCoreApplication.applicationDirPath())
    else:
        return s.value('working_directory', QDir.currentPath())
