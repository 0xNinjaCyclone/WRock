
from os.path import dirname, abspath

def rockPATH():
    return dirname(dirname(abspath(__file__)))

def rockVERSION():
    with open('VERSION', 'r') as f:
        return f.read()