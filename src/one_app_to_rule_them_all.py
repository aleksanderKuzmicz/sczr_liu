import sys
import random
from functools import partial

from src.configuration.config import DEFAULT_TASK_VALUES
from src.configuration.config import WINDOW_HEIGHT, WINDOW_WIDTH, SCROLL_HEIGHT, SCROLL_WIDTH, COLOR_PALETTE, EMPTY_COLOR, BUTTON_SIZE, LINE_EDIT_SIZE, TASK_LABEL_WIDTH, APP_BG_COLOR, BUTTON_COLOR
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QGridLayout,
    QFormLayout,
    QFrame
)


class Task:
    task_number = 0
    task_name = None
    task_color = None

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

        self.task_color = COLOR_PALETTE[Task.task_number]
        Task.task_number += 1
        self.task_name = f"Z{Task.task_number}"

    def __str__(self):
        return self.task_name

    __repr__ = __str__


class LiuWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""
    tasks_list = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.general_layout = QGridLayout()
        central_widget = QWidget(self)
        central_widget.setStyleSheet(f"background-color: {APP_BG_COLOR}")
        central_widget.setLayout(self.general_layout)
        self.setCentralWidget(central_widget)

        self._set_user_quarter()
        self._set_input_quarter()
        self._set_output_quarter()
        self._set_graph_quarter()

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
        user_input_layout.addRow("<p style=\"font-size:15px\">Minimum time:</p>", self.user_min_time)
        user_input_layout.addRow("<p style=\"font-size:15px\">Maximum time:</p>", self.user_max_time)
        user_input_layout.addRow("<p style=\"font-size:15px\">Tasks number:</p>", self.user_tasks_number)
        user_input_widget = QWidget()
        user_input_widget.setLayout(user_input_layout)

        # buttons
        self.button_user = QPushButton("Create tasks")
        self.button_default = QPushButton("Create default tasks")
        self.button_run_alg = QPushButton("Order tasks")

        self.button_user.setFixedWidth(BUTTON_SIZE)
        self.button_default.setFixedWidth(BUTTON_SIZE)
        self.button_run_alg.setFixedWidth(BUTTON_SIZE)
        self.button_user.setStyleSheet(f"background-color:{BUTTON_COLOR};border-radius:30px;border-width:2px;border-color:black")
        self.button_default.setStyleSheet(f"background-color: {BUTTON_COLOR}")
        self.button_run_alg.setStyleSheet(f"background-color: {BUTTON_COLOR}")

        # add user input layout to user quarter layout
        self.user_quarter_layout = QVBoxLayout()
        self.user_quarter_layout.addWidget(QLabel("<h1>Algorithm Liu</h1>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(QLabel("<h2>1 | r<sub>i</sub>, prm | L<sub>max</sub></h2>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(user_input_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(self.button_user, alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(self.button_default, alignment=Qt.AlignmentFlag.AlignCenter)
        self.user_quarter_layout.addWidget(self.button_run_alg, alignment=Qt.AlignmentFlag.AlignCenter)

        # add user's layout to user widget
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

        # add input layout to input widget
        self.general_layout.addLayout(self.input_quarter_layout, 1, 0)

    def _set_output_quarter(self):
        # input values layout
        self.output_values_layout = QGridLayout()
        self.output_values_layout.setSpacing(1)
        output_values_widget = QWidget()
        output_values_widget.setLayout(self.output_values_layout)

        # add output values layout to output quarter layout
        self.output_quarter_layout = QVBoxLayout()
        self.output_quarter_layout.addWidget(QLabel("<h2>Output values</h2>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.output_quarter_layout.addWidget(output_values_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.general_layout.addLayout(self.output_quarter_layout, 0, 1)

    def _set_graph_quarter(self):
        self.graph_values_layout = QGridLayout()
        self.graph_values_layout.setSpacing(1)
        graph_values_widget = QWidget()
        graph_values_widget.setLayout(self.graph_values_layout)
        # scroll
        graph_scroll = QScrollArea()
        graph_scroll.setWidgetResizable(True)
        graph_scroll.setFixedSize(SCROLL_WIDTH, SCROLL_HEIGHT)
        graph_scroll.setFrameShape(QFrame.Shape.NoFrame)
        graph_scroll.setWidget(graph_values_widget)

        self.graph_quarter_layout = QVBoxLayout()
        self.graph_quarter_layout.addWidget(QLabel("<h2>Graph</h2>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.graph_quarter_layout.addWidget(graph_scroll, alignment=Qt.AlignmentFlag.AlignCenter)

        self.general_layout.addLayout(self.graph_quarter_layout, 1, 1)

    def get_user_values(self) -> dict:
        print("[Start] get_user_values")
        user_values = {
            "min_time": int(self.user_min_time.text()),
            "max_time": int(self.user_max_time.text()),
            "tasks_number": int(self.user_tasks_number.text())
        }
        print(f"[End] get_user_values, returning: {user_values}")
        return user_values

    def create_tasks(self, **kwargs):
        min_time = kwargs["min_time"]
        max_time = kwargs["max_time"]
        tasks_number = kwargs["tasks_number"]
        print("[Start] create_tasks")
        tasks_list = []
        for el in range(tasks_number):
            execution_time = random.randint(min_time, int(max_time/3))
            release_time = random.randint(min_time, max_time)
            deadline = release_time + execution_time + int(3 / 2 * random.randint(min_time, int(max_time/3)))

            tasks_list.append(Task(p=execution_time, r=release_time, d=deadline))
        print("[End]   create_tasks")
        return tasks_list

    def create_tasks_default(self, **kwargs):
        values = kwargs["values"]
        print("[start] Model: create_tasks_default")
        tasks_list = [Task(p=el[0], r=el[1], d=el[2]) for el in values]
        print("[end]   Model: create_tasks_default")

        return tasks_list

    def fill_input_grid(self, tasks_list):
        print("[Start] fill_input_grid")
        tasks_n_label = QLabel("<h2>Task</h2>")
        p_label = QLabel("<h2>p</h2>")
        r_label = QLabel("<h2>r</h2>")
        d_label = QLabel("<h2>d</h2>")
        tasks_n_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        p_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        d_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_values_layout.addWidget(tasks_n_label, 0, 0)
        self.input_values_layout.addWidget(p_label, 0, 1)
        self.input_values_layout.addWidget(r_label, 0, 2)
        self.input_values_layout.addWidget(d_label, 0, 3)

        for row, task in enumerate(tasks_list):
            color = task[0].task_color
            for col, task_parameter in enumerate(task):
                parameter = QLabel(f"<h2>{str(task_parameter)}</h2>")
                parameter.setAlignment(Qt.AlignmentFlag.AlignCenter)
                parameter.setFixedWidth(TASK_LABEL_WIDTH)
                parameter.setStyleSheet(f"background-color: {color}")
                self.input_values_layout.addWidget(parameter, row + 1, col)
        print("[End]   fill_input_grid")
        # super().show()

    def generate_input(self, creation_method):
        print("[Start] generate_input")
        if creation_method == self.create_tasks:
            print("Creation method is: user method")
            user_values = self.get_user_values()
            self.tasks_list = creation_method(
                min_time=user_values.get("min_time"),
                max_time=user_values.get("max_time"),
                tasks_number=user_values.get("tasks_number")
            )
        elif creation_method == self.create_tasks_default:
            print("Creation method is: default method")
            self.tasks_list = creation_method(values=DEFAULT_TASK_VALUES)
        else:
            raise Exception(f"Given tasks creation method:\n\t{creation_method}\nis not a user creation method:\n\t{self.create_tasks}\nand not a default creation method:\n\t{self.create_tasks_default}")

        tasks_print_table = []
        for task in self.tasks_list:
            task_row = [task, task.execution_time, task.release_time, task.deadline]
            tasks_print_table.append(task_row)
        # print data
        self.fill_input_grid(tasks_print_table)
        print("[End]   generate_input")

    def perform_alg(self, tasks):
        tasks_exec_order = []
        # init before the start
        T = 0
        while True:
            # break check - if all tasks are done:
            if not any([task.not_done for task in tasks]):
                break

            # find tasks that can be executed in current timepoint
            available_tasks = [task for task in tasks if task.release_time <= T and task.not_done]
            # print(f"time: {T}, available tasks: {available_tasks}")

            if len(available_tasks) > 0:
                # get task with closes deadline
                min_deadline = -1
                chosen_task = None
                for task in available_tasks:
                    if task.deadline < min_deadline or min_deadline < 0:
                        min_deadline = task.deadline
                        chosen_task = task

                print(f"running: {chosen_task}")
                tasks_exec_order.append(chosen_task)
                # set "start" time for chosen task (if not set only)
                if chosen_task.start_time is None:
                    print(f"task {chosen_task}, setting start time to: {T}")
                    chosen_task.start_time = T
                # run task for 1s
                chosen_task.current_execution_time += 1

                # check if task should be done
                if chosen_task.current_execution_time == chosen_task.execution_time:
                    chosen_task.not_done = False
                    chosen_task.stop_time = T + 1  # +1 because task was executed for 1 time unit
            else:
                tasks_exec_order.append("---")

            # end of the loop
            T += 1
        return tasks_exec_order

    def fill_output_grid(self, tasks_list):
        print("[Start] fill_output_grid")
        tasks_n_label = QLabel("<h2>Task</h2>")
        p_label = QLabel("<h2>Start</h2>")
        r_label = QLabel("<h2>Stop</h2>")
        d_label = QLabel("<h2>Li</h2>")
        tasks_n_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        p_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        d_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_values_layout.addWidget(tasks_n_label, 0, 0)
        self.output_values_layout.addWidget(p_label, 0, 1)
        self.output_values_layout.addWidget(r_label, 0, 2)
        self.output_values_layout.addWidget(d_label, 0, 3)

        for row, task in enumerate(tasks_list):
            color = task[0].task_color
            for col, task_parameter in enumerate(task):
                parameter = QLabel(f"<h2>{str(task_parameter)}</h2>")
                parameter.setAlignment(Qt.AlignmentFlag.AlignCenter)
                parameter.setFixedWidth(TASK_LABEL_WIDTH)
                parameter.setStyleSheet(f"background-color: {color}")
                self.output_values_layout.addWidget(parameter, row + 1, col)
        print("[End]   fill_output_grid")

    def fill_graph_layout(self, tasks_exec_order, lmax):
        print("[Start] fill_graph_layout")
        for idx, task in enumerate(tasks_exec_order):
            # add task to tasks row
            graph_cell = QLabel(f"<h2>{str(task)}</h2>")
            graph_cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # graph_cell.setFixedWidth(TASK_LABEL_WIDTH)
            if isinstance(task, Task):
                graph_cell.setStyleSheet(f"background-color: {task.task_color}")
            if isinstance(task, str):
                graph_cell.setStyleSheet(f"background-color: {EMPTY_COLOR}")
            self.graph_values_layout.addWidget(graph_cell, 0, idx)

            # add time index
            time_label = QLabel(f"<p>{idx}</p>")
            time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.graph_values_layout.addWidget(time_label, 1, idx)

        self.graph_quarter_layout.addWidget(QLabel(f"<h2>L<sub>max</sub>: {lmax}</h2>"), alignment=Qt.AlignmentFlag.AlignCenter)
        print("[End]   fill_graph_layout")

    def order_tasks(self):
        # run Liu algorithm
        tasks_exec_order = self.perform_alg(self.tasks_list)
        # get tasks Li values
        for task in self.tasks_list:
            task.delay = task.stop_time - task.deadline if task.stop_time > task.deadline else 0  # delay can't be negative
        # get Lmax
        lmax = max(task.delay for task in self.tasks_list)
        # prepare data for printing
        tasks_print_table = []
        for task in self.tasks_list:
            task_row = [task, task.start_time, task.stop_time, task.delay]
            tasks_print_table.append(task_row)
        # print data
        self.fill_output_grid(tasks_print_table)
        print(f"Tasks order: {tasks_exec_order}")
        self.fill_graph_layout(tasks_exec_order, lmax)

    def _connect_signals_and_slots(self):
        self.button_user.clicked.connect(partial(self.generate_input, self.create_tasks))
        self.button_default.clicked.connect(partial(self.generate_input, self.create_tasks_default))
        self.button_run_alg.clicked.connect(self.order_tasks)


if __name__ == "__main__":
    app = QApplication([])
    w = LiuWindow()
    w.show()
    sys.exit(app.exec())
