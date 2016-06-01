# coding=utf-8
"""User prompts
"""

import sys


BOXES_VIEW_SHORTCUTS = [
    ('Create box', 'Right click & drag'),
    ('Move selected boxes', 'Arrow keys'),
    ('Adjust selected box', 'Shift / Alt+arrow keys'),
    ('Move between boxes', 'Ctrl+N / P'),
    ('Zoom', 'Ctrl+mouse wheel / trackpad swipe'),
]

BOXES_VIEW_TIP = ('Right click + drag to create box  |  '
                  'CTRL + N / P to move between boxes  |  '
                  'SHIFT / ALT + arrow keys to adjust selected box')

OBJECTS_VIEW_TIP = ('CTRL + N / P or arrow keys to move between objects  |  '
                    'CTRL + G to show objects in a grid  |  '
                    'CTRL + E to view a single object expanded')


def _format_action_shortcuts(action):
    return u' / '.join(s.toString() for s in action.shortcuts())


if 'darwin' == sys.platform:
    # Replace 'Ctrl' with the Apple command key
    def command_key(msg):
        return msg.replace('Ctrl', u'⌘')
    BOXES_VIEW_SHORTCUTS = [
        (text, command_key(shortcut)) for text, shortcut in BOXES_VIEW_SHORTCUTS
    ]
    BOXES_VIEW_TIP = command_key(BOXES_VIEW_TIP)
    OBJECTS_VIEW_TIP = command_key(OBJECTS_VIEW_TIP)

    def format_action_shortcuts(action):
        return command_key(_format_action_shortcuts(action))

else:
    format_action_shortcuts = _format_action_shortcuts
