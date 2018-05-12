import sys

from PyQt5.QtWidgets import (QWidget, QLabel,
                             QGridLayout, QApplication)


class MsgBox(QWidget):

    def __init__(self, msg_text):
        super(MsgBox, self).__init__()
        # запускаем метод рисующий виджеты окна
        self.initUI(msg_text)

    def initUI(self, msg_text):
        shared_key_lbl = QLabel(msg_text)

        grid = QGridLayout()

        grid.addWidget(shared_key_lbl, 0, 0)

        self.setLayout(grid)

        self.setGeometry(300, 300, 100, 100)
        self.setWindowTitle('Shared key!')
        self.show()


def ShowMsg(msg_text):
    app = QApplication(sys.argv)
    ex = MsgBox(msg_text)
    sys.exit(app.exec_())