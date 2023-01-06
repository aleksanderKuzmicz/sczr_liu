class LiuModel:
    @staticmethod
    def perform_alg(tasks):
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