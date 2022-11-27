import sys

from src.configuration.config import WINDOW_SIZE
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QFormLayout,
)


class LuiWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.general_layout = QGridLayout()
        central_widget = QWidget(self)

        central_widget.setLayout(self.general_layout)
        self.setCentralWidget(central_widget)

        self._set_user_quarter()
        self._set_input_quarter()
        self._set_output_quarter()
        self._set_graph_quarter()

    def _set_user_quarter(self):
        self.user_quarter_layout = QVBoxLayout()
        self.user_quarter_layout.addWidget(QLabel("<h1>Algorithm Liu</h1>"))
        self.user_quarter_layout.addWidget(QLabel("<h1>TODO: add Graham's notation</h1>"))

        # user input
        self.user_min_time = QLineEdit()
        self.user_max_time = QLineEdit()
        self.user_tasks_number = QLineEdit()

        # layout for user's input
        user_input_layout = QFormLayout()
        user_input_layout.addRow("Minimum time:", self.user_min_time)
        user_input_layout.addRow("Maximum time:", self.user_max_time)
        user_input_layout.addRow("Tasks number:", self.user_tasks_number)
        self.user_quarter_layout.addLayout(user_input_layout)

        # add user's layout to base layout
        self.general_layout.addLayout(self.user_quarter_layout, row=0, column=0)

    def _set_input_quarter(self):
        self.input_quarter_layout = QVBoxLayout()
        self.input_quarter_layout.addWidget(QLabel("<h2>Input values</h2>"))

        # input values layout
        self.input_values_layout = QGridLayout()

        self.general_layout.addLayout(self.input_values_layout, row=1, column=0)

    def _set_output_quarter(self):
        pass

    def _set_graph_quarter(self):
        pass

    def return_user_values(self) -> dict:
        user_values = {
            "min_time": self.user_min_time,
            "max_time": self.user_max_time,
            "tasks_number": self.user_tasks_number
        }
        return user_values

    def fill_input_data(self, tasks_list):
        for task in tasks_list:




def main():
    """PyCalc's main function."""
    lui_app = QApplication([])
    lui_window = LuiWindow()
    lui_window.show()
    sys.exit(lui_app.exec())


if __name__ == "__main__":
    main()
