import sys
from PyQt6.QtWidgets import QApplication

from src.model import LiuModel
from src.gui import LiuWindow
from src.controller import LiuController


if __name__ == "__main__":
    app = QApplication([])
    view = LiuWindow()
    model = LiuModel()
    c = LiuController(view, model)
    view.show()
    sys.exit(app.exec())
