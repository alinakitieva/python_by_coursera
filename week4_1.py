import os.path
import tempfile
import random
import string


class File:
    def __init__(self, path):
        self.path = path
        if not os.path.isfile(self.path):
            open(self.path, 'w').close()
        self.current = 0

    def __str__(self):
        return self.path

    def __add__(self, file2):
        new_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))+".txt"
        new_path = os.path.join(tempfile.gettempdir(), new_name)
        new_file = File(new_path)
        new_file.write(self.read() + file2.read())
        return new_file

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.current)
            line = f.readline()
            if not line:
                self.current = 0
                raise StopIteration
            self.current = f.tell()
            return line

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def write(self, text):
        with open(self.path, 'w') as f:
            return f.write(text)
