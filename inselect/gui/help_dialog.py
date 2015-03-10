from PySide import QtCore, QtGui
from inselect import __version__ as inselect_version
_help = """
    <h1>Inselect {version}</h1>
    <h2>Usage</h2>

    <p>Inselect is an application designed to help in identifying insects in an
    insect tray. To get started, open an image using <em>Open Image</em>, and
    segment it using <em>Segment</em>. You can then add/remove individual
    segments, modify the position and size of each segments, and annotate the
    segments (see the <em>navigation</em> instructions below).</p>

    <p>You can re-segment difficult areas by providing hints: select a segment
    that contains more than one insect, hold down the <em>shift</em> key, and
    click on the center of each insect. Once done, click on <em>Segment</em>
    again. It will re-segment that particular area with the given hints.</p>

    <p>Once you have segmented and annotated a tray, you can save that
    information by doing <em>Save Boxes</em>. Alternatively you can save the
    individual segment images as well as the annotation information by doing
    <em>Export Images</em></p>

    <h2>Mouse and keyboard shortcuts</h2>
    <h3>Application shortcuts</h3>
    <ul>
        <li><strong>Ctrl+O</strong>:Open Image</li>
        <li><strong>Ctrl+S</strong>:Export segment data</li>
        <li><strong>Ctrl+I</strong>:Import segment data</li>
        <li><strong>F5</strong>:Segment scene or re-segment selected segment</li>
        <li><strong>F3</strong>:Display segmentation</li>
        <li><strong>Ctrl+A</strong>:Select all segments</li>
        <li><strong>Ctrl++</strong>:Zoom in</li>
        <li><strong>Ctrl+-</strong>:Zoom out</li>
        <li><strong>Alt+F4</strong>:Exit</li>
    </ul>
    <h3>Keyboard segment navigation and edition</h3>
    <ul>
        <li><strong>n</strong>:Next segment</li>
        <li><strong>p</strong>:Previous segment</li>
        <li><strong>z</strong>:Zoom to selection</li>
        <li><strong>Up/Down/Right/Left</strong>:Move selected segments</li>
        <li><strong>Ctrl+Up/Down/Right/Left</strong>:Move selected segment's top left corner</li>
        <li><strong>Shift+Up/Down/Right/Left</strong>:Move selected segment's bottom right corner</li>
        <li><strong>Enter</strong>:Open annotation dialog for selected segments</li>
    </ul>
    <h3>Mouse segment navigation and edition</h3>
    <ul>
        <li><strong>Left click</strong>: Select segment</li>
        <li><strong>Left click and drag</strong>: Select multiple segments by area</li>
        <li><strong>Shift+Left click</strong>: Add seeds in selected segment for re-segmentation</li>
        <li><strong>Right click and drag</strong>: Create new segment</li>
        <li><strong>Middle click and drag</strong>: Pan the view</li>
        <li><strong>Double click</strong>: Open annotation dialog</li>
        <li><strong>Wheel</strong>: Vertical scroll</li>
        <li><strong>Shift+Wheel</strong>: Zoom</li>
    </ul>
    <h3>Keyboard shortcuts in annotation dialog</h3>
    <ul>
        <li><strong>Esc</strong>: Close dialog</li>
        <li><strong>Tab</strong>: Cycle through elements</li>
        <li><strong>Ctrl+N</strong>:Next segment</li>
        <li><strong>Ctrl+P</strong>:Previous segment</li>
    </ul>
""".format(version=inselect_version)


class HelpDialog(QtGui.QDialog):
    """Help dialog"""
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        # Button
        self._button_box = QtGui.QDialogButtonBox(self)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        # Help area
        self._scroll_area = QtGui.QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        self._help = QtGui.QLabel(_help)
        self._help.setWordWrap(True)
        self._scroll_area.setWidget(self._help)
        # Layout
        self._layout = QtGui.QGridLayout(self)
        self._layout.addWidget(self._scroll_area, 0, 0)
        self._layout.addWidget(self._button_box, 1, 0)
        # Events
        self._button_box.accepted.connect(self.accept)
