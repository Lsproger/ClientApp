import socket


def ConnectToServer(username, serv_addr, port):
    try:
        sock = socket.socket()
        sock.connect((serv_addr, port))
        sock.send(bytes(username, 'utf-8'))
        resp = sock.recv(1024)
        if resp == b'OK':
            return sock
        else:
            sock.close()
            return None
    except Exception:
        sock.close()
        return None


def RegisterListener(csocket: socket, port):
    csocket.send(server_services['RegisterListener'])
    resp = csocket.recv(1024)
    if resp == server_services['RegisterListener']:
        csocket.send(bytes(str(port), 'utf-8'))
        response = csocket.recv(1024)
        if response == b'OK':
            return True
        else:
            return False


def Disconnect(username, csocket: socket):
    csocket.send(server_services['Disconnect'])
    csocket.close()


def GetPublicKey(username, csocket: socket):
    try:
        csocket.send(server_services['GetPublicKey'])
        resp = csocket.recv(1024)
        if resp == server_services['GetPublicKey']:
            csocket.send(bytes(username, 'utf-8'))
            key = csocket.recv(1024).decode(encoding='utf-8').split(' ')
        else:
            key = 0, 0
    except Exception:
        return 0, 0
    return int(key[0]), int(key[1])


def SavePublicKey(key, csocket: socket):
    csocket.send(server_services['SaveKey'])
    csocket.send(bytes(key, 'utf-8'))
    response = csocket.recv(1024)
    if response == b'OK':
        return True
    else:
        return False


server_services = {'SaveKey': b'SAVE_KEY',
                   'GetPublicKey': b'GET_KEY',
                   'DiffieHellman': b'DIFFIE-HELLMAN',
                   'SendMessage': b'SEND_MESSAGE',
                   'Disconnect': b'DISCONNECT',
                   'RegisterListener': b'REGISTER_LISTENER'}
