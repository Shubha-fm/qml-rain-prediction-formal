"""Generate a synthetic weather dataset for rain prediction.

The dataset is intended for reproducible academic demonstration. It is not a
substitute for a real meteorological dataset.
"""

from pathlib import Path
import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)


def generate_dataset(n_samples: int = 1200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    temperature = rng.normal(27, 5, n_samples).clip(10, 42)
    humidity = rng.normal(70, 15, n_samples).clip(25, 100)
    pressure = rng.normal(1008, 8, n_samples).clip(980, 1035)
    wind_speed = rng.gamma(2.0, 3.0, n_samples).clip(0, 35)
    cloud_cover = rng.normal(60, 25, n_samples).clip(0, 100)
    previous_rainfall = rng.exponential(3.0, n_samples).clip(0, 45)

    score = (
        0.040 * humidity
        + 0.035 * cloud_cover
        + 0.075 * previous_rainfall
        + 0.025 * wind_speed
        - 0.030 * temperature
        - 0.022 * (pressure - 1000)
        + rng.normal(0, 1.2, n_samples)
    )

    probability = 1 / (1 + np.exp(-(score - 3.6)))
    rain = (probability > 0.50).astype(int)

    return pd.DataFrame(
        {
            "temperature": temperature.round(2),
            "humidity": humidity.round(2),
            "pressure": pressure.round(2),
            "wind_speed": wind_speed.round(2),
            "cloud_cover": cloud_cover.round(2),
            "previous_rainfall": previous_rainfall.round(2),
            "rain": rain,
        }
    )


if __name__ == "__main__":
    df = generate_dataset()
    output_path = DATA_DIR / "weather_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")
    print(df.head())
