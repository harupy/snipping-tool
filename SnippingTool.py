import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from PIL import ImageGrab
import numpy as np
import cv2

from ImageNewWindow import NewImage


class SnippingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.num_snip = 0
        self.is_snipping = False
        self.snips = []

    def start(self):
        self.is_snipping = True
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')
        print('Press q if you want to quit...')
        self.show()

    def paintEvent(self, event):
        print("in draw event")
        if self.is_snipping:
            brush_color = (128, 128, 255, 100)
            lw = 3
            opacity = 0.3
        else:
            # reset points, so the triangle won't
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
        #print("mouse press event!")
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        # self.close()

        print("mouse release event!")
        self.num_snip += 1
        self.is_snipping = False
        QtWidgets.QApplication.restoreOverrideCursor()
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.repaint()
        QtWidgets.QApplication.processEvents()
        img_name = 'snip{}.png'.format(self.num_snip)
        img.save(img_name)
        print(img_name, 'saved')
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        self.snips.append(NewImage(img, self.num_snip))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SnippingWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
