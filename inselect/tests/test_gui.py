import unittest
from pathlib import Path

from PySide import QtCore
from PySide.QtGui import QApplication
from PySide.QtTest import QTest

import inselect
from inselect.gui.app import InselectMainWindow
from inselect.gui.roles import RectRole


TESTDATA = Path(__file__).parent / 'test_data'


class TestDocument(unittest.TestCase):
    def _test_closed(self):
        self.assertEqual('inselect', window.windowTitle())
        self.assertEqual(0, window.model.rowCount())
        self.assertFalse(window.toggle_segment_action.isEnabled())
        self.assertFalse(window.segment_action.isEnabled())
        self.assertFalse(window.zoom_in_action.isEnabled())
        self.assertFalse(window.zoom_out_action.isEnabled())
        self.assertFalse(window.save_action.isEnabled())
        self.assertFalse(window.close_action.isEnabled())

    def test_open(self):
        window.close_document()
        self._test_closed()

        window.open_document(TESTDATA / 'test_segment.inselect')
        self.assertEqual(5, window.model.rowCount())
        self.assertEqual('inselect [test_segment]', window.windowTitle())
        self.assertFalse(window.toggle_segment_action.isEnabled())
        self.assertTrue(window.segment_action.isEnabled())
        self.assertTrue(window.zoom_in_action.isEnabled())
        self.assertTrue(window.zoom_out_action.isEnabled())
        self.assertTrue(window.save_action.isEnabled())
        self.assertTrue(window.close_action.isEnabled())

        window.close_document()
        self._test_closed()

    # TODO LH Test persist, image file missing, with and without thumbnail



class TestSegment(unittest.TestCase):
    def _segment(self):
        # Wait for the segmentation worker thread to complete and for the main
        # window to receive the boxes.
        # http://stackoverflow.com/questions/9712461/pyside-wait-for-signal-from-main-thread-in-a-worker-thread
        class SignalReceiver(QtCore.QObject):
            def __init__(self):
                super(self.__class__, self).__init__()
                self.eventLoop = QtCore.QEventLoop(self)

            def stop_waiting(self, rects, display):
                self.eventLoop.exit()

            def wait_for_input(self):
                self.eventLoop.exec_()

        window.segment()
        signalReceiver = SignalReceiver()
        window.worker.results.connect(signalReceiver.stop_waiting)
        window.worker.wait()
        signalReceiver.wait_for_input()

    def test_segment(self):
        window.close_document()
        window.open_document(TESTDATA / 'test_segment.inselect')

        self.assertFalse(window.toggle_segment_action.isEnabled())
        self.assertEqual(5, window.model.rowCount())
        indexes = [window.model.index(r, 0) for r in xrange(0, window.model.rowCount())]
        expected = [window.model.data(i, RectRole) for i in indexes]

        # TODO LH Rewrite this for new model-view architecture
        window.view.delete_all_boxes()
        self.assertEqual(0, window.model.rowCount())

        self._segment()
        self.assertTrue(window.toggle_segment_action.isEnabled())

        self.assertEqual(5, window.model.rowCount())
        actual = [b.boundingRect() for b in window.model.rowCount()]
        self.assertEqual(expected, actual)

    def test_subsegment(self):
        window.close_document()
        window.open_document(TESTDATA / 'test_subsegment.inselect')

        self.assertFalse(window.toggle_segment_action.isEnabled())
        self.assertEqual(1, window.model.rowCount())

        # TODO LH Add seed points and test subselect


# TODO LH Something better than this crude solution
app = window = None
def setUpModule():
    global app, window
    assert(not app and not window)
    inselect.settings.init()
    app = QApplication([])
    window = InselectMainWindow(app)


def tearDownModule():
    global app, window
    assert(app and window)
    window.close()
    app.quit()
    window = app = None


if __name__=='__main__':
    unittest.main()
