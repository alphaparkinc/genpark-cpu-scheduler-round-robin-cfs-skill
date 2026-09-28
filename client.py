"""Preemptive CPU Scheduler Simulation Engine
100% Python Standard Library (collections).
"""

import collections

class CPUSchedulerSimulator:
    """Preemptive Round-Robin and FIFO scheduling engine."""
    def round_robin(self, processes, quantum=2):
        queue = collections.deque()
        time = 0
        p_list = sorted(processes, key=lambda x: x[1])
        idx = 0
        rem_burst = {p[0]: p[2] for p in processes}
        completion_times = {}

        while idx < len(p_list) or queue:
            while idx < len(p_list) and p_list[idx][1] <= time:
                queue.append(p_list[idx][0])
                idx += 1
            if not queue:
                time = p_list[idx][1]
                continue
            curr = queue.popleft()
            exec_time = min(quantum, rem_burst[curr])
            rem_burst[curr] -= exec_time
            time += exec_time

            while idx < len(p_list) and p_list[idx][1] <= time:
                queue.append(p_list[idx][0])
                idx += 1

            if rem_burst[curr] > 0:
                queue.append(curr)
            else:
                completion_times[curr] = time

        return {
            "completion_times": completion_times,
            "total_time": time
        }
