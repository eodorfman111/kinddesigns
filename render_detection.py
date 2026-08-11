"""
Runs the real fish detector (leodorf/fishvision-detector, cached locally) on the
South Florida reef clip and renders a boxed-detection video for the Kind Designs
pitch demo. Real inference, real footage (not their wall) — see project notes.

Usage:
    python render_detection.py
"""
import subprocess
from collections import deque
from pathlib import Path

import cv2
from ultralytics import YOLO

BASE = Path(__file__).parent
SOURCE = BASE / "footage" / "kinddesigns_source.mp4"
MODEL_PATH = BASE / "models" / "best_v1.08.pt"
OVERLAY_OUT = BASE / "kinddesigns_boxes_overlay.mp4"
WEB_OUT = BASE / "kinddesigns_boxes_web.mp4"

BOX_COLOR = (180, 219, 56)   # BGR — teal/seafoam accent
COUNT_SMOOTH_FRAMES = 15
CONF = 0.12
IMGSZ = 1280


def run():
    model = YOLO(str(MODEL_PATH), task="detect")
    cap = cv2.VideoCapture(str(SOURCE))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    TOTAL = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(OVERLAY_OUT), fourcc, fps, (W, H))

    count_hist = deque(maxlen=COUNT_SMOOTH_FRAMES)
    frame_idx = 0
    print(f"Processing {TOTAL} frames @ {fps:.1f} fps ...")
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        results = model(frame, conf=CONF, imgsz=IMGSZ, verbose=False)
        boxes = results[0].boxes

        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                score = float(box.conf[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOR, 2)
                label = f"fish {score:.2f}"
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 6, y1), BOX_COLOR, -1)
                cv2.putText(frame, label, (x1 + 3, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 15, 20), 1, cv2.LINE_AA)

        n = len(boxes) if boxes is not None else 0
        count_hist.append(n)
        smoothed = round(sum(count_hist) / len(count_hist))

        font = cv2.FONT_HERSHEY_DUPLEX
        card_w, card_h = 190, 80
        cv2.rectangle(frame, (14, 14), (14 + card_w, 14 + card_h), (18, 12, 8), -1)
        cv2.rectangle(frame, (14, 14), (14 + card_w, 14 + card_h), BOX_COLOR, 1)
        cv2.putText(frame, "LIVE DETECTIONS", (28, 38), font, 0.4, (150, 170, 185), 1, cv2.LINE_AA)
        cv2.putText(frame, str(smoothed), (28, 74), font, 1.0, BOX_COLOR, 2, cv2.LINE_AA)

        watermark = "KIND DESIGNS DEMO -- NOT ACTUAL SITE FOOTAGE"
        (tw, _), _ = cv2.getTextSize(watermark, font, 0.42, 1)
        cv2.putText(frame, watermark, (W - tw - 14, H - 16), font, 0.42,
                    (255, 255, 255), 1, cv2.LINE_AA)

        writer.write(frame)
        if frame_idx % 60 == 0:
            print(f"  [{frame_idx:4d}/{TOTAL}]  detections={n}  smoothed={smoothed}")
        frame_idx += 1

    cap.release()
    writer.release()

    subprocess.run([
        "ffmpeg", "-y", "-i", str(OVERLAY_OUT),
        "-vcodec", "libx264", "-crf", "23", "-preset", "fast",
        "-pix_fmt", "yuv420p", str(WEB_OUT)
    ], check=True, capture_output=True)
    print(f"\nDone. Web video -> {WEB_OUT}")


if __name__ == "__main__":
    run()
