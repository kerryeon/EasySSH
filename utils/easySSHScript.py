from _pickle import load as __load__
from _pickle import dump as __dump__
from os import remove as __remove__


def __download__(path: str):
    try:
        data = None
        with open(path, 'rb') as f:
            data = __load__(f)
    finally:
        __remove__(path)
        return data


def __upload__(obj, path: str):
    with open(path, 'wb') as f:
        __dump__(obj, f)
