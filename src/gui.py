import sys

from src.configuration.config import WINDOW_SIZE, COLOR_PALETTE, BUTTON_SIZE, LINE_EDIT_SIZE
from PyQt6.QtCore import Qt
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


class LiuWindow(QMainWindow):
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
        # user input
        self.user_min_time = QLineEdit()
        self.user_max_time = QLineEdit()
        self.user_tasks_number = QLineEdit()
        self.user_min_time.setFixedWidth(LINE_EDIT_SIZE)
        self.user_max_time.setFixedWidth(LINE_EDIT_SIZE)
        self.user_tasks_number.setFixedWidth(LINE_EDIT_SIZE)

        # layout for user's input
        user_input_layout = QFormLayout()
        user_input_layout.addRow("Minimum time:", self.user_min_time)
        user_input_layout.addRow("Maximum time:", self.user_max_time)
        user_input_layout.addRow("Tasks number:", self.user_tasks_number)
        user_input_widget = QWidget()
        user_input_widget.setLayout(user_input_layout)

        # buttons
        self.button_fill_input = QPushButton("Fill input values table")
        self.button_fill_input.setFixedWidth(BUTTON_SIZE)

        # add user input layout to user quarter layout
        self.user_quarter_layout = QVBoxLayout()
        self.user_quarter_layout.addWidget(QLabel("<h1>Algorithm Liu</h1>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(QLabel("<h3>TODO: add Graham's notation</h1>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(user_input_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(self.button_fill_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # add user's layout to user widget
        # add user widget to general layout
        # ####user_widget = QWidget()
        # ####user_widget.setLayout(self.user_quarter_layout)
        # ####self.general_layout.addWidget(user_widget, 0, 0)
        self.general_layout.addLayout(self.user_quarter_layout, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)

    def _set_input_quarter(self):
        # input values layout
        input_values_widget = QWidget()
        self.input_values_layout = QGridLayout()
        input_values_widget.setLayout(self.input_values_layout)

        # add input values layout to input quarter layout
        self.input_quarter_layout = QVBoxLayout()
        self.input_quarter_layout.addWidget(QLabel("<h2>Input values</h2>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.input_quarter_layout.addWidget(input_values_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        # TODO: delete below lines
        self.foo_button = QPushButton("foo")

        # self.user_quarter_layout.addLayout(self.input_values_layout)

        # add input layout to input widget
        # add input widget to general layout
        # #### input_widget = QWidget()
        # #### input_widget.setLayout(self.input_quarter_layout)
        # #### self.general_layout.addWidget(input_widget, 1, 0)
        self.general_layout.addLayout(self.input_quarter_layout, 1, 0)
        self.general_layout.addWidget(self.foo_button, 3, 0)

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

    def fill_input_quarter(self, tasks_list):
        for row, task in enumerate(tasks_list):
            color = COLOR_PALETTE[row]
            for col, task_parameter in enumerate(task):
                parameter = QLabel(str(task_parameter))
                parameter.setStyleSheet(f"background-color: {color}")
                self.input_values_layout.addWidget(parameter, row, col)
            print(f"color: {color}")
        super().show()


def main():
    """PyCalc's main function."""
    lui_app = QApplication([])
    lui_window = LiuWindow()
    lui_window.show()
    sys.exit(lui_app.exec())


if __name__ == "__main__":
    main()
