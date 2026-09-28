from client import CPUSchedulerSimulator

def main():
    sched = CPUSchedulerSimulator()
    procs = [("P1", 0, 5), ("P2", 1, 3), ("P3", 2, 1)]
    res = sched.round_robin(procs, quantum=2)
    print("CPU Scheduler Simulator Verification:")
    print(f"Total Schedule Time: {res['total_time']}")
    print(f"Completion Times: {res['completion_times']}")

if __name__ == "__main__":
    main()
