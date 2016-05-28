# coding=utf-8
"""User prompts
"""

import sys


BOXES_VIEW_TIP = ('Right click + drag to create box  |  '
                  'CTRL + N / P to move between boxes  |  '
                  'SHIFT / ALT + arrow keys to adjust selected box')

OBJECTS_VIEW_TIP = ('CTRL + N / P or arrow keys to move between objects  |  '
                    'CTRL + G to show objects in a grid  |  '
                    'CTRL + E to view a single object expanded')

if 'darwin' == sys.platform:
    # Replace 'CTRL' with the Apple command key
    def command_key(msg):
        return msg.replace('CTRL', u'⌘')
    BOXES_VIEW_TIP = command_key(BOXES_VIEW_TIP)
    OBJECTS_VIEW_TIP = command_key(OBJECTS_VIEW_TIP)
