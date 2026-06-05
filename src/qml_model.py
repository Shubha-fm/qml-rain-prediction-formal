"""Hybrid quantum-classical rain prediction model."""

from __future__ import annotations

import torch
import torch.nn as nn
import pennylane as qml


class QuantumRainClassifier(nn.Module):
    """A compact hybrid QML classifier.

    The model maps six weather features to four qubits through a small classical
    encoder. A variational quantum circuit produces expectation values, and a
    classical head converts them into a binary rain prediction.
    """

    def __init__(self, n_features: int = 6, n_qubits: int = 4, n_layers: int = 3):
        super().__init__()
        self.n_qubits = n_qubits
        self.encoder = nn.Sequential(
            nn.Linear(n_features, 8),
            nn.ReLU(),
            nn.Linear(8, n_qubits),
        )

        dev = qml.device("default.qubit", wires=n_qubits)

        @qml.qnode(dev, interface="torch")
        def circuit(inputs, weights):
            for i in range(n_qubits):
                qml.RY(inputs[i], wires=i)
                qml.RZ(inputs[i], wires=i)

            qml.StronglyEntanglingLayers(weights, wires=range(n_qubits))
            return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

        weight_shapes = {"weights": (n_layers, n_qubits, 3)}
        self.quantum_layer = qml.qnn.TorchLayer(circuit, weight_shapes)
        self.classifier = nn.Sequential(
            nn.Linear(n_qubits, 4),
            nn.ReLU(),
            nn.Linear(4, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        encoded = self.encoder(x)
        encoded = torch.tanh(encoded) * torch.pi
        quantum_features = self.quantum_layer(encoded)
        return self.classifier(quantum_features).squeeze(-1)
