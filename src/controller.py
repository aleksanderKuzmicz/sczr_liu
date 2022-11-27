from src.gui import LuiWindow
from src.liu_alg_implementation import Model

class LiuController:
    def __init__(self, view: LuiWindow, model: Model):
        self._view = view
        self._model = model

    def _create_user_tasks(self):
        user_values = self._view.return_user_values()
        tasks_list = self._model.create_tasks(
            min_time=user_values.get("min_time"),
            max_time=user_values.get("max_time"),
            tasks_number=user_values.get("tasks_number")
        )
        # move to private method
        tasks_print_table = []
        for task in tasks_list:
            task_row = [str(task), task.execution_time, task.release_time, task.deadline]
            tasks_print_table.append(task_row)
        # end of private method
        self._view.print_tasks(tasks_print_table)


    def _connect_signals_and_slots(self):
        pass
