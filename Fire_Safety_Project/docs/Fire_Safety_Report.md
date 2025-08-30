# Fire Safety AIIMS – Technical Report

## Abstract
This report presents a practical pipeline for industrial fire detection and tracking using OpenCV with optional deep learning, integrated with simulated IoT sensors and MQTT-based alerting.

## Method
- **Classical CV**: YCrCb + HSV thresholding + morphology to isolate fire-like regions.
- **Tracking**: CSRT/KCF to maintain stable bounding boxes.
- **AI Option**: Lightweight CNN (PyTorch) for binary classification fire/no-fire.
- **IoT**: Synthetic temperature/smoke/gas streams; threshold logic can escalate alerts.

## Results (Starter)
This repository provides runnable code; quantitative results depend on your dataset and plant conditions.

## Limitations & Future Work
- False positives under warm light or reflective surfaces.
- Consider smoke-specific features, temporal consistency, and multisensor fusion.
