import sys

from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtWidgets import QAction, QWidget, QLabel, QMainWindow, QVBoxLayout, QApplication, QPushButton, QMenu
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen

import SnippingTool



class Menu(QMainWindow):

    # The first initialization will always be without a snip, so put None in both arguments.
    # numpy_image is the desired image we want to display given as a numpy array.
    def __init__(self, numpy_image=None, snip_number=None, start_position=(300, 300, 350, 250)):
        super().__init__()

        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.red
        self.lastPoint = QPoint()

        newAct = QAction('New', self)
        newAct.setShortcut('Ctrl+N')
        newAct.setStatusTip('Snip!')
        newAct.triggered.connect(self.new_image_window)

        colorButton = QPushButton("Colors")
        menu = QMenu()
        menu.addAction("Red")
        menu.addAction("Black")
        menu.addAction("Blue")
        colorButton.setMenu(menu)
        menu.triggered.connect(lambda action: change_color(action.text()))

        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(newAct)
        self.toolbar.addWidget(colorButton)
        self.toolbar.addAction(exitAct)

        self.snippingTool = SnippingTool.SnippingWidget()
        self.setGeometry(*start_position)

        # From the second initialization, both arguments will be valid
        if numpy_image is not None and snip_number is not None:
            self.image = self.convert_numpy_img_to_qpixmap(numpy_image)
            self.setWindowTitle("Snip #{0}".format(snip_number))
        else:
            self.image = QPixmap("background.PNG")
            self.setWindowTitle("Snipping Tool")

        self.resize(self.image.width(), self.image.height() + self.toolbar.height())
        self.show()

        def change_color(new_color):
            self.brushColor = eval("Qt.{0}".format(new_color.lower()))

    # snippingTool.start() will open a new window, so if this is the first snip, close the first window.
    def new_image_window(self):
        if not self.snippingTool.snips:
            self.close()
        self.snippingTool.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = QRect(0,  self.toolbar.height(), self.image.width(), self.image.height())
        painter.drawPixmap(rect, self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos() - QPoint(0, self.toolbar.height())

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos() - QPoint(0, self.toolbar.height()))
            self.lastPoint = event.pos() - QPoint(0, self.toolbar.height())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    @staticmethod
    def convert_numpy_img_to_qpixmap(np_img):
        height, width, channel = np_img.shape
        bytesPerLine = 3 * width
        return QPixmap(QImage(np_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped())




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec_())
