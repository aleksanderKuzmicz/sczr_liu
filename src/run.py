from src.configuration.config import DEFAULT, DEFAULT_TASK_VALUES, T_MAX, T_MIN, N
from src.liu_alg_implementation import Model


if __name__ == "__main__":
    if DEFAULT:
        tasks_list = Model.create_tasks_default(DEFAULT_TASK_VALUES)
    else:
        tasks_list = Model.create_tasks(T_MIN, T_MAX, N)

    # TODO: print Input Data to the GUI table
    print(f"Created task list: {tasks_list}")
    Model.perform_alg(tasks_list)
