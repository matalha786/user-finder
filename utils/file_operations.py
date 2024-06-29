import os

def isFile(filename):
    return os.path.isfile(filename)

def getLinesFromFile(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]
