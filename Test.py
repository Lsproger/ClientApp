import sys

from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton, QGridLayout


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.but = QPushButton('Clickme')
        self.but.clicked.connect(self.MakeSomething)
        grid = QGridLayout()
        grid.addWidget(self.but)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Message box')
        self.setLayout(grid)
        self.show()

    def MakeSomething(self):
        x = 5
        print(x)
        about = QMessageBox.about(self, 'Message', "This is message")


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())