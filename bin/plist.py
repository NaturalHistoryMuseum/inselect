#!/usr/bin/env python3
"""Alter Inselect's existing plist file
"""

# https://developer.apple.com/library/mac/documentation/Carbon/Conceptual/LaunchServicesConcepts/LSCConcepts/LSCConcepts.html#//apple_ref/doc/uid/TP30000999-CH202-CIHHEGGE

import plistlib
import sys

import inselect
plist = plistlib.readPlist(sys.argv[1])
plist['CFBundleShortVersionString'] = inselect.__version__
plist['CFBundleDisplayName'] = 'Inselect'
plist['CFBundleDocumentTypes'] = [{
    'CFBundleTypeName': 'Inselect document',
    'CFBundleTypeIconFile': 'inselect.icns',
    'CFBundleTypeExtensions': ['inselect'],
    'CFBundleTypeRole': 'Editor',
    'LSTypeIsPackage': 'False',
}]

plistlib.writePlist(plist, sys.argv[1])
