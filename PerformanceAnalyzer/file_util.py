import os
import re
from xml.etree import ElementTree as ET


def get_files(path, ext='', recursive=False):
    path_list = [path]
    files = list()

    while len(path_list) > 0:
        cpath = path_list.pop()
        with os.scandir(cpath) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    if entry.name.endswith(ext):
                        files.append(entry.path)
                    else:
                        if recursive:
                            path_list.append(entry.path)
    return files


def parse_xml_log(path):
    tree = ET.parse(path)
    root = tree.getroot()
    it = root.iter()
    size = 0
    for item in it:
        size = size+1
    return size


def parse_top_log(path):
    with open(path, 'r') as f:
        data = f.read()
        try:
            top = max(map(int, re.findall('(\d+)%', data)))
        except ValueError:
            top = 0
        return top
