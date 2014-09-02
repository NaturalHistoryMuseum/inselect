import numpy as np
from PySide import QtCore, QtGui

__all__ = ['GraphicsView', 'GraphicsScene', 'BoxResizable']


class GraphicsView(QtGui.QGraphicsView):
    def __init__(self, parent=None, wireframe_mode=False):
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

    # Qt-specific methods
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            for box in list(self.items):
                # if hasattr(box, "isSelected") and box.isSelected():
                if box.isSelected():
                    self.remove_item(box)

        QtGui.QGraphicsView.keyPressEvent(self, event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MidButton:
            self.mouse_press_pos = QtCore.QPoint(event.pos())

            x = self.horizontalScrollBar().value()
            y = self.verticalScrollBar().value()
            self.scrollBarValuesOnMousePress.setX(x)
            self.scrollBarValuesOnMousePress.setY(y)

            event.accept()
            return

        elif event.button() == QtCore.Qt.LeftButton and not self.is_resizing:
            # reveal hidden boxes, smallest to the front
            if self.wireframe_mode:
                e = self.mapToScene(event.pos().x(), event.pos().y())
                items = self.scene().items(e)
                items = [item for item in items if item in self.items]
                if items:
                    items.sort(lambda a, b: cmp(a.boundingRect().width() *
                                                a.boundingRect().height(),
                                                b.boundingRect().width() *
                                                b.boundingRect().height()))
                    for item in self.items:
                        item.setZValue(1000)
                    items[0].setZValue(1001)
                    self.move_box.setZValue(1002)
        elif event.button() == QtCore.Qt.RightButton:
            self.box_create_start = QtCore.QPoint(event.pos())
            return
        QtGui.QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        QtGui.QGraphicsView.mouseMoveEvent(self, event)
        if not self.box_create_start.isNull():
            self.move_box.setVisible(True)
            s = self.mapToScene(self.box_create_start.x(),
                                self.box_create_start.y())
            pos = event.pos()
            e = self.mapToScene(pos.x(), pos.y())
            w, h = (e.toPoint().x() - s.toPoint().x(), e.toPoint().y() -
                    s.toPoint().y())
            self.move_box.setPos(s)
            self.move_box._rect = QtCore.QRect(0, 0, w, h)
            self.move_box._boundingRect = QtCore.QRect(0, 0, w, h)
            self.scene().update()

        if self.mouse_press_pos.isNull():
            event.ignore()
            return

        x = self.scrollBarValuesOnMousePress.x() - event.pos().x() + \
            self.mouse_press_pos.x()
        y = self.scrollBarValuesOnMousePress.y() - event.pos().y() + \
            self.mouse_press_pos.y()

        self.horizontalScrollBar().setValue(x)
        self.horizontalScrollBar().update()

        self.verticalScrollBar().setValue(y)
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
                box = BoxResizable(QtCore.QRectF(s.x(), s.y(), w, h),
                                   scene=self.scene())
                if not self.wireframe_mode:
                    b = box.boundingRect()
                    box.setZValue(max(1000, 1E9 - b.width() * b.height()))
                    box.updateResizeHandles()
                self.add_item(box)
        if self.move_box:
            self.move_box.setVisible(False)
            self.box_create_start = QtCore.QPoint()


class GraphicsScene(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
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
    def __init__(self, rect, parent=None, color=QtCore.Qt.blue,
                 transparent=False, scene=None):
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
        self.setZValue(max(1000, 1E9 - b.width() * b.height()))

    def hoverMoveEvent(self, event):
        if any(self.top_left_handle.contains(event.pos()),
               self.bottom_right_handle.contains(event.pos())):

            self.setCursor(QtCore.Qt.SizeFDiagCursor)
            self.scene().view.is_resizing = True

        elif (self.top_right_handle.contains(event.pos()) or
              self.bottom_left_handle.contains(event.pos())):

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
        Capture mouse press events and find where the mosue was pressed
        on the object.
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
        def delta():
            return self.mouse_press_pos - self.mouse_move_pos

        self.mouse_move_pos = event.scenePos()
        if self.mouse_is_pressed:
            if self.mouse_press_area:
                self.prepareGeometryChange()
                # Move top left corner
                if self.mouse_press_area == 'topleft':
                    self._rect.setTopLeft(
                        self.rect_press.topLeft() - delta())
                # Move top right corner
                elif self.mouse_press_area == 'topright':
                    self._rect.setTopRight(
                        self.rect_press.topRight() - delta())
                # Move bottom left corner
                elif self.mouse_press_area == 'bottomleft':
                    self._rect.setBottomLeft(
                        self.rect_press.bottomLeft() - delta())
                # Move bottom right corner
                elif self.mouse_press_area == 'bottomright':
                    self._rect.setBottomRight(
                        self.rect_press.bottomRight() - delta())

                event.accept()
                self.updateResizeHandles()

                return

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

        self.offset = self.handle_size * \
            (self._scene.view.mapToScene(1, 0) -
             self._scene.view.mapToScene(0, 1)).x()
        self._boundingRect = self._rect.adjusted(-self.offset, -self.offset,
                                                 self.offset, self.offset)

        self.offset1 = (self._scene.view.mapToScene(1, 0) -
                        self._scene.view.mapToScene(0, 1)).x()
        self._innerRect = self._rect.adjusted(self.offset1, self.offset1,
                                              -self.offset1, -self.offset1)

        b = self._boundingRect
        self.top_left_handle = QtCore.QRectF(b.topLeft().x(),
                                             b.topLeft().y(),
                                             2*self.offset,
                                             2*self.offset)

        self.top_right_handle = QtCore.QRectF(b.topRight().x() - 2*self.offset,
                                              b.topRight().y(),
                                              2*self.offset,
                                              2*self.offset)

        self.bottom_left_handle = QtCore.QRectF(
            b.bottomLeft().x(),
            b.bottomLeft().y() - 2*self.offset,
            2*self.offset,
            2*self.offset)

        self.bottom_right_handle = QtCore.QRectF(
            b.bottomRight().x() - 2*self.offset,
            b.bottomRight().y() - 2*self.offset,
            2*self.offset,
            2*self.offset)

        if self.isSelected():
            self.setZValue(1E9)
        else:
            self.setZValue(max(1000, 1E9 - b.width() * b.height()))

    def map_rect_to_scene(self, map_rect):
        rect = map_rect
        target_rect = QtCore.QRectF(rect)
        t = rect.topLeft()
        b = rect.bottomRight()
        target_rect.setTopLeft(QtCore.QPointF(t.x() + self.pos().x(),
                                              t.y() + self.pos().y()))
        target_rect.setBottomRight(QtCore.QPointF(b.x() + self.pos().x(),
                                                  b.y() + self.pos().y()))
        return target_rect

    def paint(self, painter, option, widget):
        """
        Paint Widget
        """
        # Paint rectangle
        if self.isSelected():
            color = QtCore.Qt.red
        else:
            color = self.color

        painter.setPen(QtGui.QPen(color, 0, QtCore.Qt.SolidLine))
        painter.drawRect(self._rect)

        if not self.transparent:
            rect = self._innerRect
            if rect.width() > 0 and rect.height() != 0:
                # normalize negative widths and heights, during resizing
                x1, y1 = rect.x(), rect.y()
                x2, y2 = rect.x() + rect.width(), rect.y() + rect.height()
                rect = QtCore.QRectF(min(x1, x2), min(y1, y2),
                                     abs(rect.width()), abs(rect.height()))
                target_rect = self.map_rect_to_scene(rect)
                painter.drawPixmap(rect, self.scene().image.pixmap(),
                                   target_rect)

        # If mouse is over, draw handles
        if self.mouseOver:
            painter.drawRect(self.top_left_handle)
            painter.drawRect(self.top_right_handle)
            painter.drawRect(self.bottom_left_handle)
            painter.drawRect(self.bottom_right_handle)
