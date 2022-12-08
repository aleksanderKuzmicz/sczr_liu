import sys

from src.configuration.config import DEFAULT, DEFAULT_TASK_VALUES, T_MAX, T_MIN, N
from src.liu_alg_implementation import Model
from src.gui import QApplication, LiuWindow
from src.controller import LiuController


if __name__ == "__main__":
    # # TODO: get default from python run.py args
    # if DEFAULT:
    #     tasks_list = Model.create_tasks_default(DEFAULT_TASK_VALUES)
    # else:
    #     pass
        # tasks_list = Model.create_tasks(T_MIN, T_MAX, N)

    # print(f"Created task list: {tasks_list}")
    # Model.perform_alg(tasks_list)

    liu_app = QApplication([])
    liu_window = LiuWindow()
    liu_model = Model()
    liu_window.show()
    LiuController(liu_window, liu_model)

    return_code = liu_app.exec()
    sys.exit(return_code)
