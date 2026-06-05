"""Train the QML rain prediction model and save training curves."""

from pathlib import Path
import json

import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset

from qml_model import QuantumRainClassifier
from generate_weather_data import generate_dataset

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

FEATURES = [
    "temperature",
    "humidity",
    "pressure",
    "wind_speed",
    "cloud_cover",
    "previous_rainfall",
]


def load_or_create_data() -> pd.DataFrame:
    data_path = DATA_DIR / "weather_data.csv"
    if not data_path.exists():
        generate_dataset().to_csv(data_path, index=False)
    return pd.read_csv(data_path)


def main() -> None:
    torch.manual_seed(42)
    df = load_or_create_data()

    x = df[FEATURES].values
    y = df["rain"].values

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    train_ds = TensorDataset(
        torch.tensor(x_train, dtype=torch.float32),
        torch.tensor(y_train, dtype=torch.float32),
    )
    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)

    model = QuantumRainClassifier()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.BCEWithLogitsLoss()

    history = {"loss": [], "accuracy": []}

    for epoch in range(20):
        model.train()
        losses = []
        all_pred, all_true = [], []

        for xb, yb in train_loader:
            optimizer.zero_grad()
            logits = model(xb)
            loss = criterion(logits, yb)
            loss.backward()
            optimizer.step()

            losses.append(loss.item())
            pred = (torch.sigmoid(logits).detach().numpy() >= 0.5).astype(int)
            all_pred.extend(pred.tolist())
            all_true.extend(yb.numpy().astype(int).tolist())

        acc = accuracy_score(all_true, all_pred)
        history["loss"].append(float(sum(losses) / len(losses)))
        history["accuracy"].append(float(acc))
        print(f"Epoch {epoch + 1:02d}: loss={history['loss'][-1]:.4f}, acc={acc:.4f}")

    model_path = OUTPUT_DIR / "qml_rain_model.pt"
    torch.save(model.state_dict(), model_path)

    with open(OUTPUT_DIR / "training_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    model.eval()
    with torch.no_grad():
        logits = model(torch.tensor(x_test, dtype=torch.float32))
        probs = torch.sigmoid(logits).numpy()
        preds = (probs >= 0.5).astype(int)

    metrics = {
        "test_accuracy": float(accuracy_score(y_test, preds)),
        "test_f1": float(f1_score(y_test, preds)),
    }
    with open(OUTPUT_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    plt.figure(figsize=(8, 5))
    plt.plot(history["loss"], marker="o", label="Training loss")
    plt.plot(history["accuracy"], marker="s", label="Training accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Value")
    plt.title("QML Rain Prediction Training Curve")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "training_curves.png", dpi=300)
    print(f"Saved model and plots to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
