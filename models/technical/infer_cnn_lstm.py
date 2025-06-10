import torch
from typing import Dict, Any
from .train_cnn_lstm import CNNLSTMModel

def load_model(model_path: str) -> CNNLSTMModel:
    model = CNNLSTMModel(input_size=10, hidden_size=64, num_layers=2)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def predict(model: CNNLSTMModel, X: torch.Tensor) -> Dict[str, Any]:
    with torch.no_grad():
        prediction = model(X)
    return {
        "prediction": prediction.item(),
        "confidence": 0.0  # Placeholder
    }

if __name__ == "__main__":
    # Dummy data
    X = torch.randn(1, 10, 50)
    model = load_model("model.pth")
    result = predict(model, X)
    print(result) 