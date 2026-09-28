import sys
import json
from client import CPUSchedulerSimulator

sched = CPUSchedulerSimulator()

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-cpu-scheduler-round-robin-cfs-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "simulate_round_robin",
                    "description": "Simulate CPU round-robin scheduling for processes with arrival and burst times",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "processes": {
                                "type": "array",
                                "items": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "description": "Array of [pid, arrival_time, burst_time]"
                            },
                            "quantum": {"type": "integer", "default": 2}
                        },
                        "required": ["processes"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "simulate_round_robin":
            procs = [(p[0], int(p[1]), int(p[2])) for p in args.get("processes", [])]
            q = args.get("quantum", 2)
            data = sched.round_robin(procs, quantum=q)
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
