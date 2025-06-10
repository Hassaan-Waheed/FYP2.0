from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, Any, List

def load_model(model_path: str) -> AutoModelForSequenceClassification:
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    return model

def predict(model: AutoModelForSequenceClassification, texts: List[str]) -> Dict[str, Any]:
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    return {
        "predictions": outputs.logits.softmax(dim=1).tolist(),
        "sentiment": "positive"  # Placeholder
    }

if __name__ == "__main__":
    texts = ["Bitcoin is going up!", "Market looks bearish"]
    model = load_model("finbert_model")
    result = predict(model, texts)
    print(result) 