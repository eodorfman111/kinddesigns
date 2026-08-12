"""
Runs the trained species detector on the Kind Designs demo clip with
ByteTrack (via `supervision`) so detections persist across frames instead of
flickering in/out — each fish gets a track ID, and boxes are held through
brief misses (occlusion, a bad-conf frame) instead of disappearing every time
a single frame's detection dips below threshold.

Usage:
    python render_detection.py
"""
import subprocess
from collections import deque
from pathlib import Path

import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO

BASE = Path(__file__).parent
SOURCE = BASE / "footage" / "kinddesigns_source.mp4"
MODEL_PATH = BASE / "models" / "species_v1.pt"
OVERLAY_OUT = BASE / "kinddesigns_boxes_overlay.mp4"
WEB_OUT = BASE / "kinddesigns_boxes_web.mp4"

CLASS_COLORS_HEX = {
    "Bluehead Wrasse": "#38B4DB",
    "French Grunt": "#F0C456",
    "Parrotfish": "#E65AAC",
    "Porkfish": "#FFC83C",
    "Sergeant major": "#B4DB38",
    "White Grunt": "#C8C8C8",
}
COUNT_SMOOTH_FRAMES = 15
CONF = 0.12          # lower than single-frame use — ByteTrack's own confirmation
                      # logic (track age + IoU continuity) filters noise instead
                      # of relying on per-frame confidence alone
IMGSZ = 1920
LOST_TRACK_BUFFER = 12  # frames a track survives with no detection before it's dropped
MINIMUM_CONSECUTIVE_FRAMES = 2  # frames a track must be seen before it's drawn


def run():
    model = YOLO(str(MODEL_PATH), task="detect")
    class_names = model.names
    palette = sv.ColorPalette.from_hex([CLASS_COLORS_HEX[class_names[i]] for i in sorted(class_names)])

    tracker = sv.ByteTrack(lost_track_buffer=LOST_TRACK_BUFFER,
                            minimum_consecutive_frames=MINIMUM_CONSECUTIVE_FRAMES)
    box_annotator = sv.BoxAnnotator(color=palette, thickness=2)
    label_annotator = sv.LabelAnnotator(color=palette, text_scale=0.4, text_thickness=1,
                                         text_padding=3, smart_position=True)

    cap = cv2.VideoCapture(str(SOURCE))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    TOTAL = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(OVERLAY_OUT), fourcc, fps, (W, H))

    count_hist = deque(maxlen=COUNT_SMOOTH_FRAMES)
    frame_idx = 0
    print(f"Processing {TOTAL} frames @ {fps:.1f} fps with ByteTrack ...")
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        results = model(frame, conf=CONF, imgsz=IMGSZ, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = tracker.update_with_detections(detections)

        labels = [f"{class_names[cls_id]} {conf:.2f}"
                  for cls_id, conf in zip(detections.class_id, detections.confidence)]

        frame = box_annotator.annotate(scene=frame, detections=detections)
        frame = label_annotator.annotate(scene=frame, detections=detections, labels=labels)

        n = len(detections)
        count_hist.append(n)
        smoothed = round(sum(count_hist) / len(count_hist))

        font = cv2.FONT_HERSHEY_DUPLEX
        card_w, card_h = 190, 80
        cv2.rectangle(frame, (14, 14), (14 + card_w, 14 + card_h), (18, 12, 8), -1)
        cv2.rectangle(frame, (14, 14), (14 + card_w, 14 + card_h), (180, 219, 56), 1)
        cv2.putText(frame, "LIVE DETECTIONS", (28, 38), font, 0.4, (150, 170, 185), 1, cv2.LINE_AA)
        cv2.putText(frame, str(smoothed), (28, 74), font, 1.0, (180, 219, 56), 2, cv2.LINE_AA)

        watermark = "KIND DESIGNS DEMO -- NOT ACTUAL SITE FOOTAGE"
        (tw, _), _ = cv2.getTextSize(watermark, font, 0.42, 1)
        cv2.putText(frame, watermark, (W - tw - 14, H - 16), font, 0.42,
                    (255, 255, 255), 1, cv2.LINE_AA)

        writer.write(frame)
        if frame_idx % 60 == 0:
            print(f"  [{frame_idx:4d}/{TOTAL}]  tracked={n}  smoothed={smoothed}")
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
