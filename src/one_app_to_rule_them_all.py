import sys
import random

from src.configuration.config import DEFAULT, DEFAULT_TASK_VALUES, T_MAX, T_MIN, N

from src.configuration.config import WINDOW_SIZE, COLOR_PALETTE, BUTTON_SIZE, LINE_EDIT_SIZE, TASK_LABEL_WIDTH, APP_BG_COLOR, BUTTON_COLOR
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


class Task:
    task_number = 0  # TODO: change to 0 or -1. Keep in mind - tasks will start from task_number+1
    task_name = None

    # Data required for algorith
    release_time: int = None
    execution_time: int = None
    deadline: int = None
    # task state
    not_done: bool = None
    current_execution_time = None
    # Data after the
    start_time: int = None
    stop_time: int = None
    delay: int = None
    executed_time: int = None

    def __init__(self, p, r, d):
        self.execution_time = p
        self.release_time = r
        self.deadline = d

        self.not_done = True
        self.current_execution_time = 0

        Task.task_number += 1
        self.task_name = f"Z:{self.task_number}"

    def __str__(self):
        return self.task_name

    __repr__ = __str__


class LiuWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.general_layout = QGridLayout()
        central_widget = QWidget(self)
        central_widget.setStyleSheet(f"background-color: {APP_BG_COLOR}")
        central_widget.setLayout(self.general_layout)
        self.setCentralWidget(central_widget)

        self._set_user_quarter()
        self._set_input_quarter()
        # self._set_output_quarter()
        # self._set_graph_quarter()

        self._connect_signals_and_slots()

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
        self.button_run_alg = QPushButton("Order tasks")
        self.button_fill_input.setFixedWidth(BUTTON_SIZE)
        self.button_run_alg.setFixedWidth(BUTTON_SIZE)
        self.button_fill_input.setStyleSheet(f"background-color:{BUTTON_COLOR};border-radius:30px;border-width:2px;border-color:black")
        self.button_run_alg.setStyleSheet(f"background-color: {BUTTON_COLOR}")

        # add user input layout to user quarter layout
        self.user_quarter_layout = QVBoxLayout()
        self.user_quarter_layout.addWidget(QLabel("<h1>Algorithm Liu</h1>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(QLabel("<h2>1 | r<sub>i</sub>, prm | L<sub>max</sub></h2>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(user_input_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(self.button_fill_input, alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(self.button_run_alg, alignment=Qt.AlignmentFlag.AlignCenter)

        # add user's layout to user widget
        # add user widget to general layout
        # ####user_widget = QWidget()
        # ####user_widget.setLayout(self.user_quarter_layout)
        # ####self.general_layout.addWidget(user_widget, 0, 0)
        self.general_layout.addLayout(self.user_quarter_layout, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)

    def _set_input_quarter(self):
        # input values layout
        self.input_values_layout = QGridLayout()
        self.input_values_layout.setSpacing(1)
        input_values_widget = QWidget()
        input_values_widget.setLayout(self.input_values_layout)

        # add input values layout to input quarter layout
        self.input_quarter_layout = QVBoxLayout()
        self.input_quarter_layout.addWidget(QLabel("<h2>Input values</h2>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.input_quarter_layout.addWidget(input_values_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # self.user_quarter_layout.addLayout(self.input_values_layout)

        # add input layout to input widget
        # add input widget to general layout
        # #### input_widget = QWidget()
        # #### input_widget.setLayout(self.input_quarter_layout)
        # #### self.general_layout.addWidget(input_widget, 1, 0)
        self.general_layout.addLayout(self.input_quarter_layout, 1, 0)

    def get_user_values(self) -> dict:
        print("[Start] get_user_values")
        user_values = {
            "min_time": self.user_min_time,
            "max_time": self.user_max_time,
            "tasks_number": self.user_tasks_number
        }
        print("[End] get_user_values")
        return user_values

    def create_tasks(self, min_time, max_time, tasks_number):
        print("[Start] create_tasks")
        tasks_list = []
        for el in range(tasks_number):
            execution_time = random.randint(min_time, max_time)
            release_time = random.randint(min_time, max_time)
            deadline = release_time + execution_time + random.randint(min_time, max_time)

            tasks_list.append(Task(p=execution_time, r=release_time, d=deadline))
        print("[End]   create_tasks")
        return tasks_list

    def create_tasks_default(self, values):
        print("[start] Model: create_tasks_default")
        tasks_list = [Task(p=el[0], r=el[1], d=el[2]) for el in values]
        print("[end]   Model: create_tasks_default")

        return tasks_list

    def generate_input(self):
        print("[Start] generate_input")
        user_values = self.get_user_values()
        # tasks_list = self.create_tasks(
        #     min_time=user_values.get("min_time"),
        #     max_time=user_values.get("max_time"),
        #     tasks_number=user_values.get("tasks_number")
        # )
        # Plan B - start - use default values
        tasks_list = self.create_tasks_default(DEFAULT_TASK_VALUES)
        # Plan B - end
        tasks_print_table = []
        for task in tasks_list:
            task_row = [str(task), task.execution_time, task.release_time, task.deadline]
            tasks_print_table.append(task_row)
        self.fill_input_grid(tasks_print_table)
        print("[End]   generate_input")

    def fill_input_grid(self, tasks_list):
        print("[Start] fill_input_grid")
        # tasks_n_label = QLabel("Task n.")
        # p_label = QLabel("p")
        # r_label = QLabel("r")
        # d_label = QLabel("d")
        # tasks_n_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # p_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # r_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # d_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.input_quarter_layout.addWidget(tasks_n_label, 0, 0)
        # self.input_quarter_layout.addWidget(p_label, 0, 1)
        # self.input_quarter_layout.addWidget(r_label, 0, 2)
        # self.input_quarter_layout.addWidget(d_label, 0, 3)

        for row, task in enumerate(tasks_list):
            color = COLOR_PALETTE[row]
            for col, task_parameter in enumerate(task):
                parameter = QLabel(f"<h2>{str(task_parameter)} </h2>")
                parameter.setAlignment(Qt.AlignmentFlag.AlignCenter)
                parameter.setFixedWidth(TASK_LABEL_WIDTH)
                parameter.setStyleSheet(f"background-color: {color}")
                self.input_values_layout.addWidget(parameter, row + 1, col)
            print(f"color: {color}")
        print("[End]   fill_input_grid")
        # super().show()

    def _connect_signals_and_slots(self):
        self.button_fill_input.clicked.connect(self.generate_input)


if __name__ == "__main__":
    app = QApplication([])
    w = LiuWindow()
    w.show()
    sys.exit(app.exec())
