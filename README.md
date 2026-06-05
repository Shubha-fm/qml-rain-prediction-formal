# Quantum Machine Learning Rain Prediction with Formal Verification

This repository demonstrates a research-style project for predicting rain using a hybrid quantum-classical machine learning model and validating the decision logic using formal methods.

The project contains:

- A synthetic weather dataset generator
- A hybrid Quantum Machine Learning model using PennyLane and PyTorch
- Classical preprocessing and evaluation pipeline
- Professional plots and graphs for research presentation
- TLA+ formal specification for rain-warning decision safety
- A static GitHub Pages website for browser-based rain prediction

## Project Structure

```text
qml-rain-prediction-formal/
├── src/
│   ├── generate_weather_data.py
│   ├── qml_model.py
│   ├── train_qml_rain.py
│   ├── evaluate.py
│   └── generate_demo_outputs.py
├── formal/
│   └── formal_verification_notes.md
├── tla/
│   ├── RainPrediction.tla
│   └── RainPrediction.cfg
├── web/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── outputs/
│   ├── architecture.png
│   ├── dataset_distribution.png
│   ├── training_curves.png
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   └── formal_verification_summary.png
├── requirements.txt
├── LICENSE
└── README.md
```

## Research Idea

The system predicts whether rain is likely using weather attributes such as temperature, humidity, pressure, wind speed, cloud cover, and previous rainfall. A hybrid QML model embeds normalized weather features into a parameterized quantum circuit. The quantum output is passed to a classical layer for binary prediction.

The prediction layer is connected with a formal decision policy. The policy ensures that unsafe warnings are not silently ignored. For example, if the predicted rain probability is high and the humidity is above a threshold, the system must issue a rain warning.

## Install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Run the Full Pipeline

```bash
python src/generate_weather_data.py
python src/train_qml_rain.py
python src/evaluate.py
```

## Generate Demo Graphs Without Training

This command creates sample plots inside the `outputs/` folder. It is useful for GitHub preview and academic demonstration.

```bash
python src/generate_demo_outputs.py
```

## Run the Website Locally

Open the website folder:

```bash
cd web
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Deploy Website on GitHub Pages

1. Upload this project to GitHub.
2. Go to repository **Settings**.
3. Open **Pages**.
4. Under **Build and deployment**, choose:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/web`
5. Save.
6. Your website will be available at:

```text
https://YOUR_USERNAME.github.io/REPOSITORY_NAME/
```

## Formal Verification

The TLA+ model is placed in the `tla/` folder. It specifies the rain prediction decision states and verifies safety properties such as:

- high-risk weather should not remain in `NoWarning`
- warning state must be reachable
- decision state must remain within the allowed set
- every accepted prediction must lead to a valid action

To check the model with TLC:

```bash
tlc tla/RainPrediction.tla -config tla/RainPrediction.cfg
```

## Suggested GitHub Repository Description

```text
Quantum machine learning rain prediction system with TLA+ formal verification and a GitHub Pages prediction website.
```

## License

MIT License.
