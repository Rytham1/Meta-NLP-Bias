from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

app = FastAPI(title="Bias Detection API", description="API for detecting bias in text")

# Load model and tokenizer
model_repo = "Rytham1/bert-bias-detector"

tokenizer = AutoTokenizer.from_pretrained(model_repo)
model = AutoModelForSequenceClassification.from_pretrained(model_repo)
model.eval()

class InputText(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Bias Detection API is running"}

@app.post("/predict")
def predict_bias(input_data: InputText):
    """
    Predict if the input text is biased or not.

    @param input_data: InputText object containing the text to analyze
    @return Dictionary with prediction label and confidence scores
    """
    try:
        # Tokenize input text
        encoded = tokenizer(
            input_data.text,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=128
        )

        # Get prediction
        with torch.no_grad():
            outputs = model(**encoded)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            pred = torch.argmax(logits, dim=1).item()
            confidence = probabilities[0][pred].item()

        # Map prediction to label (0: non_biased, 1: biased)
        label = "biased" if pred == 1 else "non_biased"

        return {
            "prediction": label,
            "confidence": round(confidence, 4),
            "probabilities": {
                "non_biased": round(probabilities[0][0].item(), 4),
                "biased": round(probabilities[0][1].item(), 4)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}") from e
