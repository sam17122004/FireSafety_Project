#!/usr/bin/env python3
import argparse, cv2, numpy as np, time, os, pathlib

def build_tracker(name):
    name = name.upper()
    if name == "KCF":
        return cv2.TrackerKCF_create()
    if name == "CSRT":
        return cv2.TrackerCSRT_create()
    if name == "MOSSE":
        return cv2.legacy.TrackerMOSSE_create()
    return cv2.TrackerKCF_create()

def detect_fire_regions(frame):
    # Resize for speed
    resized = cv2.resize(frame, (640, 360))
    blur = cv2.GaussianBlur(resized, (5,5), 0)

    # Convert to YCrCb for fire-like chrominance, and HSV for saturation/brightness
    ycrcb = cv2.cvtColor(blur, cv2.COLOR_BGR2YCrCb)
    Y, Cr, Cb = cv2.split(ycrcb)

    # Empirical thresholds for fire colors (tune per environment)
    fire_mask1 = (Cr > 140) & (Cb < 120) & (Y > 100)
    fire_mask1 = fire_mask1.astype(np.uint8) * 255

    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    H,S,V = cv2.split(hsv)
    # High saturation and brightness, warm hues
    fire_mask2 = ((H < 50) | (H > 170)) & (S > 100) & (V > 150)
    fire_mask2 = fire_mask2.astype(np.uint8) * 255

    mask = cv2.bitwise_and(fire_mask1, fire_mask2)

    # Morphology to clean noise
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < 500:  # ignore tiny
            continue
        x,y,w,h = cv2.boundingRect(c)
        boxes.append((x,y,w,h))

    scale_x = frame.shape[1]/resized.shape[1]
    scale_y = frame.shape[0]/resized.shape[0]
    boxes = [(int(x*scale_x), int(y*scale_y), int(w*scale_x), int(h*scale_y)) for (x,y,w,h) in boxes]
    return boxes, mask

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="0", help="0 for webcam or path to video")
    ap.add_argument("--tracker", default="CSRT", choices=["KCF","CSRT","MOSSE"])
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--save", default="", help="output dir to save annotated video")
    args = ap.parse_args()

    source = 0 if args.source == "0" else args.source
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise SystemExit("Could not open source")

    writer = None
    if args.save:
        pathlib.Path(args.save).mkdir(parents=True, exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out_path = os.path.join(args.save, "annotated_output.mp4")
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(out_path, fourcc, fps, (w,h))

    tracker = None
    tracking = False
    last_boxes = []

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        boxes, mask = detect_fire_regions(frame)

        # Initialize / update tracker using largest box
        if boxes:
            # pick largest
            x,y,w,h = max(boxes, key=lambda b: b[2]*b[3])
            if not tracking:
                tracker = build_tracker(args.tracker)
                tracker.init(frame, (x,y,w,h))
                tracking = True
                last_boxes = [(x,y,w,h)]
            else:
                ok, b = tracker.update(frame)
                if ok:
                    x,y,w,h = map(int, b)
                    last_boxes = [(x,y,w,h)]
                else:
                    tracking = False
                    last_boxes = boxes
        else:
            tracking = False
            last_boxes = []

        # Draw
        for (x,y,w,h) in last_boxes:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, "FIRE (classical)", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        if args.show:
            dv = cv2.imshow("Fire Detection", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        if writer is not None:
            writer.write(frame)

    cap.release()
    if writer is not None:
        writer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
