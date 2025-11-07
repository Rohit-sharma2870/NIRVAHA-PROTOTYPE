import time, argparse, random, requests

def random_state():
    r = random.random()
    if r < 0.7: return "ATTENTIVE", 0.1
    if r < 0.85: return "DISTRACTED", 0.7
    return "DROWSY", 0.9

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default="http://127.0.0.1:8000")
    args = ap.parse_args()
    while True:
        s, sc = random_state()
        payload = {"state": s, "score": sc,
                   "metrics": {"ear": 0.25, "blink": 0.0, "gaze_off": 0.0},
                   "ts": time.time()}
        try:
            requests.post(args.api + "/state", json=payload, timeout=0.25)
        except Exception:
            pass
        time.sleep(1.0)

if __name__ == "__main__":
    main()
