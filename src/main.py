#!/usr/bin/env python
"""Inselect.

Usage:
    main.py
    main.py <filename>
    main.py --batch=input_dir
    main.py --batch=input_dir --recursive
    main.py --batch=input_dir --output=output_dir

Options:
  -h --help     Show this screen.
  --version     Show version.
  --batch=<dir> Input directory 
  --recursive   Traverse directory structure recursively.
"""
filename = None
from docopt import docopt
from PySide import QtCore, QtGui
from segment import segment_edges, segment_intensity
import cv2
import os
import numpy as np
from multiprocessing import Process, Queue
import sys
import csv

from qt_util import read_qt_image


def is_image_file(file_name):
    name, ext = os.path.splitext(file_name.lower())
    return ext in [".jpg", ".tiff", ".png"]


class GraphicsView(QtGui.QGraphicsView):
    def __init__ (self, parent=None, wireframe_mode=False):
        QtGui.QGraphicsView.__init__(self, parent)
        self.is_dragging = False
        self.mouse_press_pos = QtCore.QPoint()
        self.box_create_start = QtCore.QPoint()
        self.scrollBarValuesOnMousePress = QtCore.QPoint()
        self.move_box = None
        self.is_resizing = False
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.wireframe_mode = wireframe_mode
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        self.scene().addItem(item)

    def remove_item(self, item):
        self.items.remove(item)
        self.scene().removeItem(item)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            for box in list(self.items):
                # if hasattr(box, "isSelected") and box.isSelected():
                if box.isSelected():
                    self.remove_item(box)

        QtGui.QGraphicsView.keyPressEvent(self, event)

    def set_scale(self, scale):
        self.scale_factor = scale
        self.scale(scale, scale)

    def wheelEvent(self, event):
        if (event.modifiers() & QtCore.Qt.ControlModifier):
            if event.delta() > 0:
                scale = 1.2
            else:
                scale = 0.8
            self.set_scale(scale)
            return
        QtGui.QGraphicsView.wheelEvent(self, event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MidButton:
            self.mouse_press_pos = QtCore.QPoint(event.pos())
            self.scrollBarValuesOnMousePress.setX(self.horizontalScrollBar().value())
            self.scrollBarValuesOnMousePress.setY(self.verticalScrollBar().value())
            event.accept()
            return
        elif event.button() == QtCore.Qt.LeftButton and not self.is_resizing:
            # reveal hidden boxes, smallest to the front
            if self.wireframe_mode:
                e = self.mapToScene(event.pos().x(), event.pos().y())
                items = self.scene().items(e)
                items = [item for item in items if item in self.items]
                if items:
                    items.sort(lambda a, b: cmp(a.boundingRect().width() * a.boundingRect().height(),
                        b.boundingRect().width() * b.boundingRect().height()))
                    for item in self.items:
                        item.setZValue(1000)
                    items[0].setZValue(1001)
                    self.move_box.setZValue(1002)
                # items[0].setSelected(True)
                # items[-1].setSelected(False)
            # else:
                # e = self.mapToScene(event.pos().x(), event.pos().y())
                # items = self.scene().items(e)
                # items = [item for item in items if item in self.items]
                # for item in self.items:
                #     if item.isSelected():
                #         item.setZValue(1E9)
                #     else:
                #         b = item.boundingRect()
                #         item.setZValue(max(1000, 1E9 - b.width() * b.height()))
        elif event.button() == QtCore.Qt.RightButton:
            self.box_create_start = QtCore.QPoint(event.pos())
            return
        QtGui.QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        QtGui.QGraphicsView.mouseMoveEvent(self, event)
        if not self.box_create_start.isNull():
            self.move_box.setVisible(True)
            s = self.mapToScene(self.box_create_start.x(), self.box_create_start.y())
            pos = event.pos()
            e = self.mapToScene(pos.x(), pos.y())
            w, h = e.toPoint().x() - s.toPoint().x(), e.toPoint().y() - s.toPoint().y()
            self.move_box.setPos(s)
            self.move_box._rect = QtCore.QRect(0, 0, w, h)
            self.move_box._boundingRect = QtCore.QRect(0, 0, w, h)
            self.scene().update()
        if self.mouse_press_pos.isNull():
            event.ignore()
            return
        self.horizontalScrollBar().setValue(self.scrollBarValuesOnMousePress.x() - event.pos().x() + self.mouse_press_pos.x())
        self.verticalScrollBar().setValue(self.scrollBarValuesOnMousePress.y() - event.pos().y() + self.mouse_press_pos.y())
        self.horizontalScrollBar().update()
        self.verticalScrollBar().update()
        event.accept()

    def mouseReleaseEvent(self, event):
        QtGui.QGraphicsView.mouseReleaseEvent(self, event)
        if event.button() == QtCore.Qt.MidButton:
            self.mouse_press_pos = QtCore.QPoint()

        elif event.button() == QtCore.Qt.RightButton:
            e = QtCore.QPoint(event.pos())
            s = self.box_create_start
            x1, y1 = min(s.x(), e.x()), min(s.y(), e.y())
            x2, y2 = max(s.x(), e.x()), max(s.y(), e.y())
            s = self.mapToScene(x1, y1)
            e = self.mapToScene(x2, y2)
            w = np.abs(s.x() - e.x())
            h = np.abs(s.y() - e.y())
            if w != 0 and h != 0:
                box = BoxResizable(QtCore.QRectF(s.x(), s.y(), w, h),  scene=self.scene())
                # box.setZValue(1001)
                if not self.wireframe_mode:
                    b = box.boundingRect()
                    box.setZValue(max(1000, 1E9 - b.width() * b.height()))
                    box.updateResizeHandles()
                # self.scene().addItem(box)
                self.add_item(box)
        if self.move_box:
            self.move_box.setVisible(False)
            self.box_create_start = QtCore.QPoint()
        # event.accept()

class GraphicsScene(QtGui.QGraphicsScene):
    def __init__ (self, parent=None):
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
    def __init__(self, rect, parent=None, color=QtCore.Qt.blue, transparent=False, scene=None):
        QtGui.QGraphicsRectItem.__init__(self, rect, parent, scene)
        self._rect = rect
        self._scene = scene
        self.orig_rect = QtCore.QRectF(rect)
        self.mouseOver = False
        self.handle_size = 4.0
        self.mouse_press_pos = None
        self.mouse_move_pos = None
        self.mouse_is_pressed = False
        self.mouse_press_area = None
        self.color = color
        self.transparent = transparent
        self.setFlags(QtGui.QGraphicsItem.ItemIsFocusable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptsHoverEvents(True)
        self.updateResizeHandles()
        # self.setZValue(5000)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def hoverEnterEvent(self, event):
        self.updateResizeHandles()
        self.mouseOver = True
        b = self.boundingRect()
        if self.isSelected():
            self.setZValue(1E9)
        else:
            self.setZValue(max(1000, 1E9 - b.width() * b.height()))

    def hoverLeaveEvent(self, event):
        self.prepareGeometryChange()
        self.mouseOver = False
        self.scene().view.is_resizing = False
        b = self.boundingRect()
        # if self.isSelected():
        #     self.setZValue(1E9)
        # else:
        self.setZValue(max(1000, 1E9 - b.width() * b.height()))

    def hoverMoveEvent(self, event):
        if self.top_left_handle.contains(event.pos()) or self.bottom_right_handle.contains(event.pos()):
        # if self.topLeft.contains(event.scenePos()) or self.bottomRight.contains(event.scenePos()):
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
            self.scene().view.is_resizing = True
        elif self.top_right_handle.contains(event.pos()) or self.bottom_left_handle.contains(event.pos()):
        # elif self.topRight.contains(event.scenePos()) or self.bottomLeft.contains(event.scenePos()):
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
            self.scene().view.is_resizing = True
        else:
            self.setCursor(QtCore.Qt.SizeAllCursor)
            self.scene().view.is_resizing = False

        b = self.boundingRect()
        if self.isSelected():
            self.setZValue(1E9)
        else:
            self.setZValue(max(1000, 1E9 - b.width() * b.height()))
        QtGui.QGraphicsRectItem.hoverMoveEvent(self, event)

    def mousePressEvent(self, event):
        """
        Capture mouse press events and find where the mosue was pressed on the object
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_press_pos = event.scenePos()
            self.mouse_is_pressed = True
            self.rect_press = QtCore.QRectF(self._rect)

            # Top left corner
            if self.top_left_handle.contains(event.pos()):
                self.mouse_press_area = 'topleft'
            # top right corner
            elif self.top_right_handle.contains(event.pos()):
                self.mouse_press_area = 'topright'
            #  bottom left corner
            elif self.bottom_left_handle.contains(event.pos()):
                self.mouse_press_area = 'bottomleft'
            # bottom right corner
            elif self.bottom_right_handle.contains(event.pos()):
                self.mouse_press_area = 'bottomright'
            # entire rectangle
            else:
                self.mouse_press_area = None

            QtGui.QGraphicsRectItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        """
        Capture nmouse press events.
        """
        self.mouse_is_pressed = False
        self._rect = self._rect.normalized()
        self.updateResizeHandles()
        QtGui.QGraphicsRectItem.mouseReleaseEvent(self, event)

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events.
        """
        self.mouse_move_pos = event.scenePos()
        if self.mouse_is_pressed:
            if self.mouse_press_area:
                self.prepareGeometryChange()
                # Move top left corner
                if self.mouse_press_area=='topleft':
                    self._rect.setTopLeft(self.rect_press.topLeft()-(self.mouse_press_pos-self.mouse_move_pos))
                # Move top right corner
                elif  self.mouse_press_area=='topright':
                    self._rect.setTopRight(self.rect_press.topRight()-(self.mouse_press_pos-self.mouse_move_pos))
                # Move bottom left corner
                elif  self.mouse_press_area=='bottomleft':
                    self._rect.setBottomLeft(self.rect_press.bottomLeft()-(self.mouse_press_pos-self.mouse_move_pos))
                # Move bottom right corner
                elif  self.mouse_press_area=='bottomright':
                    self._rect.setBottomRight(self.rect_press.bottomRight()-(self.mouse_press_pos-self.mouse_move_pos))
                event.accept()
                self.updateResizeHandles()
                # self.setZValue(1000 + self._rect.width() * self._rect.height())

                return
            # Move entire rectangle, don't resize
            # else:
            #     self._rect.moveCenter(self.rect_press.center()-(self.mouse_press_pos-self.mouse_move_pos))
            self.updateResizeHandles()

            QtGui.QGraphicsRectItem.mouseMoveEvent(self, event)

    def boundingRect(self):
        """
        Return bounding rectangle
        """
        return self._boundingRect

    def updateResizeHandles(self):
        """
        Update bounding rectangle and resize handles
        """
        self.prepareGeometryChange()

        self.offset = self.handle_size*(self._scene.view.mapToScene(1,0)-self._scene.view.mapToScene(0,1)).x()
        self.offset1 = (self._scene.view.mapToScene(1,0)-self._scene.view.mapToScene(0,1)).x()
        self._boundingRect = self._rect.adjusted(-self.offset, -self.offset, self.offset, self.offset)
        self._innerRect = self._rect.adjusted(self.offset1, self.offset1, -self.offset1, -self.offset1)

        b = self._boundingRect
        self.top_left_handle = QtCore.QRectF(b.topLeft().x(), b.topLeft().y(), 2*self.offset, 2*self.offset)
        self.top_right_handle = QtCore.QRectF(b.topRight().x() - 2*self.offset, b.topRight().y(),
            2*self.offset, 2*self.offset)
        self.bottom_left_handle = QtCore.QRectF(b.bottomLeft().x(), b.bottomLeft().y() - 2*self.offset,
            2*self.offset, 2*self.offset)
        self.bottom_right_handle = QtCore.QRectF(b.bottomRight().x() - 2*self.offset, b.bottomRight().y() - 2*self.offset,
            2*self.offset, 2*self.offset)
        if self.isSelected():
            self.setZValue(1E9)
        else:
            self.setZValue(max(1000, 1E9 - b.width() * b.height()))

    def map_rect_to_scene(self, map_rect):
        rect = map_rect
        target_rect = QtCore.QRectF(rect)
        t = rect.topLeft()
        b = rect.bottomRight()
        target_rect.setTopLeft(QtCore.QPointF(t.x() + self.pos().x(), t.y() + self.pos().y()))
        target_rect.setBottomRight(QtCore.QPointF(b.x() + self.pos().x(), b.y() + self.pos().y()))
        return target_rect

    def paint(self, painter, option, widget):
        """
        Paint Widget
        """
        # Paint rectangle
        if self.isSelected():
            color = QtCore.Qt.red
            # print self._rect
            # e = self.mapToScene(self.pos().x(), self.pos().y())
            # print e
        else:
            color = self.color
        painter.setPen(QtGui.QPen(color, 0, QtCore.Qt.SolidLine))
        painter.drawRect(self._rect)

        # b = self._boundingRect
        # e = self.pos() #self.mapToScene(self.pos().x(), self.pos().y())
        # e = self.scenePos() #self.mapToScene(self.pos().x(), self.pos().y())
        # e = self.mapToParent(self., self.pos().y())
        # rect = QtCore.QRectF(e.x(), e.(), b.width(), b.height())
        if not self.transparent:
            rect = self._innerRect
            if rect.width() > 0 and rect.height() != 0:
                # normalize negative widths and heights, during resizing
                x1, y1 = rect.x(), rect.y()
                x2, y2 = rect.x() + rect.width(), rect.y() + rect.height()
                rect = QtCore.QRectF(min(x1, x2), min(y1, y2), abs(rect.width()), abs(rect.height()))
                target_rect = self.map_rect_to_scene(rect)
                painter.drawPixmap(rect, self.scene().image.pixmap(), target_rect)
        # If mouse is over, draw handles
        if self.mouseOver:
            # if self.isSelected():
            #     rect = self._innerRect
            #     target_rect = self.map_rect_to_scene(rect)
            #     painter.drawPixmap(rect, self.scene().image.pixmap(), target_rect)
            painter.drawRect(self.top_left_handle)
            painter.drawRect(self.top_right_handle)
            painter.drawRect(self.bottom_left_handle)
            painter.drawRect(self.bottom_right_handle)


class ImageViewer(QtGui.QMainWindow):
    def __init__(self, filename=None):
        super(ImageViewer, self).__init__()
        self.wireframe_mode = 0
        self.view = GraphicsView(wireframe_mode=self.wireframe_mode)
        self.scene = GraphicsScene()
        # self.view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
        self.view.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
        self.view.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setUpdatesEnabled(True)
        self.view.setMouseTracking(True)
        self.scene.setGraphicsView(self.view)
        self.view.setScene(self.scene)
        self.view.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setCentralWidget(self.view)
        # self.box = BoxResizable(QtCore.QRectF(50, 50, 100.0, 100.0),  scene=self.scene)
        self.view.move_box = BoxResizable(QtCore.QRectF(10, 10, 100, 100), color=QtCore.Qt.red,
            transparent=True, scene=self.scene)
        self.scene.addItem(self.view.move_box)
        self.view.move_box.setVisible(False)
        if not self.wireframe_mode:
            self.view.move_box.setZValue(1E9)

        if filename is None:
            image = QtGui.QImage()
        else:
            image = read_qt_image(filename)

        item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(image))
        self.scene.addItem(item)
        self.image_item = item
        self.scene.image = item
        self.create_actions()
        self.create_menus()

        self.setWindowTitle("Image Viewer")
        self.resize(500, 400)
        if filename:
            self.open(filename)


    def open(self, filename=None):
        if not filename:
            filename, _ = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                    QtCore.QDir.currentPath())
        if filename:
            self.filename = filename
            image = read_qt_image(filename)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                                             "Cannot load %s." % filename)
                return
            for item in list(self.view.items):
                self.view.remove_item(item)

            self.image_item.setPixmap(QtGui.QPixmap.fromImage(image))
            self.scene.setSceneRect(0, 0, image.width(), image.height())
            self.segment_action.setEnabled(True)
            self.export_action.setEnabled(True)
            self.zoom_in_action.setEnabled(True)
            self.zoom_out_action.setEnabled(True)

    def zoom_in(self):
        self.view.set_scale(1.2)

    def zoom_out(self):
        self.view.set_scale(0.8)

    def about(self):
        QtGui.QMessageBox.about(self, "Insect Selector",
                "Stefan van der Walt\nPieter Holtzhausen")

    def add_box(self, rect):
        x, y, w, h = rect
        s = QtCore.QPoint(x, y)
        e = QtCore.QPoint(x + w, y + h)
        qrect = QtCore.QRectF(s.x(), s.y(), e.x() - s.x(), e.y() - s.y())
        box = BoxResizable(qrect, transparent=self.wireframe_mode, scene=self.scene)
        self.view.add_item(box)
        if not self.wireframe_mode:
            b = box.boundingRect()
            box.setZValue(max(1000, 1E9 - b.width() * b.height()))
            box.updateResizeHandles()

    def segment(self):
        self.progressDialog = QtGui.QProgressDialog(self)
        self.progressDialog.setWindowTitle("Segmenting...")
        self.progressDialog.setValue(0)
        self.progressDialog.setMaximum(0)
        self.progressDialog.setMinimum(0)
        self.progressDialog.show()
        image = cv2.imread(self.filename)

        def f(image, results, window=None):
            rects = segment_edges(image, window=window, variance_threshold=100, size_filter=1)
            results.put(rects)

        results = Queue()
        window = None
        selected = self.scene.selectedItems()
        if selected:
            selected = selected[0]
            window_rect = selected.map_rect_to_scene(selected._rect)
            p = window_rect.topLeft()
            window = [p.x(), p.y(), window_rect.width(), window_rect.height()]
            # rects = segment_edges(image, window=window, threshold=50, variance_threshold=100, size_filter=0)
            rects = segment_intensity(image, window=window)
            self.view.remove_item(selected)
        else:
            p = Process(target=f, args=[image, results, window])
            p.start()
            while results.empty():
                app.processEvents()
            p.join()
            rects = results.get()
        for rect in rects:
            self.add_box(rect)
        self.progressDialog.hide()


    def export(self):
        path = QtGui.QFileDialog.getExistingDirectory(
            self, "Export Destination", QtCore.QDir.currentPath())
        image = cv2.imread(self.filename)

        for i, item in enumerate(self.view.items):
            # b = item.boundingRect()
            b = item._rect
            print b
            x, y, w, h = b.x(), b.y(), b.width(), b.height()
            extract = image[y:y+h, x:x+w]
            print extract.shape, i
            cv2.imwrite(os.path.join(path, "image%s.png" % i), extract)

    def select_all(self):
        for item in self.view.items:
            item.setSelected(True)

    def create_actions(self):
        self.open_action = QtGui.QAction(self.style().standardIcon(
                QtGui.QStyle.SP_DirIcon), "&Open Image", self, shortcut="ctrl+O",
                triggered=self.open)

        self.exit_action = QtGui.QAction("E&xit", self, shortcut="alt+f4",
                triggered=self.close)

        self.select_all_action = QtGui.QAction("Select &All", self, shortcut="ctrl+A",
                triggered=self.select_all)

        self.zoom_in_action = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_ArrowUp),
            "Zoom &In", self, enabled=False, shortcut="Ctrl++", triggered=self.zoom_in)

        self.zoom_out_action = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_ArrowDown),
            "Zoom &Out", self, enabled=False, shortcut="Ctrl+-", triggered=self.zoom_out)

        self.about_action = QtGui.QAction("&About", self, triggered=self.about)

        self.segment_action = QtGui.QAction(self.style().standardIcon(
                QtGui.QStyle.SP_ComputerIcon),
            "&Segment", self, shortcut="f5", enabled=False,
            statusTip="Segment",
            triggered=self.segment)

        self.save_action = QtGui.QAction(self.style().standardIcon(
                QtGui.QStyle.SP_DesktopIcon), 
            "&Save Boxes", self, shortcut="ctrl+s", enabled=False,
            statusTip="Save Boxes",
            triggered=self.save_boxes)

        self.import_action = QtGui.QAction(self.style().standardIcon(
                QtGui.QStyle.SP_DesktopIcon), 
            "&Import Boxes", self, shortcut="ctrl+i", enabled=False,
            statusTip="Import Boxes",
            triggered=self.import_boxes)

        self.export_action = QtGui.QAction(self.style().standardIcon(
                QtGui.QStyle.SP_FileIcon),
            "&Export Images...", self, shortcut="", enabled=False,
            statusTip="Export",
            triggered=self.export)

    def save_boxes(self):
        file_name, filtr = QtGui.QFileDialog.getSaveFileName(self,
                "QFileDialog.getSaveFileName()",
                self.file_name + ".csv",
                "All Files (*);;CSV Files (*.csv)", "", QtGui.QFileDialog.Options())
        if file_name:
            with open(file_name, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=' ')
                for item in self.view.items:
                    rect = item.rect()
                    box = [rect.left(), rect.top(), rect.width(), rect.height()]
                    # box = [float(value) for value in box]
                    width = self.image_item.pixmap().width()
                    height = self.image_item.pixmap().height()
                    box[0] /= width
                    box[1] /= height 
                    box[2] /= width 
                    box[3] /= height
                    writer.writerow(box)

    def import_boxes(self):
        files, filtr = QtGui.QFileDialog.getOpenFileNames(self,
                "QFileDialog.getOpenFileNames()", "../data",
                "All Files (*);;Text Files (*.csv)", "", QtGui.QFileDialog.Options())
        if files:
            width = self.image_item.pixmap().width()
            height = self.image_item.pixmap().height()
            for file_name in files:
                with open(file_name, 'r') as csvfile:
                    reader = csv.reader(csvfile, delimiter=' ')
                    for row in reader:
                        rect = [float(x) for x in row]
                        rect[0] *= width
                        rect[1] *= height 
                        rect[2] *= width 
                        rect[3] *= height
                        self.add_box(rect)

    def create_menus(self):
        self.toolbar = self.addToolBar("Edit")
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.segment_action)
        self.toolbar.addAction(self.zoom_in_action)
        self.toolbar.addAction(self.zoom_out_action)
        self.toolbar.addAction(self.save_action)
        self.toolbar.addAction(self.import_action)
        self.toolbar.addAction(self.export_action)
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.open_action)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.save_action)
        self.fileMenu.addAction(self.import_action)
        self.fileMenu.addAction(self.export_action)
 
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exit_action)

        self.viewMenu = QtGui.QMenu("&View", self)
        self.viewMenu.addAction(self.select_all_action)
        self.viewMenu.addAction(self.zoom_in_action)
        self.viewMenu.addAction(self.zoom_out_action)

        self.helpMenu = QtGui.QMenu("&Help", self)
        self.helpMenu.addAction(self.about_action)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)


    def keyPressEvent(self, event):
        return
        if event.key() == 16777216:
        # if event.key() == Qtcore.Qt.Key_Escape:
            sys.exit(1)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Inselect 0.1')
    if not arguments["--batch"]:
        print "Launching gui."
        app = QtGui.QApplication(sys.argv)
        # window = ImageViewer("../data/drawer.jpg")
        # window = ImageViewer("../data/Plecoptera_Accession_Drawer_4.jpg")
        window = ImageViewer()
        if arguments['<filename>']:
            window.open(arguments['<filename>']) 
        window.showMaximized()
        window.show()
        sys.exit(app.exec_())
    else:
        print "Batch processing mode"
        for root, dirs, files in os.walk(arguments["--batch"]):
            print "Processing", root
            for file_name in files:
                if is_image_file(file_name):
                    file_name = os.path.join(root, file_name)
                    image = cv2.imread(file_name)
                    height, width, _ = image.shape
                    print "Segmenting", file_name, image.shape
                    rects = segment_edges(image, variance_threshold=100, size_filter=1)
                    csv_file_name = file_name + '.csv'
                    print "Writing csv file", csv_file_name 
                    with open(csv_file_name, 'w') as csvfile:
                        writer = csv.writer(csvfile, delimiter=' ')
                        for box in rects:
                            box = [float(value) for value in box]
                            box[0] /= width
                            box[1] /= height 
                            box[2] /= width 
                            box[3] /= height
                            writer.writerow(box)
            if not arguments["--recursive"]:
                break