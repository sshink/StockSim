#!/usr/bin/env python

# Copyright (C) 2017 Simon Shink

# This file is part of StockSim.
#
# StockSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# StockSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with StockSim.  If not, see <http://www.gnu.org/licenses/>.

import sys

import stocksim
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import QQuickView


class MainWindow(QQuickView):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setTitle("StockSim")
        self.setSource(QUrl("uiTest.qml"))
        self.setResizeMode(QQuickView.SizeRootObjectToView)
        s = stocksim.Stock()


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
