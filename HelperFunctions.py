from os import system
from StaticStrings import Logging


def Save(file, content):
    f = open(file, "w")
    f.write(content)
    f.close()


def Read(file):
    f = open(file)
    fd = f.read()
    f.close()
    return fd
