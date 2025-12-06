from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_id = "Rytham1/bert-bias-detector"

# Load your fine-tuned model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(
    model_id
)
id2label = model.config.id2label

while True:
    text = input("Enter a sentence: ")
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=1).item()
    print(f"Prediction: {id2label[prediction]}")



