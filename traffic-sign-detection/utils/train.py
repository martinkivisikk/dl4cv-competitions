from ultralytics import YOLO


def train_yolo_model(model_variant, data_yaml, experiment_name, **kwargs):
    """
    Initializes and trains a YOLO model with specified parameters.

    Args:
        model_variant (str): Path to model weights (e.g., 'yolov8n.pt').
        data_yaml (str): Path to the data configuration file.
        experiment_name (str): Name for the training run.
        **kwargs: Additional hyperparameters (imgsz, epochs, batch, etc.)
    """
    print(f"🚀 Starting training for: {experiment_name} using {model_variant}")

    # Load model
    model = YOLO(model_variant)

    # Train
    results = model.train(data=data_yaml, name=experiment_name, **kwargs)

    print(f"Training for {experiment_name} complete.\n")
    return results
