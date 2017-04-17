import simulator
import model_picker
import gi
from helpers import GtkHelper

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GameOfLifeGrid(Gtk.Window):
    color_mapping = {0: 'white', 1:'black'}

    #HELPERS
    def determineWhichCellWasClicked(self, x, y):
        return (int(y//self.cell_size), int(x//self.cell_size))

    def getModelSize(self):  #(rows, cols)
        return (len(self.model), len(self.model[0]))

    #VIEW RELATED METHODS
    def colorSwatch(self, str_color):
        return GtkHelper.generateCell(str_color, self.cell_size)

    def generateGridOfCells(self, grid, init_color='white'):
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                cell = self.colorSwatch(init_color)
                grid.attach(cell, i, j, 1, 1)

    def changeCellColor(self, row, column, color):
        cell = self.grid.get_child_at(column, row)
        GtkHelper.overrideCellColor(cell, color)

    def updateVisualization(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.model[i][j]:
                    self.changeCellColor(i,j,'black')
                elif not self.model[i][j]:
                    self.changeCellColor(i, j, 'white')

    def nextStep(self, widget):
        self.game_of_life_simulator.simulate(self.model)
        self.updateVisualization()
        win.show_all()

    def toggleCellState(self, row, col):
        new_state = 1 - self.model[row][col]
        self.model[row][col] = new_state
        self.changeCellColor(row, col, GameOfLifeGrid.color_mapping[new_state])

    #EVENTS
    def eventPress(self, eventbox, event):
        print("Button Press Event: %d %d" % (event.x, event.y))
        row, col = self.determineWhichCellWasClicked(event.x, event.y)
        row_bound, col_bound = self.getModelSize()
        if row>=row_bound or col>=col_bound:
            return
        self.toggleCellState(row, col)

    def __init__(self):
        #DEFAULT PROPERTIES
        self.grid_width = 20
        self.grid_height = 20
        self.cell_size = 24
        #WINDOW INIT
        Gtk.Window.__init__(self, title="Grid Example")
        self.grid = Gtk.Grid()
        eventbox = Gtk.EventBox()
        self.add(eventbox)
        eventbox.connect("button-press-event", self.eventPress)
        eventbox.add(self.grid)
        self.set_border_width(10)
        #HEADER
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "GAME OF LIFE"
        self.set_titlebar(hb)
        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        button.connect("clicked", self.nextStep)
        hb.add(button)
        #CONFIG DIALOG
        configurer = model_picker.ModelPicker()
        initial_model = configurer.run()
        self.model = initial_model[0]
        self.cell_size = initial_model[1]
        self.grid_height = len(self.model)
        self.grid_width = len(self.model[0])
        configurer.destroy()
        # IMPORT SIMULATOR
        self.game_of_life_simulator = simulator.GameOfLifeSimulator()
        #VISUALIZATION
        self.generateGridOfCells(self.grid)
        self.updateVisualization()
        self.show_all()

win = GameOfLifeGrid()
win.connect("delete-event", Gtk.main_quit)
Gtk.main()