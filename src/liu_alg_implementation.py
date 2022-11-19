import random

DEFAULT = True
DEFAULT_VALUES = [
        [2, 4, 7],
        [1, 1, 2],
        [2, 0, 3],
        [1, 4, 5],
        [3, 2, 6],
    ]
T_MIN = 1
T_MAX = 4
N = 5


class Task:
    done_status: bool = None
    # Data required for algorith
    release_time: int = None
    execution_time: int = None
    deadline: int = None
    # Data after the
    start_time: int = None
    stop_time: int = None
    delay: int = None

    executed_time: int = None

    def __init__(self, p, r, d):
        self.executed_time = p
        self.release_time = r
        self.deadline = d


def create_tasks(min_time, max_time, tasks_number):
    tasks_list = []
    for el in range(tasks_number):
        execution_time = random.randint(min_time, max_time)
        release_time = random.randint(min_time, max_time)
        deadline = release_time + execution_time + random.randint(min_time, max_time)

        tasks_list.append(Task(p=execution_time, r=release_time, d=deadline))
    return tasks_list


def create_tasks_default(values):
    tasks_list = [Task(p=el[1], r=el[0], d=el[2]) for el in values]
    return tasks_list


class Algos:
    @staticmethod
    def perform_alg(Tasks):
        pass
        # T is current time
        # 0 - get pool of available (release tima and status(if done or not) tasks for T
        # 1 - find Task with closest deadline
        # 2 - run that task for 1 time unit
        # 2.1 T+=1
        # 3 - if task is done - set status to done
        # 4 - Break if all tasks are done (check statuses)




if __name__ == "__main__":
    if DEFAULT:
        tasks_list = create_tasks_default(DEFAULT_VALUES)
    else:
        tasks_list = create_tasks(T_MIN, T_MAX, N)

    # TODO: print Input Data to the GUI table



