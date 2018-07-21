import sys
from PyQt5.QtWidgets import QAction, QWidget, QLabel, QMainWindow, QVBoxLayout, QApplication
from PyQt5.QtGui import QPixmap, QImage
import SnippingTool


class Menu(QMainWindow):

    # The first initialization will always be without a snip, so put None in both arguments.
    # numpy_image is the desired image we want to display given as a numpy array.
    def __init__(self, numpy_image=None, snip_number=None, start_position=(300, 300, 350, 250)):
        super().__init__()
        newAct = QAction('New', self)
        newAct.setShortcut('Ctrl+N')
        newAct.triggered.connect(self.new_image_window)

        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.statusBar()
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(newAct)
        toolbar.addAction(exitAct)

        self.snippingTool = SnippingTool.SnippingWidget()
        self.setGeometry(*start_position)
        self.setWindowTitle('Snipping Tool')

        # From the second initialization, both arguments will be valid
        if numpy_image is not None and snip_number is not None:
            self.setWindowTitle("Snip #{0}".format(snip_number))
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)

            lay = QVBoxLayout(self.central_widget)
            label = QLabel(self)
            pixmap = self.convert_numpy_img_to_qpixmap(numpy_image)
            label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            lay.addWidget(label)

        self.show()

    # snippingTool.start() will open a new window, so if this is the first snip, close the first window.
    def new_image_window(self):
        if not self.snippingTool.snips:
            self.close()
        self.snippingTool.start()


    @staticmethod
    def convert_numpy_img_to_qpixmap(np_img):
        height, width, channel = np_img.shape
        bytesPerLine = 3 * width
        return QPixmap(QImage(np_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = Menu()
    sys.exit(app.exec_())
