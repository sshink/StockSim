import sys

import stocksim
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import QQuickView

app = QGuiApplication(sys.argv)
view = QQuickView()
view.setSource(QUrl("uiTest.qml"))
view.setResizeMode(QQuickView.SizeRootObjectToView)
s = stocksim.Stock()
view.show()
sys.exit(app.exec())
