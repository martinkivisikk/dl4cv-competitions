import cv2
import random
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path


def visualize_predictions(
    results_list, img_dir, class_names, num_images=8, conf_threshold=0.25
):
    """Plots predictions on a grid of images."""
    valid = [
        r
        for r in results_list
        if not r["PredictionString"].startswith("No_parking 0.0001")
    ]
    sample = random.sample(valid, min(num_images, len(valid)))

    cols = 4
    rows = -(-len(sample) // cols)
    fig, axes = plt.subplots(rows, cols, figsize=(16, 4 * rows))
    axes = axes.flatten() if rows * cols > 1 else [axes]

    for ax, record in zip(axes, sample):
        img_path = Path(img_dir) / f"{record['image_id']}.jpg"
        if not img_path.exists():
            continue

        img = cv2.cvtColor(cv2.imread(str(img_path)), cv2.COLOR_BGR2RGB)
        ax.imshow(img)
        ax.set_title(record["image_id"], fontsize=8)
        ax.axis("off")

        # Regex to parse the prediction string
        pattern = (
            r"([A-Za-z0-9_]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)"
        )
        predictions = re.findall(pattern, record["PredictionString"])

        for label, conf, x1, y1, x2, y2 in predictions:
            if float(conf) < conf_threshold:
                continue

            # Draw box
            rect = patches.Rectangle(
                (float(x1), float(y1)),
                float(x2) - float(x1),
                float(y2) - float(y1),
                linewidth=2,
                edgecolor="red",
                facecolor="none",
            )
            ax.add_patch(rect)
            ax.text(
                float(x1),
                float(y1),
                f"{label} {float(conf):.2f}",
                color="white",
                bbox=dict(facecolor="red", alpha=0.5),
            )

    plt.tight_layout()
    plt.show()
