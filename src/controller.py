from src.gui import LiuWindow
from src.liu_alg_implementation import Model


class LiuController:
    def __init__(self, view: LiuWindow, model: Model):
        print("[start] Controller: __init__")
        self._view = view
        self._model = model
        self._connect_signals_and_slots()
        print("[end]   Controller: __init__")

    def _create_user_tasks(self):
        print("[start] Controller: _create_user_tasks")
        user_values = self._view.return_user_values()
        tasks_list = self._model.create_tasks(
            min_time=user_values.get("min_time"),
            max_time=user_values.get("max_time"),
            tasks_number=user_values.get("tasks_number")
        )
        return tasks_list

    def _show_tasks(self, tasks_list):
        # move to private method
        tasks_print_table = []
        for task in tasks_list:
            task_row = [str(task), task.execution_time, task.release_time, task.deadline]
            tasks_print_table.append(task_row)
        # end of private method
        self._view.fill_input_quarter(tasks_print_table)
        print("[end]   Controller: _create_user_tasks")

    def create_show_tasks(self):
        tasks = self._create_user_tasks()
        self._show_tasks(tasks)

    def foo(self):
        print("Foo has been called")

    def _connect_signals_and_slots(self):
        print("[start] Controller: _connect_signals_and_slots")
        # connect tasks creation options
        self._view.user_tasks_number.returnPressed.connect(self.create_show_tasks)
        self._view.button_fill_input.clicked.connect(self.foo)
        self._view.foo_button.clicked.connect(self.foo)
        print("[end]   Controller: _connect_signals_and_slots", end="\n\n")

