#!/usr/bin/env python3
import json, time, os, sys

STATE_FILE = os.path.expanduser("~/.config/eww/scripts/pomodoro_state.json")

DEFAULT_STATE = {"phase": "Work", "remaining": 1500, "progress": 0.0, "running": False, "start_time": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return DEFAULT_STATE.copy()

def start():
    state = load_state()
    state["running"] = True
    state["start_time"] = time.time()
    save_state(state)
    print("Pomodoro iniciado")

def stop():
    state = load_state()
    state["running"] = False
    save_state(state)
    print("Pomodoro detenido")

def reset():
    save_state(DEFAULT_STATE)
    print("Pomodoro reiniciado")

def status():
    state = load_state()
    if state["running"] and state["start_time"]:
        elapsed = time.time() - state["start_time"]
        remaining = max(0, 1500 - int(elapsed))
        state["remaining"] = remaining
        state["progress"] = min(1.0, elapsed / 1500)
    minutes = state["remaining"] // 60
    seconds = state["remaining"] % 60
    print(json.dumps({
        "phase": state["phase"],
        "remaining": f"{minutes:02d}:{seconds:02d}",
        "progress": state["progress"]
    }))

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "start": start()
    elif cmd == "stop": stop()
    elif cmd == "reset": reset()
    elif cmd == "status": status()
