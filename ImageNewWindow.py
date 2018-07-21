from PyQt5.QtWidgets import QWidget, QLabel, QMainWindow, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage


class NewImage(QMainWindow):
    # Store configuration settings (pen width, and maybe more)
    config = {
        # Drawing options.
        'size': 1
    }

    # Modes available
    MODES = [
        'marker', 'pen',
        'eraser', 'brush'
    ]

    def __init__(self, numpy_image, snip_number):
        super().__init__()
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

    @staticmethod
    def convert_numpy_img_to_qpixmap(np_img):
        height, width, channel = np_img.shape
        bytesPerLine = 3 * width
        return QPixmap(QImage(np_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped())
