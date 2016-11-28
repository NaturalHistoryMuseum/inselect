"""PyInstaller runtime hook to set the version of the interface to Qt

https://github.com/pyinstaller/pyinstaller/wiki/Recipe-PyQt4-API-Version
"""

import sip


VERSION = 2

sip.setapi(u'QDate', VERSION)
sip.setapi(u'QDateTime', VERSION)
sip.setapi(u'QString', VERSION)
sip.setapi(u'QTextStream', VERSION)
sip.setapi(u'QTime', VERSION)
sip.setapi(u'QUrl', VERSION)
sip.setapi(u'QVariant', VERSION)
