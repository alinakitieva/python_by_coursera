import socket
import time
import bisect


class ClientError(Exception):
    pass


class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        try:
            self.connection = socket.create_connection(host, port)
        except socket.error:
            raise ClientError

    def read_data(self):
        data = b""
        while not data.endswith(b"\n\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error:
                raise ClientError
        return data.decode('utf-8')

    def send_data(self, data):
        try:
            self.connection.sendall(data)
        except socket.error:
            raise ClientError

    def get(self, key):
        request = f'get {key}\n'.encode()
        self.send_data(request)
        data = self.read_data()
        d = {}
        status, payload = data.split('\n', 1)
        payload.strip()
        if status != 'ok':
            raise ClientError
        if payload == '':
            return d
        try:
            for row in payload.splitlines():
                key, value, timestamp = row.split()
                if key not in data:
                    data[key] = []
                bisect.insort(data[key], (int(timestamp), float(value)))
        except Exception:
            raise ClientError

        return data

    def put(self, key, value, timestamp=None):
        timestamp = timestamp or int(time.time())
        request = f'put {key} {value} {timestamp}\n'.encode()
        self.send_data(request)
        data = self.read_data()
        if data == 'ok\n\n':
            return
        raise ClientError

    def close(self):

        try:
            self.connection.close()
        except socket.error:
            raise ClientError
