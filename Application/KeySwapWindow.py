import socket
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication, QPushButton)


class KeySwapWindow(QWidget):

    def __init__(self, server_ip, sock, username):
        super(KeySwapWindow, self).__init__()
        # запускаем метод рисующий виджеты окна

        self.initUI(server_ip, sock, username)

    def initUI(self, server_ip, sock: socket, username):

        server_ip_lbl = QLabel('Server ip: ' + str(server_ip))
        my_name_lbl = QLabel('Your username: ' + username)
        partner_connection = QLabel('Connection status:')
        partner_name = QLabel("Your partner's name")

        partner_name_edit = QTextEdit()
        partner_connection_status_lbl = QLabel('Not connected')
        refresh_partner_connection_status_btn = QPushButton('refresh', self)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(server_ip_lbl, 0, 0, 1, 3)

        grid.addWidget(my_name_lbl, 1, 0, 1, 3)

        grid.addWidget(partner_name, 2, 0)
        grid.addWidget(partner_name_edit, 2, 1, 1, 2)

        grid.addWidget(partner_connection, 3, 0)
        grid.addWidget(partner_connection_status_lbl, 3, 1)
        grid.addWidget(refresh_partner_connection_status_btn, 3, 2)

        self.setLayout(grid)

        self.setGeometry(300, 300, 100, 100)
        self.setWindowTitle('Diffie-Hellman key swap')
        self.show()


def ClientConnectionsListener(sock: socket):
    conn, addr = sock.accept()

