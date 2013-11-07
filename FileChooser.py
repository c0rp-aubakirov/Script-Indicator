from gi.repository import Gtk


class FileChooserWindow(Gtk.Window):
    filePath = ""
    fileName = ""

    def on_file_clicked(self):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            self.fileName = dialog.get_filename()
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            print("Cancel clicked")

    def add_filters(self, dialog):
        filter_desktop = Gtk.FileFilter()
        filter_desktop.set_name("Any files")
        filter_desktop.add_pattern("*.desktop")
        dialog.add_filter(filter_desktop)

        filter_text = Gtk.FileFilter()
        filter_text.set_name("bash scripts")
        filter_text.add_pattern("*.sh")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def __init__(self):
        self.on_file_clicked()

def show():
  win = FileChooserWindow()
  return win.fileName
