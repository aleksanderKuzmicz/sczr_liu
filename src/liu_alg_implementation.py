import random

from src.configuration.config import DEFAULT, DEFAULT_TASK_VALUES, T_MAX, T_MIN, N


class Task:
    task_number = 0  # TODO: change to 0 or -1
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


class Model:

    @staticmethod
    def create_tasks(min_time, max_time, tasks_number):
        print("[start] Model: create_tasks")
        tasks_list = []
        for el in range(tasks_number):
            execution_time = random.randint(min_time, max_time)
            release_time = random.randint(min_time, max_time)
            deadline = release_time + execution_time + random.randint(min_time, max_time)

            tasks_list.append(Task(p=execution_time, r=release_time, d=deadline))
        print("[end]   Model: create_tasks")
        return tasks_list

    @staticmethod
    def create_tasks_default(values):
        tasks_list = [Task(p=el[0], r=el[1], d=el[2]) for el in values]
        return tasks_list

    @staticmethod
    def perform_alg(tasks):
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

                # run task for 1s
                chosen_task.current_execution_time += 1

                # check if task should be done
                if chosen_task.current_execution_time == chosen_task.execution_time:
                    chosen_task.not_done = False

            # end of the loop
            T += 1


if __name__ == "__main__":
    if DEFAULT:
        tasks_list = Model.create_tasks_default(DEFAULT_TASK_VALUES)
    else:
        tasks_list = Model.create_tasks(T_MIN, T_MAX, N)

    # TODO: print Input Data to the GUI table
    print(f"Created task list: {tasks_list}")
    Model.perform_alg(tasks_list)
