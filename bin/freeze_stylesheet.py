"""Freezes inselect.qss into inselect/gui/frozen_stylesheet.py
"""

TEMPLATE = '''"""Frozen from inselect.qss
"""

STYLESHEET = """
{0}
"""
'''

with open('data/inselect.qss') as infile:
    with open('inselect/gui/frozen_stylesheet.py', 'w') as outfile:
        outfile.write(TEMPLATE.format(infile.read()))
