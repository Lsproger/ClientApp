import socket
import threading
import os

from Requests import (ConnectToServer, SavePublicKey, GetPublicKey, Disconnect, RegisterListener)
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QPushButton, QMessageBox)
from Cryptography.Functions import generate_keys, get_secret
from KeySwapWindow import KeySwapWindow
from SendMessageWindow import SendMessageWindow
from Cryptography.Point import Point
from Cryptography.PSEC_KEM import decrypt


class MainWindow(QWidget):

    def getx(self): return self.__addwin  # методы для чтения,

    def setx(self, value): self.__addwin = value  # записи

    def delx(self): del self.__addwin  # удаления свойства

    addwin = property(getx, setx, delx, "Свойство 'addwin'.")  # определение свойства
    # ---конец описания свойства

    __lastusername = ''
    __port = 9090
    __username = ''
    __filename = os.getcwd() + '/Keys/{name}.txt'
    __public_key = Point(0, 0)
    __private_key = 0
    __server_ip = '127.0.0.1'
    __connect_status = 'Not connected'
    __ssocket = None
    __listener_sock = None
    __listener_port = 0

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        username_lbl = QLabel('Your name')
        server_ip_lbl = QLabel('Server ip:')
        connection = QLabel('Connection status:')

        public_key_lbl = QLabel('Your public:')
        private_key_lbl = QLabel('Your private:')
        guide = QLabel('You can use next functions:')

        connect_server_btn = QPushButton('Connect', self)
        gen_keys_btn = QPushButton('Generate keys', self)
        key_swap_btn = QPushButton('Diffie-Hellman', self)
        create_ds_btn = QPushButton('Create digital signature', self)
        psec2_btn = QPushButton('Send message using PSEK-KEM algorythm (One-time note)', self)

        self.username = QLineEdit(username_lbl)
        self.server_ip_edit = QLineEdit(self.__server_ip)
        self.connection_status_lbl = QLabel(self.__connect_status)
        self.public_key = QTextEdit('x: %s <br> y: %s' % (self.__public_key.x, self.__public_key.y))
        self.private_key = QLineEdit(str(self.__private_key))

        self.public_key.setReadOnly(False)
        self.private_key.setReadOnly(False)

        self.public_key.setToolTip('Generated public key. If empty - generate keys!')
        self.private_key.setToolTip('Generated private key. If empty - generate keys!')

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(username_lbl, 0, 0)
        grid.addWidget(self.username, 0, 1)

        grid.addWidget(server_ip_lbl, 1, 0)
        grid.addWidget(self.server_ip_edit, 1, 1, 1, 1)
        grid.addWidget(connect_server_btn, 1, 2)

        grid.addWidget(connection, 2, 0)
        grid.addWidget(self.connection_status_lbl, 2, 1, 1, 2)

        grid.addWidget(public_key_lbl, 3, 0)
        grid.addWidget(self.public_key, 3, 1, 1, 2)

        grid.addWidget(private_key_lbl, 4, 0)
        grid.addWidget(self.private_key, 4, 1, 1, 2)

        grid.addWidget(guide, 5, 0, 1, 2)

        grid.addWidget(gen_keys_btn, 6, 0)
        grid.addWidget(key_swap_btn, 6, 1)
        grid.addWidget(create_ds_btn, 6, 2)

        grid.addWidget(psec2_btn, 7, 0, 1, 3)

        self.setLayout(grid)

        connect_server_btn.clicked.connect(self.ConnectServerBtnClicked)
        gen_keys_btn.clicked.connect(self.GenKeysBtnClicked)
        key_swap_btn.clicked.connect(self.KeySwapBtnClicked)
        psec2_btn.clicked.connect(self.PSEC2BtnClicked)

        self.setGeometry(300, 300, 650, 100)
        self.setWindowTitle('Elliptic cryptographer')
        self.show()

    def LoadKeys(self):
        try:
            self.LoadPublicKey()
            self.LoadPrivateKey()

        except Exception:
            self.__public_key = Point(0, 0)
            self.__private_key = 0
        # Implementation of loading keys from server

    def LoadPrivateKey(self):
        f = open(self.__filename.format(name=self.__username), 'r')
        self.__private_key = f.read()
        f.close()

    def LoadPublicKey(self):
        x, y = GetPublicKey(self.__username, self.__ssocket)
        self.__public_key = Point(x, y)

    def ConnectServerBtnClicked(self):
        if self.__ssocket is not None:
            Disconnect(self.__lastusername, self.__ssocket)
            self.__ssocket = None

        self.__username = self.username.text()
        self.__lastusername = self.__username

        if self.__username == '':
            return 0

        self.__server_ip = self.server_ip_edit.text()
        self.__ssocket = ConnectToServer(self.__username, self.__server_ip, self.__port)

        if self.__ssocket is not None:
            self.__connect_status = 'Connected'
            self.LoadKeys()

            self.__listener_sock, self.__listener_port = self.CreateListener()
            RegisterListener(self.__ssocket, self.__listener_port)
            self.StartListen(self.__listener_sock)
        else:
            self.__connect_status = 'Not connected! Address error!'
        self.UpdateLables()

    def SavePrivateKey(self, key):
        try:
            f = open(self.__filename.format(name=self.__username), 'w')
            f.write(str(key))
            f.close()
        except Exception:
            print('file not opened on way ' + self.__filename.format(name=self.__username))
            f.close()

    def SaveKeys(self, private_key, public_key, csocket: socket):
        SavePublicKey(public_key, csocket)
        self.SavePrivateKey(private_key)
        return True

    def GenKeysBtnClicked(self):
        try:
            sock = self.__ssocket
            if sock is not None:
                self.__private_key, self.__public_key = generate_keys()
                key = str(self.__public_key.x) + ' ' + str(self.__public_key.y)
                isSaved = self.SaveKeys(str(self.__private_key), key, self.__ssocket)

            self.UpdateLables()
        except Exception as e:
            self.UpdateLables()

    def KeySwapBtnClicked(self):
        if self.__connect_status == 'Not connected':
            return 0
        self.addwin = KeySwapWindow(
            self.__server_ip, self.__ssocket, self.__username, self.__public_key, self.__private_key)

    def PSEC2BtnClicked(self):
        if self.__connect_status == 'Not connected':
            return 0
        self.addwin = SendMessageWindow(
            self.__server_ip, self.__ssocket, self.__username, self.__public_key, self.__private_key)


    def UpdateLables(self):
        self.private_key.setText(str(self.__private_key))
        self.public_key.setText('x: %d <br> y: %d' % (self.__public_key.x, self.__public_key.y))
        self.connection_status_lbl.setText(self.__connect_status)

    def StartListen(self, sock: socket):
        listener = threading.Thread(target=self.Listen, args=(sock, None))
        listener.setDaemon(True)
        listener.start()

    def Listen(self, sock: socket, param):
        try:
            while 1:
                conn, addr = sock.accept()
                service = conn.recv(1024)
                if service == b'SWAP':
                    conn.send(b'SWAP')
                    client_name = conn.recv(1024).decode(encoding='utf-8')
                    print('send SWAP')
                    partner_public_mas = GetPublicKey(client_name, self.__ssocket)
                    print('Get public key')
                    partner_public = Point(partner_public_mas[0], partner_public_mas[1])
                    secret = get_secret(int(self.__private_key), partner_public)
                    msgtext = self.__username + ', your shared key with %s is:\n' % client_name + str(secret.x)
                    reply = QMessageBox.question(self, 'Shared key', msgtext, QMessageBox.Yes,
                                                 QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        print('Yes')
                    conn.close()
                if service == b'MSG':
                    conn.send(b'MSG')
                    params = conn.recv(4096)
                    conn.send(b'Ok')
                    c_text = conn.recv(1024)
                    msg, sender = FormatRecievedMessageFtomBytes(params, c_text, int(self.__private_key))
                    text_to_show = self.__username + ', you have recieved message from %s:\n %s' % (sender, msg)
                    reply = QMessageBox.question(self, 'Message', text_to_show, QMessageBox.Yes,
                                                 QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        print('Yes')
                    conn.close()
        except Exception as e:
                print('Exception on MessageBox', e.__repr__(), e.__str__())

    def CreateListener(self):
        sock = socket.socket()
        port = 50000
        while 1:
            try:
                sock.bind(('', port))
                sock.listen(1)
                break
            except OSError:
                port = port + 1
        return sock, port


def FormatRecievedMessageFtomBytes(params, c_text, private):
    from_name, s, Tx, Ty = params.decode(encoding='utf-8').split(' ')
    T = Point(int(Tx), int(Ty))
    decoded_s = int(s)
    sender = from_name
    msg_text = decrypt(private, decoded_s, T, c_text)
    return msg_text.decode(encoding='utf-8'), sender
