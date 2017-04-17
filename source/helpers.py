import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import subprocess

def fileTo2dListOfInts(path):
    list2d = []
    with open(path, 'r') as f:
        for line in f:
            list2d.append([int(a) for a in line.strip()])
    return list2d

def makeListOfIntsConsistentModel(list):
    for i in range(len(list)):
        for j in range(len(list[0])):
            if list[i][j]!=0 and list[i][j]!=1:
                list[i][j]=0

def getModelBlank(width, height):
    return [[0] * width for _ in range(height)]

def detectResolution():
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4', shell=True, stdout=subprocess.PIPE).communicate()[0]
    return output.decode('utf-8')


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