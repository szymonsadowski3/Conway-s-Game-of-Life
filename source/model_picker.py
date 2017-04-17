import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import helpers

class DialogCustomEmptyGrid(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Configure your Game Of Life", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        vbox = self.get_content_area()
        self.add(vbox)

        self.entry_width = Gtk.Entry()
        self.entry_width.set_text("20")

        self.entry_height = Gtk.Entry()
        self.entry_height.set_text("20")

        self.entry_cell_size = Gtk.Entry()
        self.entry_cell_size.set_text("24")

        label_width = Gtk.Label("Grid Width")
        label_height = Gtk.Label("Grid Height")
        label_cell_size = Gtk.Label("Cell size")

        vbox.pack_start(label_width, True, True, 0)
        vbox.pack_start(self.entry_width, True, True, 0)
        vbox.pack_start(label_height, True, True, 0)
        vbox.pack_start(self.entry_height, True, True, 0)
        vbox.pack_start(label_cell_size, True, True, 0)
        vbox.pack_start(self.entry_cell_size, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        self.model = []

        self.show_all()

    def getEntriesContent(self):
        return self.entry_height.get_text(), self.entry_width.get_text(), self.entry_cell_size.get_text()


# THIS IS BLOCKING WINDOW
class ModelPicker(Gtk.Window):
    def parseEntriesToInts(self, entries):
        try:
            return int(entries[0]), int(entries[1]), int(entries[2])
        except ValueError:
            print('Input parsing error, returning default values')
            return 20, 20, 24

    def getOptimalCellSizeForModel(self, consistent_model):
        resolution = helpers.detectResolution().split('x')
        window_width = int(resolution[0]) // 3
        return window_width // len(consistent_model[0])

    def __init__(self):
        Gtk.Window.__init__(self, title="MODEL PICKER")
        self.set_border_width(6)

        vbox = Gtk.Box(spacing=6)
        self.add(vbox)

        custom_grid_button = Gtk.Button("Create empty custom grid")
        custom_grid_button.connect("clicked", self.onCustomGridButtonClicked)

        ok_button = Gtk.Button("OK")
        ok_button.connect("clicked", self.onOkButtonClicked)
        vbox.pack_start(ok_button, True, True, 0)

        import_model_from_file_button = Gtk.Button("Import grid from file")
        import_model_from_file_button.connect("clicked", self.onImportModelFromFileButtonClicked)

        vbox.pack_start(custom_grid_button, True, True, 0)
        vbox.pack_start(import_model_from_file_button, True, True, 0)

        self.initial_model_and_size = None

    def onOkButtonClicked(self, button):
        Gtk.main_quit()

    def run(self):
        self.show_all()
        Gtk.main()
        self.destroy()
        return self.initial_model_and_size

    def onCustomGridButtonClicked(self, widget):
        dialog = DialogCustomEmptyGrid(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
            dialog_entries_contents = (
                dialog.entry_width.get_text(), dialog.entry_height.get_text(), dialog.entry_cell_size.get_text())
            parsed_entries = self.parseEntriesToInts(dialog_entries_contents)
            self.initial_model_and_size = (
                helpers.getModelBlank(width=parsed_entries[0], height=parsed_entries[1]), parsed_entries[2])

        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()

    def onImportModelFromFileButtonClicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.addFilters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selected_file = dialog.get_filename()
            print("Open clicked")
            print("File selected: " + selected_file)
            initial_model= helpers.fileTo2dListOfInts(selected_file)
            helpers.makeListOfIntsConsistentModel(initial_model)
            self.initial_model_and_size = (initial_model, self.getOptimalCellSizeForModel(initial_model))
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def addFilters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def getInitialModel(self):
        return self.initial_model_and_size

    def show(self):
        win = ModelPicker()
        win.connect("delete-event", Gtk.main_quit)
        win.show_all()
