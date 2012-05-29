#!/usr/bin/env python3

import sys
import re
import os
import configparser

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, SLOT, Qt

CONFIG_FILE = '~/.clipcatch'
DEFAULT_FILTER = '$\w+://'

class Catcher(QtGui.QWidget):

    def __init__(self, default, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.resize(500, 500)

        layout = QtGui.QVBoxLayout(self)

        if default == None:
            default = ''

        self.regex = regex = QtGui.QLineEdit(default, self)
        layout.addWidget(regex)

        self.dump = dump = QtGui.QTextEdit(self)
        layout.addWidget(dump)

        dump.setFocus(Qt.ActiveWindowFocusReason)

        self.board = board = QtGui.QApplication.clipboard()
        board.dataChanged.connect(self.update)

        self.update()

    def update(self):
        pattern = str(self.regex.text())
        data = str(self.board.text())

        if re.search(pattern, data):
            dump = self.dump
            dump.moveCursor(QtGui.QTextCursor.End)
            self.dump.insertPlainText(data + '\n')

def main():
    app = QtGui.QApplication(sys.argv)

    config = configparser.ConfigParser()
    config.read(os.path.expanduser(CONFIG_FILE))

    default = config.get('default', 'filter', fallback=DEFAULT_FILTER)

    catcher = Catcher(default)
    catcher.show()

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())

