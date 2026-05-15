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

## 2. Vehicle Type Classification

### Problem

Classify 10 vehicle body types (SUV, bus, convertible, coupe, hatchback, pickup, sedan, station wagon, truck, van) from 224×224 images. The dataset contains 802 labelled training images (~80 per class) and 201 unlabelled test images. Submissions are evaluated with accuracy.

### Approach

With only ~80 images per class, fine-tuning a pretrained CNN end-to-end led to severe overfitting: the model memorised the training distribution (sourced at 224×224) and failed on test images (sourced at 256×256). Full fine-tuning of EfficientNet-B2 achieved 94% validation accuracy but only 48% on the public test set; staged fine-tuning (frozen backbone then partial unfreeze) gave the same test score.

The effective approach was to treat pretrained backbones purely as **frozen feature extractors** and train a lightweight classifier on the extracted features. We extracted features from both EfficientNet-B2 (1408-dim) and ViT-B/16 (768-dim), applied 4-view feature-level TTA (original, H-flip, center-crop, H-flip+crop), concatenated the two feature vectors, and trained a logistic regression on the combined 2176-dim representation. This avoids distorting generalised ImageNet features with the small, domain-specific training set.

### Results

| Model | Val acc | Public test acc |
|---|---|---|
| EfficientNet-B2, full fine-tune (30 epochs) | 0.943 | 0.484 |
| EfficientNet-B2, staged fine-tune | 0.943 | 0.484 |
| EfficientNet-B2 features + LogReg | 0.930 | 0.581 |
| EfficientNet-B2 + ViT-B/16 features + TTA + LogReg | 0.931 | 0.677 |
| EfficientNet-B2 + ViT-B/16 features + TTA + LogReg (full train) | — | **0.694** |
| Competition baseline | — | 0.790 |

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
| Vehicle type classification | 0.694 | 0.790 | −0.096 |
| [Competition 3] | | | |
| [Competition 4] | | | |

The key challenge was working with limited training data. Transformer-based architectures (RT-DETR) proved more competitive than compact CNN-based detectors on the traffic sign task, while careful regularisation and early stopping were critical to avoid overfitting.
