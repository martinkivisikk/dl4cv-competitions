# Kaggle Competition Report

**Course:** Deep Learning for Computer Vision  
**Team members:** [names]

---

## 1. Traffic Sign Detection

### Problem

Detect eight categories of Estonian traffic signs (crosswalk, no entry, speed limit, yield, no stopping, no parking, direction of road, bus stop) in photos collected in Tartu and Tallinn under varied lighting and weather conditions. Submissions are evaluated with mAP@50. The dataset contains 708 training images and 167 held-out test images with 1087 total annotations. The classes are naturally imbalanced, with crosswalk appearing roughly twice as often as bus stop.

### Approach

We experimented with two families of object detectors.

**One-stage CNN detectors (YOLO).** We first established a baseline using YOLOv8n (nano), the lightest variant of the YOLOv8 family, trained for 50 epochs at 640×640 with standard Ultralytics augmentations (mosaic, random flip, HSV jitter). We also evaluated YOLO26n, a newer compact variant from the YOLO family, across several training budgets and resolutions. Increasing the input resolution to 768 produced near-perfect validation scores (mAP50 ≈ 0.994) but did not improve test performance, indicating overfitting on the small training set.

**Transformer-based detector (RT-DETR).** RT-DETR-l uses a ResNet backbone fed into a transformer encoder-decoder, replacing the convolutional detection head with cross-attention over learned object queries. Unlike YOLO's anchor-based sliding window, it reasons globally over the image, which is advantageous when signs appear at varying scales and in cluttered backgrounds. We trained RT-DETR-l for 15 epochs at 640×640 with batch size 8, using max epochs=50 and early stopping with patience 15.

### Results

| Model | Val mAP@50 | Public test mAP@50 |
|---|---|---|
| YOLOv8n (10 epochs) | 0.951 | 0.891 |
| YOLOv8n (50 epochs) | 0.965 | 0.908 |
| YOLO26n (32 epochs) | 0.901 | 0.845 |
| RT-DETR-l (~15 epochs, early stop) | 0.919 | **0.935** |
| Competition baseline | — | 0.944 |

RT-DETR-l achieved the best test score (0.935), narrowing the gap to the 0.944 competition baseline. Continued training beyond the best checkpoint degraded test performance to 0.892, consistent with the overfitting pattern observed in the YOLO runs. The small dataset size (708 images) was the dominant limiting factor throughout.

---

## 2. [Competition name]

### Problem

[description]

### Approach

[approach]

### Results

| Model | Score |
|---|---|
| [model] | [score] |

---

## 3. [Competition name]

### Problem

[description]

### Approach

[approach]

### Results

| Model | Score |
|---|---|
| [model] | [score] |

---

## 4. [Competition name]

### Problem

[description]

### Approach

[approach]

### Results

| Model | Score |
|---|---|
| [model] | [score] |

---

## Summary

| Competition | Best score | Baseline | Δ |
|---|---|---|---|
| Traffic sign detection | 0.935 | 0.944 | −0.009 |
| [Competition 2] | | | |
| [Competition 3] | | | |
| [Competition 4] | | | |

The key challenge was working with limited training data. Transformer-based architectures (RT-DETR) proved more competitive than compact CNN-based detectors on the traffic sign task, while careful regularisation and early stopping were critical to avoid overfitting.
