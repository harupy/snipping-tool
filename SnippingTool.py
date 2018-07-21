import tkinter as tk
import numpy as np
import cv2
from PIL import ImageGrab
from PyQt5 import QtWidgets, QtCore, QtGui
import SnippingMenu


class SnippingWidget(QtWidgets.QWidget):
    snips = []
    num_snip = 0

    def __init__(self):
        super().__init__()
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.is_snipping = False

    def start(self):
        self.is_snipping = True
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')
        print('Press q if you want to quit...')
        self.show()

    def paintEvent(self, event):
        if self.is_snipping:
            brush_color = (128, 128, 255, 100)
            lw = 3
            opacity = 0.3
        else:
            # reset points, so the rectangle won't show up again.
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0

        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        rect = QtCore.QRectF(self.begin, self.end)
        qp.drawRect(rect)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:
            print('Quit')
            self.close()
        event.accept()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        SnippingWidget.num_snip += 1
        self.is_snipping = False
        QtWidgets.QApplication.restoreOverrideCursor()
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        QtWidgets.QApplication.processEvents()
        img_name = 'snip{}.png'.format(SnippingWidget.num_snip)
        img.save(img_name)
        print(img_name, 'saved')
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        # add to the snips list the object that opens a window of the image
        SnippingWidget.snips.append(SnippingMenu.Menu(img, SnippingWidget.num_snip, (x1, y1, x2, y2)))


# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = SnippingWidget()
#     window.show()
#     app.aboutToQuit.connect(app.deleteLater)
#     sys.exit(app.exec_())
