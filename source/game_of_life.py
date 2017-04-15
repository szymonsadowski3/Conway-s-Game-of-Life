import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio
import game_of_life_model

def fileTo2dListOfInts(path):
    list2d = []
    with open(path, 'r') as f:
        for line in f:
            list2d.append([int(a) for a in line.strip()])
    return list2d

GRID_WIDTH = 20
GRID_HEIGHT = GRID_WIDTH
SIZE_CELL = 24

class GameOfLifeGrid(Gtk.Window):
    color_mapping = {0: 'white', 1:'black'}

    def colorSwatch(self, str_color):
        color = Gdk.color_parse(str_color)
        rgba = Gdk.RGBA.from_color(color)

        area = Gtk.DrawingArea()
        area.set_size_request(SIZE_CELL, SIZE_CELL)
        area.override_background_color(0, rgba)

        return area

    def overrideCellColor(self, cell, str_color):
        color = Gdk.color_parse(str_color)
        rgba = Gdk.RGBA.from_color(color)
        cell.override_background_color(0, rgba)

    def generateGridOfCells(self, grid, init_color='white'):
        cells = []
        for x in range(GRID_WIDTH*GRID_HEIGHT):
            cell = self.colorSwatch(init_color)
            cells.append(cell)

        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                grid.attach(cells[GRID_WIDTH * i + j], i, j, 1, 1)

        return cells

    def changeCellColor(self, row, column, color):
        cell = self.grid.get_child_at(column, row)
        self.overrideCellColor(cell, color)

    def visualizeModel(self):
        for i in range(GRID_HEIGHT,):
            for j in range(GRID_WIDTH):
                if self.model[i][j]:#!=self.current_grid_state and self.model[i][j]:
                    self.changeCellColor(i,j,'black')
                elif not self.model[i][j]:#!=self.current_grid_state and not self.model[i][j]:
                    self.changeCellColor(i, j, 'white')

    def nextStep(self, widget):
        # self.changeCellColor(0,0, 'black')
        self.game_of_life_simulator.simulate(self.model)
        self.visualizeModel()
        win.show_all()

    def determineCell(self, x, y):
        return (int(y//SIZE_CELL), int(x//SIZE_CELL))

    def eventPress(self, eventbox, event):
        # (row, column) = self.determineGrid(event.x, event.y)
        print("Button Press Event: %d %d" % (event.x, event.y))
        row, col = self.determineCell(event.x, event.y)
        new_state = 1 - self.model[row][col]
        self.model[row][col] = new_state
        self.changeCellColor(row, col, GameOfLifeGrid.color_mapping[new_state])

    def __init__(self):
        #IMPORT MODEL
        self.game_of_life_simulator = game_of_life_model.GameOfLifeSimulator()
        self.model = fileTo2dListOfInts('example2.txt')
        #END

        #WINDOW INIT
        Gtk.Window.__init__(self, title="Grid Example")
        self.grid = Gtk.Grid()

        eventbox = Gtk.EventBox()
        self.add(eventbox)
        eventbox.connect("button-press-event", self.eventPress)


        eventbox.add(self.grid)
        self.set_border_width(10)
        #END

        #HEADER
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "GAME OF LIFE"
        self.set_titlebar(hb)
        # button = Gtk.Button()
        # button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        # hb.add(button)

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        button.connect("clicked", self.nextStep)
        hb.add(button)
        #END

        self.generateGridOfCells(self.grid)
        self.visualizeModel()
        # cell = self.grid.get_child_at(0,0)
        # self.overrideCellColor(cell, 'brown')
        # cell = self.color_swatch_new('brown')
        # grid.attach(self.color_swatch2('brown'), 0, 0, 1, 1)
        # grid.attach(self.color_swatch2('brown'), 0, 1, 1, 1)


win = GameOfLifeGrid()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

# def color_swatch_new(self, str_color):
    #     color = Gdk.color_parse(str_color)
    #     rgba = Gdk.RGBA.from_color(color)
    #     button = Gtk.Button()
    #
    #     area = Gtk.DrawingArea()
    #     area.set_size_request(24, 24)
    #     area.override_background_color(0, rgba)
    #
    #     button.add(area)
    #
    #     return button

# def generate_grid_of_cells(self, grid):
    #     cells = []
    #     for x in range(GRID_WIDTH*GRID_HEIGHT):
    #         cell = self.color_swatch_new('white')
    #         cells.append(cell)
    #
    #     for i in range(GRID_WIDTH):
    #         for j in range(GRID_HEIGHT):
    #             grid.attach(cells[GRID_WIDTH * i + j], i, j, 1, 1)
    #
    #     return cells