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
from datetime import datetime
import stocksim
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlComponent, QQmlEngine


class Slots(QObject):
    def __init__(self):
        super(Slots, self).__init__()


class StockSimGui(QObject, stocksim.StockSim):
    def __init__(self):
        super(StockSimGui, self).__init__()

    @pyqtSlot()
    def open_history(self):
        # dialog = FileDialog.create()
        # fd = dialog.findChild(QObject, "fileDialog")
        self.fileDialog = FileDialog.create()
        self.fileDialog.setProperty("title", "Open history")
        self.fileDialog.accepted.connect(self.open_history_file)
        self.fileDialog.open()

    @pyqtSlot(result=str)
    def open_history_file(self):
        self.fileDialog.accepted.disconnect(self.open_history_file)
        r = "History opened at " + repr(datetime.utcnow())
        with open(self.fileDialog.property("fileUrl").toLocalFile()) as file:
            data = file.read()
            root.update_history(data)
        return r

    @pyqtSlot(str)
    @pyqtSlot(str, int)
    def load_history(self, data, i=0):
        self.stocks[i].history.load(data)
        # print(repr(self.stocks[i].history))

    @pyqtSlot(str)
    @pyqtSlot(str, int)
    def load_transactions(self, data, i=0):
        self.stocks[i].transactions.load(data)

    @pyqtSlot()
    @pyqtSlot(int)
    def calc_stock_shares(self, i=0):
        print("calc_shares")
        self.stocks[i].calc_shares()

    @pyqtSlot()
    @pyqtSlot(int)
    def calc_stock_value(self, i=0):
        print("calc_value")
        self.stocks[i].calc_value()

    history_opened = pyqtSignal()

    @pyqtSlot()
    def test(self):
        print("TEST")


# class FileDialog(QObject):
#     def __new__(cls, engine: QQmlEngine):
#         print(1)
#         component = QQmlComponent(engine, "fileDialog.qml")
#         print(2)
#
#         return super(FileDialog, cls).__new__(cls)  # component.create()
#
#     def __init__(self, engine: QQmlEngine):
#         print(3)
#         super(FileDialog, self).__init__()
#         o = QQmlComponent(engine, "fileDialog.qml").create()
#         print(4)
#         self.__dict__ = o.__dict__.copy()
#         print("Success!")


class MainWindow(QQuickView):
    def __init__(self, slots):
        super(MainWindow, self).__init__()
        context = self.rootContext()
        for (name, slot) in slots:
            context.setContextProperty(name, slot)

        print(repr(self.rootContext().contextProperty("stocksim").test))
        self.setTitle("StockSim")
        self.setSource(QUrl("uiTest.qml"))
        self.setResizeMode(QQuickView.SizeRootObjectToView)


ss = StockSimGui()

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    slots = Slots()
    window = MainWindow([("testslots", slots), ("stocksim", ss)])
    root = window.rootObject()
    FileDialog = QQmlComponent(window.engine(), "fileDialog.qml")
    window.show()
    sys.exit(app.exec())
