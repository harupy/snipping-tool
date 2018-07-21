import sys
from PyQt5 import QtWidgets

from SnippingTool import SnippingWidget


class Menu(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        newAct = QtWidgets.QAction('New', self)
        newAct.setShortcut('Ctrl+N')
        newAct.triggered.connect(self.new_image_window)

        exitAct = QtWidgets.QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.statusBar()
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(newAct)
        toolbar.addAction(exitAct)

        self.snippingTool = SnippingWidget()

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

    def new_image_window(self):
        self.snippingTool.start()

    # quitting in the main menu will close all windows as well.
    def closeEvent(self, event):
        for snip in self.snippingTool.snips:
            snip.close()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Menu()

    sys.exit(app.exec_())
