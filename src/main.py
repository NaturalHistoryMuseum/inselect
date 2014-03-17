#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

from PySide import QtCore, QtGui
from segment import segment_edges
import copy
import cv2
import numpy as np

class GraphicsView(QtGui.QGraphicsView):
    def __init__ (self, parent  =None):
        QtGui.QGraphicsView.__init__(self, parent)
        self.is_dragging = False
        self.mousePressPos = QtCore.QPoint()
        self.box_create_start = QtCore.QPoint()
        self.scrollBarValuesOnMousePress = QtCore.QPoint()
        self.move_box = None

    def wheelEvent(self, event):
        if (event.modifiers() & QtCore.Qt.ControlModifier):
            if event.delta() > 0:
                scale = 1.25
            else:
                scale = 0.8
            self.scale_factor = scale
            self.scale(scale, scale)

    def scrollContentsBy(self, x, y):
        if not self.move_box or not self.move_box.isVisible():
            QtGui.QGraphicsView.scrollContentsBy(self, x, y)

    def mousePressEvent(self, event):
        QtGui.QGraphicsView.mousePressEvent(self, event) 

        if event.button() == QtCore.Qt.MidButton:
            self.mousePressPos = QtCore.QPoint(event.pos())
            self.scrollBarValuesOnMousePress.setX(self.horizontalScrollBar().value())
            self.scrollBarValuesOnMousePress.setY(self.verticalScrollBar().value())
        elif event.button() == QtCore.Qt.RightButton:
            self.box_create_start = QtCore.QPoint(event.pos())
        # event.accept()

    def mouseMoveEvent(self, event):
        QtGui.QGraphicsView.mouseMoveEvent(self, event) 
        if not self.box_create_start.isNull():
            if not self.move_box:
                self.move_box = BoxResizable(QtCore.QRectF(10, 10, 100, 100), color=QtCore.Qt.blue, scene=self.scene())
                self.scene().addItem(self.move_box)
            self.move_box.setVisible(True)
            s = self.mapToScene(self.box_create_start.x(), self.box_create_start.y())  
            pos = event.pos()
            e = self.mapToScene(pos.x(), pos.y())
            # self.move_box.setRect(s.x(), s.y(), e.x() - s.x(), e.y() - e.y())
            self.move_box._rect = QtCore.QRect(s.toPoint(), e.toPoint())
            self.move_box._boundingRect = QtCore.QRect(s.toPoint(), e.toPoint())
            # self.move_box.setPos(s)
            self.scene().update()
            # app.processEvents()
            # import time
            # time.sleep(0.1) 
            # self.move_box.resize(200,200)


        elif self.mousePressPos.isNull():
            event.ignore()
            return
        self.horizontalScrollBar().setValue(self.scrollBarValuesOnMousePress.x() - event.pos().x() + self.mousePressPos.x())
        self.verticalScrollBar().setValue(self.scrollBarValuesOnMousePress.y() - event.pos().y() + self.mousePressPos.y())
        self.horizontalScrollBar().update()
        self.verticalScrollBar().update()
        event.accept()

    def mouseReleaseEvent(self, event):
        if self.move_box:
            self.move_box.setVisible(False)
        QtGui.QGraphicsView.mouseReleaseEvent(self, event) 

        if event.button() == QtCore.Qt.MidButton: 
            self.mousePressPos = QtCore.QPoint()
        elif event.button() == QtCore.Qt.RightButton:
            e = QtCore.QPoint(event.pos())
            s = self.box_create_start
            x1, y1 = min(s.x(), e.x()), min(s.y(), e.y())
            x2, y2 = max(s.x(), e.x()), max(s.y(), e.y())
            s = self.mapToScene(x1, y1) 
            e = self.mapToScene(x2, y2)
            w = np.abs(s.x() - e.x())  
            h = np.abs(s.y() - e.y())
            box = BoxResizable(QtCore.QRectF(s.x(), s.y(), w, h),  scene=self.scene())
            self.scene().addItem(box)
            self.box_create_start = QtCore.QPoint()
        # event.accept() 

class GraphicsScene(QtGui.QGraphicsScene):
    def __init__ (self, parent  =None):
        QtGui.QGraphicsScene.__init__(self, parent)

    def mousePressEvent(self, event):
        QtGui.QGraphicsScene.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        QtGui.QGraphicsScene.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        QtGui.QGraphicsScene.mouseReleaseEvent(self, event)

    def setGraphicsView(self, view):
        self.view = view

class BoxResizable(QtGui.QGraphicsRectItem):
    def __init__(self, rect, parent=None, color=QtCore.Qt.red, scene=None):
        QtGui.QGraphicsRectItem.__init__(self, rect, parent, scene)
        self.setZValue(1000)
        self._rect = rect
        self._scene = scene
        self.mouseOver = False
        self.resizeHandleSize = 4.0

        self.mousePressPos = None
        self.mouseMovePos = None
        self.mouseIsPressed = False
        self.mousePressArea = None
        self.color = color

        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable|QtGui.QGraphicsItem.ItemIsFocusable)
        self.setAcceptsHoverEvents(True)

        self.updateResizeHandles()

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def hoverEnterEvent(self, event):
        self.updateResizeHandles()
        self.mouseOver = True
        self.prepareGeometryChange()

    def hoverLeaveEvent(self, event):
        self.mouseOver = False
        self.prepareGeometryChange()

    def hoverMoveEvent(self, event):
        if self.topLeft.contains(event.scenePos()) or self.bottomRight.contains(event.scenePos()):
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif self.topRight.contains(event.scenePos()) or self.bottomLeft.contains(event.scenePos()):
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        else:
            self.setCursor(QtCore.Qt.SizeAllCursor)

        QtGui.QGraphicsRectItem.hoverMoveEvent(self, event)

    def mousePressEvent(self, event):
        """
        Capture mouse press events and find where the mosue was pressed on the object
        """
        self.mousePressPos = event.scenePos()
        self.mouseIsPressed = True
        self.rectPress = copy.deepcopy(self._rect)

        # Top left corner
        if self.topLeft.contains(event.scenePos()):
            self.mousePressArea = 'topleft'
        # top right corner            
        elif self.topRight.contains(event.scenePos()):
            self.mousePressArea = 'topright'
        #  bottom left corner            
        elif self.bottomLeft.contains(event.scenePos()):
            self.mousePressArea = 'bottomleft'
        # bottom right corner            
        elif self.bottomRight.contains(event.scenePos()):
            self.mousePressArea = 'bottomright'
        # entire rectangle
        else:
            self.mousePressArea = None

        QtGui.QGraphicsRectItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        """
        Capture nmouse press events.
        """
        self.mouseIsPressed = False
        self.updateResizeHandles()
        self.prepareGeometryChange()
        self._rect = self._rect.normalized()

        QtGui.QGraphicsRectItem.mouseReleaseEvent(self, event)

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events.
        """
        self.mouseMovePos = event.scenePos()

        if self.mouseIsPressed:
            # Move top left corner
            if self.mousePressArea=='topleft':
                self._rect.setTopLeft(self.rectPress.topLeft()-(self.mousePressPos-self.mouseMovePos))
            # Move top right corner            
            elif  self.mousePressArea=='topright':
                self._rect.setTopRight(self.rectPress.topRight()-(self.mousePressPos-self.mouseMovePos))
            # Move bottom left corner            
            elif  self.mousePressArea=='bottomleft':
                self._rect.setBottomLeft(self.rectPress.bottomLeft()-(self.mousePressPos-self.mouseMovePos))
            # Move bottom right corner            
            elif  self.mousePressArea=='bottomright':
                self._rect.setBottomRight(self.rectPress.bottomRight()-(self.mousePressPos-self.mouseMovePos))
            # Move entire rectangle, don't resize
            else:
                self._rect.moveCenter(self.rectPress.center()-(self.mousePressPos-self.mouseMovePos))

            self.updateResizeHandles()
            self.prepareGeometryChange()

        QtGui.QGraphicsRectItem.mousePressEvent(self, event)

    def boundingRect(self):
        """
        Return bounding rectangle
        """
        return self._boundingRect

    def updateResizeHandles(self):
        """
        Update bounding rectangle and resize handles
        """
        self.offset = self.resizeHandleSize*(self._scene.view.mapToScene(1,0)-self._scene.view.mapToScene(0,1)).x()        
        self._boundingRect = self._rect.adjusted(-self.offset, -self.offset, self.offset, self.offset)

        # self._rect = self._rect.normalized()
        # Note: this draws correctly on a view with an inverted y axes. i.e. QGraphicsView.scale(1,-1)
        self.topLeft = QtCore.QRectF(self._boundingRect.topLeft().x(), self._boundingRect.topLeft().y(),
                                     2*self.offset, 2*self.offset)
        self.topRight = QtCore.QRectF(self._boundingRect.topRight().x() - 2*self.offset, self._boundingRect.topRight().y() ,
                                     2*self.offset, 2*self.offset)
        self.bottomLeft = QtCore.QRectF(self._boundingRect.bottomLeft().x(), self._boundingRect.bottomLeft().y() - 2*self.offset,
                                     2*self.offset, 2*self.offset)
        self.bottomRight = QtCore.QRectF(self._boundingRect.bottomRight().x() - 2*self.offset, self._boundingRect.bottomRight().y() - 2*self.offset,
                                     2*self.offset, 2*self.offset)

    def paint(self, painter, option, widget):
        """
        Paint Widget
        """
        # # show boundingRect for debug purposes
        # painter.setPen(QtGui.QPen(QtCore.Qt.red, 0, QtCore.Qt.DashLine))
        # painter.drawRect(self._boundingRect)
        # Paint rectangle
        painter.setPen(QtGui.QPen(self.color, 0, QtCore.Qt.SolidLine))
        painter.drawRect(self._rect)

        # If mouse is over, draw handles
        if self.mouseOver:
            # if rect selected, fill in handles
            # if self.isSelected():
            #     painter.setBrush(QtGui.QBrush(QtGui.QColor(0,0,0)))
            painter.drawRect(self.topLeft)
            painter.drawRect(self.topRight)
            painter.drawRect(self.bottomLeft)
            painter.drawRect(self.bottomRight)

# class ScrollArea(QtGui.QScrollArea):
#     def __init__(self, parent=None):
#         QtGui.QScrollArea.__init__(self)
#         self.is_dragging = False
#         self.mousePressPos = QtCore.QPoint()
#         self.scrollBarValuesOnMousePress = QtCore.QPoint()

#     def wheelEvent(self, event):
#         if (event.modifiers() & QtCore.Qt.ControlModifier):
#             if event.delta() > 0:
#                 scale = 1.25
#             else:
#                 scale = 0.8
#             self.window().scaleImage(scale)

#     def mousePressEvent(self, event):
#         if event.button() == QtCore.Qt.MidButton:
#             self.mousePressPos = QtCore.QPoint(event.pos())
#             self.scrollBarValuesOnMousePress.setX(self.horizontalScrollBar().value())
#             self.scrollBarValuesOnMousePress.setY(self.verticalScrollBar().value())
#         event.accept()

#     def mouseMoveEvent(self, event):
#         if self.mousePressPos.isNull():
#             event.ignore()
#             return
#         self.horizontalScrollBar().setValue(self.scrollBarValuesOnMousePress.x() - event.pos().x() + self.mousePressPos.x())
#         self.verticalScrollBar().setValue(self.scrollBarValuesOnMousePress.y() - event.pos().y() + self.mousePressPos.y())
#         self.horizontalScrollBar().update()
#         self.verticalScrollBar().update()
#         event.accept()

#     def mouseReleaseEvent(self, event):
#         if event.button() == QtCore.Qt.MidButton: 
#             self.mousePressPos = QtCore.QPoint()
#         event.accept()

class ImageViewer(QtGui.QMainWindow):
    def __init__(self, file_name=None):
        super(ImageViewer, self).__init__()

        self.printer = QtGui.QPrinter()
        self.scaleFactor = 0.0

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
                QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        # self.scrollArea = ScrollArea()
        # self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        # self.scrollArea.setWidget(self.imageLabel)
        # self.setCentralWidget(self.scrollArea)
        self.scene = GraphicsScene()
        # self.scene.setSceneRect(-500, 0, 600, 600)
        # self.view = QtGui.QGraphicsView()
        self.view = GraphicsView()
        self.view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
        self.view.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        # self.view.scale(1,-1)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setUpdatesEnabled(True)
        self.view.setMouseTracking(True)
        self.scene.setGraphicsView(self.view)
        self.view.setScene(self.scene)
        self.view.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setCentralWidget(self.view)
        self.box = BoxResizable(QtCore.QRectF(50, 50, 100.0, 100.0),  scene=self.scene)
        image = QtGui.QImage(file_name)

        item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(image))
        self.scene.addItem(item) 
        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        self.resize(500, 400)
        if file_name:
            self.open(file_name)


    def open(self, file_name=None):
        if not file_name:
            file_name, _ = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                    QtCore.QDir.currentPath())
        if file_name:
            self.file_name = file_name
            image = QtGui.QImage(file_name)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % file_name)
                return

            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))

            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def print_(self):
        dialog = QtGui.QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QtGui.QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        QtGui.QMessageBox.about(self, "About Image Viewer",
                "<p>The <b>Image Viewer</b> example shows how to combine "
                "QLabel and QScrollArea to display an image. QLabel is "
                "typically used for displaying text, but it can also display "
                "an image. QScrollArea provides a scrolling view around "
                "another widget. If the child widget exceeds the size of the "
                "frame, QScrollArea automatically provides scroll bars.</p>"
                "<p>The example demonstrates how QLabel's ability to scale "
                "its contents (QLabel.scaledContents), and QScrollArea's "
                "ability to automatically resize its contents "
                "(QScrollArea.widgetResizable), can be used to implement "
                "zooming and scaling features.</p>"
                "<p>In addition the example shows how to use QPainter to "
                "print an image.</p>")

    def add_box(self, rect):
        x, y, w, h = rect
        s = self.view.mapToScene(x, y)
        e = self.view.mapToScene(x + w, y + h)
        qrect = QtCore.QRectF(s.x(), s.y(), e.x() - s.x(), e.y() - s.y()) 
        box = BoxResizable(qrect,  scene=self.scene)
        self.scene.addItem(box)

    def segment(self):
        image = cv2.imread(self.file_name)
        rects = segment_edges(image)
        image = QtGui.QImage(self.file_name)
        item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(image))
        self.scene.addItem(item) 
        for rect in rects:
            self.add_box(rect)


    def createActions(self):
        self.openAct = QtGui.QAction(self.style().standardIcon(
                QtGui.QStyle.SP_DirIcon), "&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.printAct = QtGui.QAction("&Print...", self, shortcut="Ctrl+P",
                enabled=False, triggered=self.print_)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.zoomInAct = QtGui.QAction("Zoom &In (25%)", self,
                shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QtGui.QAction("Zoom &Out (25%)", self,
                shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)

        self.normalSizeAct = QtGui.QAction("&Normal Size", self,
                shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)

        self.fitToWindowAct = QtGui.QAction("&Fit to Window", self,
                enabled=False, checkable=True, shortcut="Ctrl+F",
                triggered=self.fitToWindow)

        self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                triggered=QtGui.qApp.aboutQt)

        self.segment_action = QtGui.QAction(self.style().standardIcon(
                QtGui.QStyle.SP_ComputerIcon), 
            "&Segment", self, shortcut="",
            statusTip="Segment",
            triggered=self.segment)

    def createMenus(self):
        self.toolbar = self.addToolBar("Edit")
        self.toolbar.addAction(self.openAct)
        self.toolbar.addAction(self.segment_action)
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QtGui.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QtGui.QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep()/2)))

    def keyPressEvent(self, event):
        if event.key() == 16777216:
        # if event.key() == Qtcore.Qt.Key_Escape:
            sys.exit(1)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    # window = ImageViewer("../data/drawer.jpg")
    window = ImageViewer("../data/Plecoptera_Accession_Drawer_4.jpg")
    window.showMaximized()

    window.show()
    sys.exit(app.exec_())
