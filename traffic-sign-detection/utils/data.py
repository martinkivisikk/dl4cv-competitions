import json
import os
import shutil


def convert_coco_to_yolo(ann_path, img_src_dir, yolo_base_dir):
    """Converts COCO json to YOLO txt format and moves images."""
    img_dst_dir = os.path.join(yolo_base_dir, "images", "train")
    lbl_dst_dir = os.path.join(yolo_base_dir, "labels", "train")
    os.makedirs(img_dst_dir, exist_ok=True)
    os.makedirs(lbl_dst_dir, exist_ok=True)

    with open(ann_path, "r") as f:
        data = json.load(f)

    # Class Mapping
    class_names = {c["id"]: c["name"] for c in data["categories"]}
    sorted_ids = sorted(class_names.keys())
    class_idx_map = {coco_id: i for i, coco_id in enumerate(sorted_ids)}

    img_dict = {img["id"]: img for img in data["images"]}

    for ann in data["annotations"]:
        img_info = img_dict[ann["image_id"]]
        w_orig, h_orig = img_info["width"], img_info["height"]
        filename = img_info["file_name"]

        # Copy Image
        shutil.copy(
            os.path.join(img_src_dir, filename), os.path.join(img_dst_dir, filename)
        )

        # Convert BBox (COCO [x,y,w,h] -> YOLO [xc, yc, w, h] normalized)
        x, y, w, h = ann["bbox"]
        x_center = (x + w / 2) / w_orig
        y_center = (y + h / 2) / h_orig
        w_norm, h_norm = w / w_orig, h / h_orig

        class_idx = class_idx_map[ann["category_id"]]

        txt_path = os.path.join(lbl_dst_dir, filename.replace(".jpg", ".txt"))
        with open(txt_path, "a") as f:
            f.write(f"{class_idx} {x_center} {y_center} {w_norm} {h_norm}\n")

    return {i: class_names[cid] for i, cid in enumerate(sorted_ids)}


def generate_yolo_yaml(output_path, yolo_dir, class_map):
    """Creates the data.yaml file for YOLO training."""
    names_str = "\n".join([f"  {k}: {v}" for k, v in sorted(class_map.items())])
    yaml_content = f"path: {yolo_dir}\ntrain: images/train\nval: images/train\nnc: {len(class_map)}\nnames:\n{names_str}"
    with open(output_path, "w") as f:
        f.write(yaml_content)
