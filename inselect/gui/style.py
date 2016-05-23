STYLESHEET = """
QWidget {
    background: #2e2e2e;
    color: #dddddd;
    border: 0;
    padding: 0;
    margin: 0;
    font-family: Arial;
    /*TODO LH Can we include Avenir or some other good font?*/
    /*font-family: "Avenir", "Helvetica Neue", Helvetica, Arial, sans-serif;*/
}

QDialog {
    background: #4c4c4c;
}

QDialog QWidget {
    background: #4c4c4c;
}

QDialog QPushButton {
    font-size: 13pt;
    font-weight: bold;
    padding: 8px 36px;
    border-radius: 12px;
    margin-left: 6px;
}

QAbstractItemView {
    border: none;
    background-color: #8f8e93;
}

QGraphicsView {
    border: none;
    background-color: #8f8e93;
}

QLabel {
    border: 0;
}

QCheckBox, QRadioButton {
    border: 0;
}

QRadioButton::indicator {
    border: 2px solid #3a3939;
    border-radius: 6px;
    background-color: white;
    width: 10px;
    height: 10px;
    margin-left: 5px;
}

QRadioButton::indicator:checked {
    background-color: #8d20ae;
}

QRadioButton::indicator:disabled {
    background-color: #3e3e3e;
}

QStatusBar {
    border: none;
    border-top: 1px solid #5a5a5a;
}

QStatusBar QWidget {
    border: none;
}

QStatusBar::item{
    border: none;
}

QStatusBar > QLabel {
    border-left: 2px solid #5A5A5A;
}

QScrollBar {
    border: None;
    background: #191919;
}

QScrollBar:horizontal {
    height: 15px;
    margin: 0;
}

QScrollBar:vertical {
    width: 15px;
    margin: 32px 0 0 0;
}

QScrollBar::handle {
    background: #353535;
    border: 1px solid #5A5A5A;
}

QScrollBar::handle:horizontal {
    border-width: 0 1px 0 1px;
}

QScrollBar::handle:vertical {
    border-width: 1px 0 1px 0;
}

QScrollBar::handle:horizontal {
    min-width: 20;
}

QScrollBar::handle:vertical {
    min-height: 20;
}

QScrollBar::add-line, QScrollBar::sub-line {
    background:#353535;
    border: 1px solid #5A5A5A;
    subcontrol-origin: margin;
}

QScrollBar::add-line {
    position: absolute;
}

QScrollBar::add-line:horizontal {
    width: 15px;
    subcontrol-position: left;
    left: 15px;
}

QScrollBar::add-line:vertical {
    height: 15px;
    subcontrol-position: top;
    top: 15px;
}

QScrollBar::sub-line:horizontal {
    width: 15px;
    subcontrol-position: top left;
}

QScrollBar::sub-line:vertical {
    height: 15px;
    subcontrol-position: top;
}

QScrollBar:left-arrow, QScrollBar::right-arrow,
QScrollBar::up-arrow, QScrollBar::down-arrow {
    border: 1px solid #5A5A5A;
    width: 3px;
    height: 3px;
}

QScrollBar::add-page, QScrollBar::sub-page {
    background: 0;
}

QComboBox::down-arrow {
    border: 1px solid #5A5A5A;
    background: #353535;
}

QComboBox::drop-down {
    border: 1px solid #5A5A5A;
    background: #353535;
}

QComboBox::down-arrow {
    width: 3px;
    height: 3px;
    border: 1px solid #5A5A5A;
}

/* No image for splitter handle */
QSplitter::handle:horizontal {
    image: none;
}

/* Taken from https://bugreports.qt.io/browse/QTBUG-13768 */
QSplitterHandle:hover {
}

QSplitter::handle:horizontal:hover {
    background-color: #5b5b5b;
}

QProgressBar {
    text-align: center;
}

QProgressBar::chunk {
    width: 1px;
    background-color: #8d20ae;
}

QSlider {
    border: 0;
}

QSlider::handle:horizontal {
    width: 10px;
    background-color: #dddddd;
    border-radius: 3px;
    /* -ve vertical margins to get handle to protude beyond groove */
    margin-top: -4px;
    margin-bottom: -4px;
}

QSlider::handle:horizontal:hover {
    background-color: white;
}

QSlider::handle:horizontal:disabled {
    background-color: #aaaaaa;
}

QSlider::groove:horizontal {
    background: #4a4a4a;
    height: 10px;
    border-radius: 4px;
}

QPushButton {
    font-size: 13pt;
    padding: 8px;
    border-radius: 12px;
    text-align: center;
}

/* No drop-down menu item */
QPushButton::menu-indicator {
    image: "";
}

QPushButton:hover {
    color: white;
    background-color: #5b5b5b;
}

QPushButton:default {
    color: white;
    background-color: #8d20ae;
    border: white;
}

QComboBox:selected {
    color: white;
    background-color: #5b5b5b;
}

QMenu {
    background-color: #4f4f4f;
}

QMenu::item {
    /* top right bottom left */
    padding: 4px 6px 4px 24px;
    border: 1px solid rgba(0, 0, 0, 0);    /* Space for selection box */
}

QMenu::icon {
    margin-left: 4px;    /* So that icons do not touching left of menu */
}

QMenu::item:selected {
    color: white;
    background: rgba(141, 32, 174, 88);
    border: 1px solid #3b034c;
    border-radius: 3px;
}

QMenu::item:checked {
    color: white;
    background: rgba(141, 32, 174, 88);
    border: 1px solid #3b034c;
    border-radius: 3px;
}

QMenu::item::disabled {
    color: gray;
    background-color: #4f4f4f;
}

/* To get menu bar appearing correctly on Windows
See https://bugreports.qt.io/browse/QTBUG-49115
*/
QMenuBar, QMenuBar::item {
    background: transparent;
}

QTabWidget {
    background-color: blue;
    border: 0;
    margin: 0;
    padding: 0;
}

QTabWidget::pane {
    border: 0;
    margin: 0;
    padding: 0;
    background-color: red;
}

QTabWidget::tab-bar {
    position: absolute;
    left: 0;
    background-color: black;
}

QTabBar {
    background-color: green;
    font-size: 17pt;
    padding: 0;
    border: 0;
    margin: 0;
    margin-left: 4px;
}

QTabBar::tab {
    padding: 8px;
    border: 0;
    margin: 0;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
}

QTabBar::tab:selected {
    color: white;
    background-color: #2e2e2e;
/*
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop: 0 #5b5b5b, stop:1 #2e2e2e
    );
*/
}

QTabBar::tab:hover {
    color: white;
    background-color: #2e2e2e;
}

QToolBar {
    spacing: 0;
    margin: 0;
    border: 0;
    padding: 0;
    border-bottom: 1px solid #5a5a5a;
}

QToolBar QWidget {
    font-size: 11px;
    padding: 0;
    border: 0;
    margin: 0;
}

QToolBar::separator {
    background: #666666;
    width: 1px;
    padding: 0;
    border: 0;
    margin: 0;
}

QToolBar QToolButton {
    margin: 0;
    border: 0;
    padding: 2px;
}

QToolBar QToolButton:checked {
    color: white;
    background-color: #5b5b5b;
}

QToolBar QToolButton:hover {
    color: white;
    background-color: #5b5b5b;
}

QToolBar QToolButton:disabled {
    color: #aaaaaa;
}

QToolBar QToolButton::menu-indicator {
    image: "";
}

/* Custom widgets */
SideBar {
    padding: 0 2px;
    border: none;

}

ToggleWidgetLabel {
    margin: 0;
    padding: 4px 2px;
}

ToggleWidgetLabel QLabel {
    font-size: 13pt;
    text-decoration: 0;
}

ToggleWidgetLabel QLabel:hover {
    color: white;
}

PopupPanel {
    margin: 0;
    padding: 0;
    border: 0;
}

PanelContainer {
    background: #4f4f4f;
    padding: -10px;
    margin: 2;
    border: 1px solid #dddddd;
    border-radius: 2px;
}

PanelContainer > QWidget {
    background: #4f4f4f;
}

BoldLabel {
    font-weight: bold;
}

RevealPathLabel {
    text-decoration: underline;
}

FieldEdit {
    background-color: #4a4a4a;
    padding: 2px;
    border: 1px solid #3a3939;
    margin: 0;
}

FieldEdit:disabled {
    background: #3e3e3e;
}

FieldEdit:hover:!focus {
    color: white;
    background-color: #5b5b5b;
}

FieldEdit:focus {
    color: black;
    background-color: white;
}

FieldEdit[invalid="true"] {
    color: black;
    background: #fb9a99;
}

FieldEdit[invalid="true"]:hover {
    color: black;
    background: #fbb8b6;
}

FieldEdit[invalid="true"]:focus {
    color: black;
    background: #fbb8b6;
}

FieldComboBox {
    border: 1px solid #3a3939;
    /* Fiddling here for consistency with FieldEdit */
    padding-top: 2px;
    padding-left: 5px;
    margin-left: 3px;
}

FieldComboBox:disabled {
    background: #3e3e3e;
}

FieldComboBox:hover {
    color: white;
    background-color: #5b5b5b;
}

FieldComboBox[invalid="true"] {
    background: #fb9a99;
}

FieldComboBox[invalid="true"]:hover {
    background: #fbb8b6;
}

FieldComboBox[invalid="true"]:focus {
    background: #fbb8b6;
}

HorizontalLine {
    border-top: 1px solid #dddddd;
    border-left: 0;
    border-bottom: 0;
    border-right: 0;
}
"""
