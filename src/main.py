import sys
import os
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickWindow

QQuickWindow.setSceneGraphBackend('software')  # should be included as a fallback option for old hardware
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()  # will use Qml instead of QtWidgets as the UI layer for the Qt App
engine.quit.connect(app.quit)  # connects UI layer's "quit" to app's "quit". both are closed, when UI is closed by user
engine.load('./UI/main.qml')  # load qml for th Qml UI
exit_code = app.exec()  # runs the App, return exit_code
sys.exit(exit_code)  # exits Python system
