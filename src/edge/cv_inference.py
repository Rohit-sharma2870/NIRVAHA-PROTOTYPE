import cv2, time, argparse, numpy as np
import requests, json
try:
    import mediapipe as mp
except Exception as e:
    mp = None
    print("Warning: mediapipe not available. Landmarks disabled. Install dependencies.")

def eye_aspect_ratio(pts):
    # pts: 6x2 for one eye. Here we approximate with vertical/horizontal distances.
    if pts is None or len(pts) < 6:
        return 0.3
    v = np.linalg.norm(pts[1]-pts[5]) + np.linalg.norm(pts[2]-pts[4])
    h = np.linalg.norm(pts[0]-pts[3]) + 1e-6
    return float(v/(2*h))

def estimate_metrics(frame, face_mesh):
    h, w = frame.shape[:2]
    metrics = {"ear": 0.3, "blink": 0.0, "gaze_off": 0.0, "yawn": 0.0}
    if face_mesh is None:
        return metrics
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = face_mesh.process(rgb)
    if not res.multi_face_landmarks:
        metrics["gaze_off"] = 1.0
        return metrics
    lm = res.multi_face_landmarks[0]
    # sample landmark indices for left eye (MediaPipe Face Mesh)
    LEFT = [33, 160, 158, 133, 153, 144]
    pts = np.array([[lm.landmark[i].x*w, lm.landmark[i].y*h] for i in LEFT], dtype=np.float32)
    ear = eye_aspect_ratio(pts)
    metrics["ear"] = ear
    metrics["blink"] = 1.0 if ear < 0.23 else 0.0
    # crude gaze proxy: x position away from center
    cx = np.mean(pts[:,0])/w
    metrics["gaze_off"] = float(abs(cx - 0.5) > 0.18)
    return metrics

def state_from_metrics(m, prev_state):
    score = 0.0
    if m["blink"] > 0.5 or m["ear"] < 0.20:
        return "DROWSY", 0.9
    if m["gaze_off"] > 0.5:
        return "DISTRACTED", 0.7
    return "ATTENTIVE", 0.1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cam", type=int, default=0)
    ap.add_argument("--api", type=str, default="http://127.0.0.1:8000")
    ap.add_argument("--show", action="store_true")
    args = ap.parse_args()

    cap = cv2.VideoCapture(args.cam)
    face_mesh = None
    if mp is not None:
        face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
    prev = "ATTENTIVE"

    while True:
        ok, frame = cap.read()
        if not ok: break
        m = estimate_metrics(frame, face_mesh)
        state, score = state_from_metrics(m, prev)
        prev = state

        payload = {
            "state": state,
            "score": float(score),
            "metrics": {k: float(v) for k,v in m.items()},
            "ts": time.time()
        }
        try:
            requests.post(args.api + "/state", json=payload, timeout=0.25)
        except Exception:
            pass

        if args.show:
            cv2.putText(frame, f"STATE: {state}", (16,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.imshow("NIRVAHA Edge", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
