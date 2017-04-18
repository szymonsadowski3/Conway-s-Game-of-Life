import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import subprocess
import os
import sys
import configparser


class ConfigLoader(object):
    DEFAULT_PATH = 'config.ini'
    config_loader = None

    @classmethod
    def getDefaultValueFor(cls, key):
        backupValues = {'DEFAULT_BG_COLOR': 'steel blue', 'DEFAULT_BG_COLOR2': 'cornflower blue',
                        'DEFAULT_FOREGROUND_COLOR': 'black', 'WINDOW_SIZE_DIVIDEND_WHILE_IMPORT_FROM_FILE': 3}
        if not cls.config_loader:
            cls.config_loader = configparser.ConfigParser()
            cls.config_loader.read(cls.DEFAULT_PATH)

        if not ('CONFIG' in cls.config_loader) or not (key in cls.config_loader['CONFIG']):
            return backupValues[key]

        if key=='WINDOW_SIZE_DIVIDEND_WHILE_IMPORT_FROM_FILE':
            try:
                dividend = int(cls.config_loader['CONFIG'][key])
                return dividend
            except ValueError:
                return backupValues[key]

        return cls.config_loader['CONFIG'][key]


def restartProgram(widget):
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, *sys.argv)


def fileTo2dListOfInts(path):
    list2d = []
    with open(path, 'r') as f:
        for line in f:
            list2d.append([int(a) for a in line.strip()])
    return list2d


def makeListOfIntsConsistentModel(list):
    for i in range(len(list)):
        for j in range(len(list[0])):
            if list[i][j] != 0 and list[i][j] != 1:
                list[i][j] = 0


def getModelBlank(width, height):
    return [[0] * width for _ in range(height)]


def detectResolution():
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4', shell=True, stdout=subprocess.PIPE).communicate()[0]
    return output.decode('utf-8')


def saveModelToFile(path, model):
    with open(path, 'w+') as f:
        for line in model:
            f.write(''.join(str(x) for x in line))
            f.write('\n')


class GtkHelper(object):
    @staticmethod
    def generateColor(str):
        color = Gdk.color_parse(str)
        return Gdk.RGBA.from_color(color)

    @staticmethod
    def generateCell(color, size):
        rgba = GtkHelper.generateColor(color)
        area = Gtk.DrawingArea()
        area.set_size_request(size, size)
        area.override_background_color(0, rgba)
        return area

    @staticmethod
    def overrideCellColor(cell, str_color):
        rgba = GtkHelper.generateColor(str_color)
        cell.override_background_color(0, rgba)
