import random
from functools import partial

from src.configuration.config import DEFAULT_TASK_VALUES
from src.configuration.config import COLOR_PALETTE, EMPTY_COLOR, TASK_LABEL_WIDTH

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


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


class LiuController:
    view = None
    model = None
    tasks_list = None

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self._connect_signals_and_slots()

    def _validate_user_values(self, user_values):
        if user_values['min_time'].isnumeric() and \
                user_values['max_time'].isnumeric() and \
                user_values['tasks_number'].isnumeric() and \
                0 <= int(user_values['min_time']) <= 10 and \
                0 < int(user_values['max_time']) <= 30 and \
                0 < int(user_values['tasks_number']) <= 10:
            print("Validation - returning TRUE")
            return True
        else:
            print("Validation - returning Flase")
            return False

    def _convert_values_to_int(self, values):
        return {key: int(value) for key, value in values.items()}

    def _clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def create_tasks(self, **kwargs):
        min_time = kwargs["min_time"]
        max_time = kwargs["max_time"]
        tasks_number = kwargs["tasks_number"]
        print("[Start] create_tasks")
        tasks_list = []
        for el in range(tasks_number):
            execution_time = random.randint(min_time, int(max_time / 3)) + 1
            release_time = random.randint(min_time, max_time)
            deadline = release_time + execution_time + int(3 / 2 * random.randint(min_time, int(max_time / 3)))

            tasks_list.append(Task(p=execution_time, r=release_time, d=deadline))
        print("[End]   create_tasks")
        return tasks_list

    def create_tasks_default(self, **kwargs):
        values = kwargs["values"]
        print("[start] Model: create_tasks_default")
        tasks_list = [Task(p=el[0], r=el[1], d=el[2]) for el in values]
        print("[end]   Model: create_tasks_default")

        return tasks_list

    def fill_input_grid(self):
        print("[Start] fill_input_grid")

        tasks_print_table = []
        for task in self.tasks_list:
            task_row = [task, task.execution_time, task.release_time, task.deadline]
            tasks_print_table.append(task_row)

        tasks_n_label = QLabel("<h2>Task</h2>")
        p_label = QLabel("<h2>p</h2>")
        r_label = QLabel("<h2>r</h2>")
        d_label = QLabel("<h2>d</h2>")
        tasks_n_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        p_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        d_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.view.input_values_layout.addWidget(tasks_n_label, 0, 0)
        self.view.input_values_layout.addWidget(p_label, 0, 1)
        self.view.input_values_layout.addWidget(r_label, 0, 2)
        self.view.input_values_layout.addWidget(d_label, 0, 3)

        for row, task in enumerate(tasks_print_table):
            color = task[0].task_color
            for col, task_parameter in enumerate(task):
                parameter = QLabel(f"{str(task_parameter)}")
                parameter.setAlignment(Qt.AlignmentFlag.AlignCenter)
                parameter.setFixedWidth(TASK_LABEL_WIDTH)
                parameter.setStyleSheet(f"font-size:20px; background-color: {color}")
                self.view.input_values_layout.addWidget(parameter, row + 1, col)
        print("[End]   fill_input_grid")
        # super().show()

    def generate_input(self, creation_method):
        print("[Start] generate_input")
        # clean up
        self._delete_tasks()
        self._clear_layout(self.view.input_values_layout)
        self._clear_layout(self.view.output_values_layout)
        self._clear_layout(self.view.graph_values_layout)
        self.view.lmax_label.setText(f"")

        if creation_method == self.create_tasks:
            user_values = self.view.get_user_values()
            validation_pass = self._validate_user_values(user_values)
            if validation_pass:
                user_values = self._convert_values_to_int(user_values)
                self.view.invalid_params_label.setText("")
                self.tasks_list = creation_method(
                    min_time=user_values.get("min_time"),
                    max_time=user_values.get("max_time"),
                    tasks_number=user_values.get("tasks_number")
                )
            else:
                self.view._clear_user_values()
                self.view.invalid_params_label.setText("Invalid parameters! Try again.")
        elif creation_method == self.create_tasks_default:
            self.view.tasks_list = creation_method(values=DEFAULT_TASK_VALUES)

        if self.tasks_list:
            self.fill_input_grid()
        print("[End]   generate_input")

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
        self.view.output_values_layout.addWidget(tasks_n_label, 0, 0)
        self.view.output_values_layout.addWidget(p_label, 0, 1)
        self.view.output_values_layout.addWidget(r_label, 0, 2)
        self.view.output_values_layout.addWidget(d_label, 0, 3)

        for row, task in enumerate(tasks_list):
            color = task[0].task_color
            for col, task_parameter in enumerate(task):
                parameter = QLabel(f"{str(task_parameter)}")
                parameter.setAlignment(Qt.AlignmentFlag.AlignCenter)
                parameter.setFixedWidth(TASK_LABEL_WIDTH)
                parameter.setStyleSheet(f"background-color: {color}; font-size:20px")
                self.view.output_values_layout.addWidget(parameter, row + 1, col)
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
            self.view.graph_values_layout.addWidget(graph_cell, 0, idx)

            # add time index
            time_label = QLabel(f"<p>{idx}</p>")
            time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.view.graph_values_layout.addWidget(time_label, 1, idx)

        self.view.lmax_label.setText(f"<h2>L<sub>max</sub>= {lmax}</h2>")
        print("[End]   fill_graph_layout")

    def order_tasks(self):
        self._clear_layout(self.view.output_values_layout)
        self._clear_layout(self.view.graph_values_layout)
        self.view.lmax_label.setText(f"")
        # run Liu algorithm
        tasks_exec_order = self.model.perform_alg(self.tasks_list)
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

        # clean up
        self._delete_tasks()

    def _delete_tasks(self):
        if self.tasks_list:
            for task_obj in self.tasks_list:
                print(f"Delete task {task_obj}")
                del task_obj
        self.tasks_list = None
        Task.task_number = 0

    def clear(self):
        print("[Start] clear")
        self._delete_tasks()
        self.view._clear_user_values()
        self._clear_layout(self.view.input_values_layout)
        self._clear_layout(self.view.output_values_layout)
        self._clear_layout(self.view.graph_values_layout)
        self.view.lmax_label.setText(f"")
        print("[End]   clear")

    def _connect_signals_and_slots(self):
        self.view.button_user.clicked.connect(partial(self.generate_input, self.create_tasks))
        self.view.button_default.clicked.connect(partial(self.generate_input, self.create_tasks_default))
        self.view.button_run_alg.clicked.connect(self.order_tasks)
        self.view.button_clear.clicked.connect(self.clear)