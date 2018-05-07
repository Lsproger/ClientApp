
import os


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


file_path = "/folder/filename2.txt"
directory = os.getcwd() + file_path
ensure_dir(directory)
f = open(directory, 'w')

f.write('hello, mtfckr')
f.close()
