"""Evaluate the rain prediction model and create publication-style plots."""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay, accuracy_score, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from qml_model import QuantumRainClassifier
from generate_weather_data import generate_dataset

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
FEATURES = ["temperature", "humidity", "pressure", "wind_speed", "cloud_cover", "previous_rainfall"]


def main() -> None:
    data_path = DATA_DIR / "weather_data.csv"
    if not data_path.exists():
        generate_dataset().to_csv(data_path, index=False)

    df = pd.read_csv(data_path)
    x = df[FEATURES].values
    y = df["rain"].values
    x_train, x_test, _, y_test = train_test_split(x, y, test_size=0.25, random_state=42, stratify=y)

    scaler = StandardScaler()
    scaler.fit(x_train)
    x_test = scaler.transform(x_test)

    model = QuantumRainClassifier()
    model.load_state_dict(torch.load(OUTPUT_DIR / "qml_rain_model.pt", map_location="cpu"))
    model.eval()

    with torch.no_grad():
        probs = torch.sigmoid(model(torch.tensor(x_test, dtype=torch.float32))).numpy()

    preds = (probs >= 0.5).astype(int)
    acc = accuracy_score(y_test, preds)
    auc = roc_auc_score(y_test, probs)
    print(f"Accuracy: {acc:.3f}")
    print(f"ROC-AUC: {auc:.3f}")

    cm = confusion_matrix(y_test, preds)
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay(cm, display_labels=["No Rain", "Rain"]).plot(ax=ax, values_format="d")
    ax.set_title("Confusion Matrix: QML Rain Prediction")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=300)

    fig, ax = plt.subplots(figsize=(6, 5))
    RocCurveDisplay.from_predictions(y_test, probs, ax=ax)
    ax.set_title("ROC Curve: QML Rain Prediction")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "roc_curve.png", dpi=300)


if __name__ == "__main__":
    main()
