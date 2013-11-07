from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk as gtk
from gi.repository import Notify
import sys
import FileChooser
import logging
import subprocess

Notify.init("Hello world")
f = open('ex_list', 'r')
listOfMenu = f.read().splitlines()
f.close()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='indicator.log')

def menuitem_response(w, optionName):
    logging.info("Executing: " + optionName)
    try:
        if optionName.split("/")[-1].split(".")[-1] == "desktop":
            if 0 == subprocess.check_call("deskopen " + optionName, shell=True):
                subprocess.call("deskopen " + optionName, shell=True)
            else:
                notification = Notify.Notification.new("Script Indicator", optionName.split("/")[-1] + " Cannot be run",
                                                       "dialog-information")
                notification.show()
        elif optionName.split("/")[-1].split(".")[-1] == "sh":
            if 0 == subprocess.check_call("sh " + optionName, shell=True):
                subprocess.call("sh " + optionName, shell=True)
            else:
                notification = Notify.Notification.new("Script Indicator", optionName.split("/")[-1] + " Cannot be run",
                                                       "dialog-information")
                notification.show()
        elif optionName.split("/")[-1].split(".")[-1] == "py":
            if 0 == subprocess.check_call("python " + optionName, shell=True):
                subprocess.call("python " + optionName, shell=True)
            else:
                notification = Notify.Notification.new("Script Indicator", optionName.split("/")[-1] + " Cannot be run",
                                                       "dialog-information")
                notification.show()

        else:
            if 0 == subprocess.check_call(optionName, shell=True):
                subprocess.call(optionName, shell=True)
            else:
                notification = Notify.Notification.new("Script Indicator", optionName.split("/")[-1] + " Cannot be run",
                                                       "dialog-information")
                notification.show()
    except subprocess.CalledProcessError:
        notification = Notify.Notification.new("Script Indicator", "Something is wrong. Sorry",
                                               "dialog-information")
        notification.show()

def getFile(w, optionName):
    optionName = str(FileChooser.show())
    logging.info("Adding file" + optionName.split("/")[-1])
    menuitem_add(w, optionName)


def menuitem_add(w, optionName):
    f = open('ex_list', 'w')
    for menulist in listOfMenu:
        if str(menulist).lower() == optionName.lower():
            notification = Notify.Notification.new("Script Indicator", "This scripts already exist",
                                               "dialog-information")
            notification.show()
            f.close()
            return
    listOfMenu.append(optionName)
    for line in listOfMenu:
        f.writelines(line + "\n")
    f.close()
    optionName = listOfMenu[-1]
    menu_items = gtk.MenuItem(optionName)
    menu.append(menu_items)
    menu_items.connect("activate", menuitem_response, optionName)
    menu_items.show()


def quitApplication(w, optionName):
    sys.exit(0)


if __name__ == "__main__":
    ind = appindicator.Indicator.new("example-simple-client",
                                     "indicator-messages",
                                     appindicator.IndicatorCategory.OTHER)
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)
    ind.set_attention_icon("indicator-messages-new")
    ind.set_icon("cab_view")
    # create a menu
    menu = gtk.Menu()
    # create some drop down options
    for optionName in listOfMenu:
        menu_items = gtk.MenuItem(optionName)
        menu.append(menu_items)
        menu_items.connect("activate", menuitem_response, optionName)
        menu_items.show()

    optionName = "Add"
    menu_items = gtk.MenuItem(optionName)
    menu.append(menu_items)
    menu_items.connect("activate", getFile, optionName)
    menu_items.show()

    optionName = "Quit"
    menu_items = gtk.MenuItem(optionName)
    menu.append(menu_items)
    menu_items.connect("activate", quitApplication, optionName)
    menu_items.show()
    ind.set_menu(menu)
    print(listOfMenu)
    gtk.main()
