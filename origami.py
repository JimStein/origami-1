#! /usr/bin/env python

from PySide import QtGui
import sys

import window

app = QtGui.QApplication(sys.argv)

window = window.Window()
window.show()

ret = app.exec_()

sys.exit(ret)
