import os
from tqdm import tqdm
from ultralytics import YOLO


def run_inference(model_path, test_dir, class_names, iou=0.5):
    """Runs prediction and returns a list of result dictionaries."""
    model = YOLO(model_path)
    results_list = []

    test_files = [f for f in os.listdir(test_dir) if f.lower().endswith(".jpg")]

    for img_name in tqdm(test_files, desc="Inference"):
        img_path = os.path.join(test_dir, img_name)
        image_id = os.path.splitext(img_name)[0]

        try:
            res = model.predict(img_path, verbose=False, iou=iou)[0]
            boxes = res.boxes

            if boxes is None or len(boxes) == 0:
                results_list.append(
                    {
                        "image_id": image_id,
                        "PredictionString": "No_parking 0.0001 0 0 1 1",
                    }
                )
                continue

            preds = []
            for i in range(len(boxes)):
                conf = boxes.conf[i].item()
                cls_id = int(boxes.cls[i].item())
                xyxy = boxes.xyxy[i].cpu().numpy()
                label = class_names[cls_id].replace(" ", "_")
                preds.append(
                    f"{label} {conf:.4f} {xyxy[0]:.4f} {xyxy[1]:.4f} {xyxy[2]:.4f} {xyxy[3]:.4f}"
                )

            results_list.append(
                {"image_id": image_id, "PredictionString": " ".join(preds)}
            )

        except Exception as e:
            print(f"Error on {img_name}: {e}")
            results_list.append(
                {"image_id": image_id, "PredictionString": "No_parking 0.0001 0 0 1 1"}
            )

    return results_list
