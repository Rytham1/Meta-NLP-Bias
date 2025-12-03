# from fastapi import FastAPI
# from pydantic import BaseModel
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch

# app = FastAPI()

# model_path = "saved_model/"
# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForSequenceClassification.from_pretrained(model_path)
# model.eval()

# class InputText(BaseModel):
#     text: str

# @app.post("/predict")
# def predict_sentiment(input_data: InputText):
#     encoded = tokenizer(
#         input_data.text,
#         return_tensors="pt",
#         truncation=True,
#         padding="max_length",
#         max_length=128
#     )

#     with torch.no_grad():
#         outputs = model(**encoded)
#         logits = outputs.logits
#         pred = torch.argmax(logits, dim=1).item()

#     label = "biased" if pred == 1 else "non-biased"
#     return {"prediction": label}
