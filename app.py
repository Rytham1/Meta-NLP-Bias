"""
Hugging Face Spaces deployment for Meta NLP Bias Detection
Includes both Gradio UI AND FastAPI for custom frontend
"""
import gradio as gr
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Initialize FastAPI for your custom frontend
app = FastAPI(title="Bias Detection API")

# Add CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and tokenizer
model_repo = "Rytham1/bert-bias-detector"
tokenizer = AutoTokenizer.from_pretrained(model_repo)
model = AutoModelForSequenceClassification.from_pretrained(model_repo)
model.eval()

# Request model for FastAPI
class InputText(BaseModel):
    text: str

# FastAPI endpoint for your custom frontend
@app.get("/")
def root():
    return {"message": "Bias Detection API is running", "status": "healthy"}

@app.post("/predict")
def predict_bias_api(input_data: InputText):
    """
    FastAPI endpoint for your custom frontend
    """
    try:
        encoded = tokenizer(
            input_data.text,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=128
        )

        with torch.no_grad():
            outputs = model(**encoded)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            pred = torch.argmax(logits, dim=1).item()
            confidence = probabilities[0][pred].item()

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
        return {"error": str(e)}, 500

def predict_bias(text):
    """
    Predict if the input text is biased or not.
    """
    if not text.strip():
        return "Please enter some text to analyze.", None, None
    
    try:
        # Tokenize input text
        encoded = tokenizer(
            text,
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

        # Map prediction to label
        label = "⚠️ BIASED" if pred == 1 else "✅ NOT BIASED"
        
        # Create probability dictionary for display
        prob_dict = {
            "Not Biased": float(probabilities[0][0].item()),
            "Biased": float(probabilities[0][1].item())
        }
        
        return label, confidence, prob_dict
        
    except Exception as e:
        return f"Error: {str(e)}", None, None

# Create Gradio interface
with gr.Blocks(title="AI Bias Detection Tool") as demo:
    gr.Markdown("""
    # 🤖 AI Bias Detection Tool
    ### Identifying dataset bias using fine-tuned language models
    
    This tool was developed as part of the **Meta Breakthrough Tech Fellowship** to detect bias 
    in text across multiple dimensions (gender, race, religion, and orientation).
    
    **Try examples like:**
    - "Women are better at nursing than men"
    - "Doctors are usually men"
    - "All teenagers are irresponsible"
    """)
    
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(
                label="Enter text to analyze",
                placeholder="Type or paste text here...",
                lines=5
            )
            with gr.Row():
                analyze_btn = gr.Button("🔍 Analyze Text", variant="primary", size="lg")
                clear_btn = gr.ClearButton([input_text], value="Clear")
        
        with gr.Column():
            result_label = gr.Textbox(label="Prediction", interactive=False)
            confidence = gr.Number(label="Confidence Score", interactive=False)
            probabilities = gr.Label(label="Probabilities", num_top_classes=2)
    
    # Examples
    gr.Examples(
        examples=[
            ["Women are better at nursing than men"],
            ["Doctors are usually men"],
            ["All teenagers are irresponsible"],
            ["This is a neutral statement about the weather"],
            ["People from that country are lazy"],
        ],
        inputs=input_text,
        label="Try these examples"
    )
    
    # Connect button to function
    analyze_btn.click(
        fn=predict_bias,
        inputs=input_text,
        outputs=[result_label, confidence, probabilities]
    )
    
    gr.Markdown("""
    ---
    ### 📊 About This Project
    
    **Developed by:**
    - Rytham Dawar, Leonardo Siu, Rianna Lei, Wen Fan, Mia Carter, Jay Chan, Hala Khattab
    
    **Mentors:**
    - Rajshri Jain (Break Through Tech)
    - Candace Ross (META - Research Scientist)
    - Megan Ung (META - Research Engineer)
    
    **Model:** Fine-tuned BERT on RedditBias dataset
    """)

# Mount Gradio app to FastAPI
app = gr.mount_gradio_app(app, demo, path="/gradio")

# Launch the app
if __name__ == "__main__":
    demo.launch()

