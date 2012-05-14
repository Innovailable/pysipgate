import sys
import os.path
import ConfigParser

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, SLOT

from sipgate import SipgateConnection

CONFIG_FILE = "~/.pysipgate"

class Tray(QtGui.QSystemTrayIcon):

    def __init__(self, con, parent=None):
        self.con = con
        self.parent = parent

        icon = QtGui.QIcon("img/phone_icon.png")

        QtGui.QSystemTrayIcon.__init__(self, icon, parent)

        self.menu = menu = QtGui.QMenu()

        callAction = menu.addAction("Call")

        menu.addSeparator()

        exitAction = menu.addAction("Exit")
        self.connect(exitAction, SIGNAL('triggered()'), QtGui.QApplication.quit)

        self.setContextMenu(menu)

def main():
    app = QtGui.QApplication(sys.argv)

    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser(CONFIG_FILE))

    user = config.get('account', 'user')
    password = config.get('account', 'password')

    con = SipgateConnection(user, password)

    tray = Tray(con)
    tray.show()

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
