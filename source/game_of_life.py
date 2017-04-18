import simulator
import model_picker
import gi
import helpers
from helpers import GtkHelper

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

DEFAULT_BG_COLOR = 'steel blue'
DEFAULT_BG_COLOR2 = 'cornflower blue'
DEFAULT_FOREGROUND_COLOR = 'black'

class GameOfLifeGrid(Gtk.Window):

    #HELPERS
    def determineWhichCellWasClicked(self, x, y):
        return (int(y//self.cell_size), int(x//self.cell_size))

    def getModelSize(self):  #(rows, cols)
        return (len(self.model), len(self.model[0]))

    #VIEW RELATED METHODS
    def colorSwatch(self, str_color):
        return GtkHelper.generateCell(str_color, self.cell_size)

    def generateGridOfCells(self, grid, init_color=DEFAULT_BG_COLOR):
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                cell = self.colorSwatch(init_color)
                grid.attach(cell, i, j, 1, 1)

    def changeCellColor(self, row, column, color):
        cell = self.grid.get_child_at(column, row)
        GtkHelper.overrideCellColor(cell, color)

    def changeCellColorToBG(self, row, column):
        is_cell_odd = (row+column)%2==0
        cell = self.grid.get_child_at(column, row)
        if is_cell_odd:
            GtkHelper.overrideCellColor(cell, DEFAULT_BG_COLOR)
        else:
            GtkHelper.overrideCellColor(cell, DEFAULT_BG_COLOR2)

    def changeCellColorToForeground(self, row, column):
        cell = self.grid.get_child_at(column, row)
        GtkHelper.overrideCellColor(cell, DEFAULT_FOREGROUND_COLOR)

    def updateVisualization(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.model[i][j]!=self.model_buffer and self.model[i][j]:
                    self.changeCellColor(i,j, DEFAULT_FOREGROUND_COLOR)
                elif self.model[i][j]!=self.model_buffer and not self.model[i][j]:
                    self.changeCellColorToBG(i, j)

    def nextStep(self, widget):
        self.game_of_life_simulator.simulate(self.model)
        self.updateVisualization()
        self.model_buffer = self.model
        win.show_all()

    def toggleCellState(self, row, col):
        new_state = 1 - self.model[row][col]
        self.model[row][col] = new_state
        if new_state:
            self.changeCellColorToForeground(row, col)
        else:
            self.changeCellColorToBG(row, col)

    #EVENTS
    def eventPress(self, eventbox, event):
        print("Button Press Event: %d %d" % (event.x, event.y))
        row, col = self.determineWhichCellWasClicked(event.x, event.y)
        row_bound, col_bound = self.getModelSize()
        if row>=row_bound or col>=col_bound:
            return
        self.toggleCellState(row, col)

    def saveModel(self, widget):
        dialog = Gtk.FileChooserDialog("Save", self, Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            save_path = dialog.get_filename()
            print("Save selected: " + save_path)
            helpers.saveModelToFile(save_path, self.model)

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

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
        next_step_button = Gtk.Button()
        next_step_button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        next_step_button.connect("clicked", self.nextStep)
        hb.add(next_step_button)

        save_button = Gtk.Button("Save")
        save_button.connect("clicked", self.saveModel)
        hb.add(save_button)
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
        self.model_buffer = self.model
        self.updateVisualization()
        self.show_all()

win = GameOfLifeGrid()
win.connect("delete-event", Gtk.main_quit)
Gtk.main()