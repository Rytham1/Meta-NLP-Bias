# Break Through Tech AI Studio: Meta 1B

## Finding Dataset Bias using Language Models

This project was developed in collaboration with Meta researchers Megan Ung and Candace Ross as part of the Break Through Tech fellowship. 

Our model was trained by detecting bias in Reddit comments across multiple groups (gender, race, religion, and orientation) using NLP techniques and then fine-tuning on the BERT model. 

## 🌐 Live Demo
Access the interactive NLP Bias Detection application here:
[https://nlp-bias-detection.vercel.app/](https://nlp-bias-detection.vercel.app/)

---

### 👥 **Team Members**

| Name             | GitHub Handle | Email                                                             |
|------------------|---------------|--------------------------------------------------------------------------|
| Rytham Dawar    | @Rytham1 | Rythamdawar30@gmail.com            |
| Leonardo Siu   | @baller7215     | leonardo.siu.dev@gmail.com  |
| Rianna Lei     | @riannalei  | rxlei@calpoly.edu                 |
| Wen Fan      | @Wen-qqi       | wqfan05@gmail.com  |
| Jay Chan       | @jayc-10    | jayc10@uci.edu           |
| Hala Khattab       | @halakhattab    | hala.khattaab@gmail.com           |

---

## 🎯 **Project Highlights**
- Prepared and standardized the RedditBias dataset, creating robust train/validation/test splits to support reliable model evaluation.
- Fine-tuned a base language model on the RedditBias dataset, optimizing performance through iterative training and validation on Wandb.
- Conducted final model evaluation, documented findings, and deployed results on full-stack website.

## 👩🏽‍💻 **Setup and Installation**

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Test the model:
   ```bash
   python test_model.py
   ```

### Running the Backend Server

The backend provides a REST API for bias detection inference using FastAPI.

1. **Start the server:**
   ```bash
   cd backend
   uvicorn backend:app --reload
   ```
   The `--reload` flag enables auto-reload on code changes.

2. **Access the API:**
   - API will be available at: `http://127.0.0.1:8000`
   - Interactive API documentation (Swagger UI): `http://127.0.0.1:8000/docs`

3. **API Endpoints:**
   - `GET /` - Health check endpoint
   - `POST /predict` - Bias detection endpoint
     - **Request body:**
       ```json
       {
         "text": "Your text to analyze here"
       }
       ```
     - **Response:**
       ```json
       {
         "prediction": "biased" | "non_biased",
         "confidence": 0.xxxx,
         "probabilities": {
           "non_biased": 0.xxxx,
           "biased": 0.xxxx
         }
       }
       ```

4. **Example usage with curl:**
   ```bash
   curl -X POST "http://127.0.0.1:8000/predict" \
        -H "Content-Type: application/json" \
        -d '{"text": "Your text here"}'
   ```

5. **Example usage with Python:**
   ```python
   import requests
   
   response = requests.post(
       "http://127.0.0.1:8000/predict",
       json={"text": "Your text to analyze"}
   )
   print(response.json())
   ```

## 🏗️ **Project Overview**
As Large Language Models (LLMs) become increasingly embedded in real-world applications, concerns around bias and fairness have grown. The models directly learn from large-scale text data which often includes historical, social, and demographic bias. When unleft, the biases can propagate stereotypes and lead to discriminatory outcomes. This project focuses on detecting and evaluating demographic bias in text before it is used. Our work highlights the challenges of bias in NLP systems and practical steps towards building more responsible and interpretable AI tools.

## 📊 **Data Exploration**
- RedditBias Dataset: 28,000 Data Points
  - Categorized into: Gender, Race, Orientation, Religion
- Consolidated data into binary labels (0 = Not Biased, 1 = Biased)
- Removed duplicates and handled missing values
- Standardized and normalized all text (lowercased everything, removed URLS and special characters), and handled contradictions and whitespace
- Marked trigger words and created word count feature

## 🧠 **Model Development**
- We utilized weights and biases to track our 20+ fine tuning runs.
- Originally, our model was overfitting so we applied different techniques which included applying regularization through weight decay and early dropout, adjusting learning rate, batch size, and epochs.
- The solution to our issue was modifying the learning rate and learning rate scheduler type to linear rather than a constant one.
- Additionally, we ran into a very high validation loss in which we continued hyperparameter tuning with a focus on learning rate and batch size.

## 📈 **Results & Key Findings**
- Built a baseline Logistic Regression model for a supervised learning task, using data cleaning and filtering that reduced the dataset from ~28,000 to ~11,000 high-quality datapoints.
- Achieved strong performance with ~0.40 training loss and ~0.45 validation loss, indicating good generalization.
- Improved model effectiveness from 0.74 to 0.83 F1 score (12.16% relative increase), demonstrating feature engineering and establishing a solid foundation for future development.

## 🚀 **Next Steps**
- Continue hyperparameter tuning
  - Further refine our model to reduce validation loss
- Expand dataset source
  - Sample a wider range of data beyond the RedditBias dataset
  - Test the fine-tuned model on other datasets
- Experiment with other models for comparison
  - RoBERTa, DistilBERT, DeBERTa

## 🙏 **Acknowledgements**
- Rajshri Jain (Break Through Tech)
- Candace Ross (Research Scientist @ Meta)
- Megan Ung (Research Engineer @ Meta)
