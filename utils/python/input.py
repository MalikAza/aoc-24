import os

def get_file(file: str):
    path = os.path.join(os.path.dirname(file), "../input.txt")
    
    return open(path, "r")