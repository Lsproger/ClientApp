import socket
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QGridLayout, QPushButton, QMessageBox, QTextEdit)

from Cryptography.Point import Point
from Requests import server_services, GetPublicKey
from Cryptography.Functions import get_secret


class SendMessageWindow(QWidget):

    __partner_status = 'offline'
    __partner_addr = 'None'
    __partner_port = 'None'
    __partner_name = 'None'
    __partner_public = None
    __private = None
    __public = None

    def __init__(self, server_ip, sock, username, public: Point, private):
        super(SendMessageWindow, self).__init__()
        # запускаем метод рисующий виджеты окна
        self.__sock = sock
        self.__username = username
        self.__private = private
        self.__public = public
        self.initUI(server_ip, sock, username)

    def initUI(self, server_ip, sock: socket, username):

        server_ip_lbl = QLabel('Server ip: ' + str(server_ip))
        my_name_lbl = QLabel('Your username: ' + username)
        partner_connection = QLabel('Partner connection status:')
        partner_name = QLabel("Your partner's name")
        self.partner_name_edit = QLineEdit()

        msglbl = QLabel('Input message text: ')
        self.msg_edit = QTextEdit()

        self.send_msg_btn = QPushButton('send', self)

        self.send_msg_btn.clicked.connect(self.ConnectPartnerBtnClicked)

        shared_key_lbl = QLabel('Your shared key: ')

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(server_ip_lbl, 0, 0, 1, 2)

        grid.addWidget(my_name_lbl, 1, 0, 1, 2)

        grid.addWidget(partner_name, 2, 0)
        grid.addWidget(self.partner_name_edit, 2, 1)

        grid.addWidget(msglbl, 3, 0)
        grid.addWidget(self.msg_edit, 3, 1)

        grid.addWidget(self.send_msg_btn, 4, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 100, 100)
        self.setWindowTitle('Send message')
        self.show()

    def ConnectPartnerBtnClicked(self):
        self.__sock.send(server_services['DiffieHellman'])
        resp = self.__sock.recv(1024)
        if resp == server_services['DiffieHellman']:
            self.__partner_name = self.partner_name_edit.text()
            self.__sock.send(
                bytes(self.__partner_name, 'utf-8'))
            resp = self.__sock.recv(1024)
            if resp == b'Fail':
                self.partner_connection_status_lbl.setText('Not connected')
                return 0
            resp = resp.decode(encoding='utf-8').split(' ')
            self.__partner_addr, self.__partner_port = resp[0], resp[1]
            self.UpdateLables(True)

    def StartSwapBtnClicked(self):
        try:
            sock = socket.socket()
            sock.connect((str(self.__partner_addr), int(self.__partner_port)))
            print('connected to partner', sock)
            sock.send(bytes(self.__username, 'utf-8'))
            # sock.send(b'SWAP')
            print('sended name & swap')
            resp = sock.recv(1024)
            if resp == b'SWAP':
                partner_public = GetPublicKey(self.__partner_name, self.__sock)
                self.__partner_public = Point(partner_public[0], partner_public[1])
                secret = get_secret(int(self.__private), self.__partner_public)
                print(secret)
                self.ShowDialog(secret, self.__username)
        except ConnectionRefusedError:
            print('Connection refused')

    def ShowDialog(self, shared_key, name):
        msg = name + ', your shared key is:\n' + str(shared_key.x)
        reply = QMessageBox.question(self, 'Shared key', msg, QMessageBox.Yes,
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            print('Yes')
        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Information)
        #
        # msg.setText(str(shared_key.x))
        # msg.setInformativeText(name + ", this is your shared key. Save this info!")
        # msg.setWindowTitle("Shared key")
        # msg.setDetailedText("It will disappear if you close!")
        # msg.setStandardButtons(QMessageBox.Ok)
        # msg.exec_()

    def UpdateLables(self, isConnected):
        if isConnected:
            self.__partner_status = 'Online'
        else:
            self.__partner_status = 'Offline'

        self.partner_connection_status_lbl.setText(self.__partner_status)
        self.partner_ip_lbl.setText(self.__partner_addr)
        self.partner_port_lbl.setText(self.__partner_port)
        self.start_swap_btn.show()



