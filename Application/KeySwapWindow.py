import socket
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication, QPushButton)
import time

from Application.Requests import server_services


class KeySwapWindow(QWidget):

    __partner_status = 'offline'
    __partner_addr = 'None'
    __partner_port = 'None'

    def __init__(self, server_ip, sock, username):
        super(KeySwapWindow, self).__init__()
        # запускаем метод рисующий виджеты окна
        self.__sock = sock
        self.__username = username
        self.initUI(server_ip, sock, username)

    def initUI(self, server_ip, sock: socket, username):

        server_ip_lbl = QLabel('Server ip: ' + str(server_ip))
        my_name_lbl = QLabel('Your username: ' + username)
        partner_connection = QLabel('Partner connection status:')
        partner_name = QLabel("Your partner's name")

        partner_ip = QLabel('Partner ip: ')
        partner_port = QLabel('Partner port: ')

        self.partner_ip_lbl = QLabel(self.__partner_addr)
        self.partner_port_lbl = QLabel(self.__partner_addr)

        self.partner_name_edit = QLineEdit()
        self.partner_connection_status_lbl = QLabel('Offline')
        connect_partner_btn = QPushButton('connect', self)
        connect_partner_btn.clicked.connect(self.ConnectPartnerBtnClicked)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(server_ip_lbl, 0, 0, 1, 3)

        grid.addWidget(my_name_lbl, 1, 0, 1, 3)

        grid.addWidget(partner_name, 2, 0)
        grid.addWidget(self.partner_name_edit, 2, 1, 1, 2)

        grid.addWidget(partner_connection, 3, 0)
        grid.addWidget(self.partner_connection_status_lbl, 3, 1)
        grid.addWidget(connect_partner_btn, 3, 2)

        grid.addWidget(partner_ip, 4, 0)
        grid.addWidget(self.partner_ip_lbl, 4, 1)

        grid.addWidget(partner_port, 5, 0)
        grid.addWidget(self.partner_port_lbl, 5, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 100, 100)
        self.setWindowTitle('Diffie-Hellman key swap')
        self.show()


    def ConnectPartnerBtnClicked(self):
        self.__sock.send(server_services['DiffieHellman'])
        resp = self.__sock.recv(1024)
        if resp == server_services['DiffieHellman']:
            self.__sock.send(
                bytes(self.partner_name_edit.text(), 'utf-8'))
            resp = self.__sock.recv(1024)
            if resp == b'Fail':
                self.partner_connection_status_lbl.setText('Not connected')
                return 0
            resp = resp.decode(encoding='utf-8').split(' ')
            self.__partner_addr, self.__partner_port = resp[0], resp[1]
            self.UpdateLables(True)


    def UpdateLables(self, isConnected):
        if isConnected:
            self.__partner_status = 'Online'
        else:
            self.__partner_status = 'Offline'

        self.partner_connection_status_lbl.setText(self.__partner_status)
        self.partner_ip_lbl.setText(self.__partner_addr)
        self.partner_port_lbl.setText(self.__partner_port)



