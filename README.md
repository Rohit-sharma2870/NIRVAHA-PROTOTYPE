# NIRVĀHA — AI-Enhanced Driver Wellness (Prototype)

> Minimal end‑to‑end prototype to demo real‑time driver state monitoring (drowsy/stressed/distracted) with edge inference, a simple API, and a lightweight dashboard.

## What this is
- **Edge CV loop**: Webcam/cabin cam → face/eye landmarks → simple blink/yawn/focus metrics.
- **Driver state engine**: Heuristics combine metrics into `ATTENTIVE`, `DROWSY`, or `DISTRACTED`.
- **Actions**: Stubbed cabin controls (lights/music prompts) + voice/beep alerts.
- **API (FastAPI)**: Exposes current state and metrics.
- **Fleet sim**: Generates sample trips for demos if you don't have a camera.
- **Dashboard**: Simple web UI that polls the API.

> This is a prototype scaffold — plug in your models/datasets and iterate.

## Quickstart

### 1) Clone & set up
```bash
git clone https://github.com/<your-username>/nirvaha-prototype.git
cd nirvaha-prototype
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run edge loop (webcam required)
```bash
python src/edge/cv_inference.py --show --api http://127.0.0.1:8000
```

### 3) Start API
```bash
uvicorn src.backend.api:app --reload --port 8000
```

### 4) Open dashboard
```bash
python -m http.server 5173 -d dashboard
# visit http://localhost:5173
```

### 5) No camera? Use simulator
```bash
python src/fleet/simulator.py --api http://127.0.0.1:8000
```

## Repo layout
```
src/
 ├─ edge/            # camera → metrics → state (+ optional on‑device model)
 ├─ backend/         # FastAPI for state & metrics
 ├─ gateway/         # MQTT/REST stubs for CAN, wearables
 ├─ fleet/           # data generators + log replay
dashboard/           # minimal HTML/JS UI
examples/            # sample configs
tests/               # pytest sanity checks
```

## Replaceable components
- **Landmarks/vision**: Start with MediaPipe Face Mesh; swap to YOLO/RTMPose later.
- **State engine**: Heuristics now; replace with LSTM/Transformer on time‑series.
- **Actions**: Map to actual CAN bus / seat / light controllers when hardware is ready.

## Safety note
Prototype only. Do not use while driving. Evaluate in a lab/simulated environment.

## License
MIT
