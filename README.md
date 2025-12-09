# Break Through Tech AI Studio: Meta 1B

## 🌐 Live Demo
Access the interactive NLP Bias Detection application here:
[https://nlp-bias-detection.vercel.app/](https://nlp-bias-detection.vercel.app/)

## Finding Dataset Bias using Language Models

This project was developed in collaboration with Meta researchers Megan Ung and Candace Ross as part of the Break Through Tech Fellowship. 

Our model was trained by detecting bias in Reddit comments across multiple groups (gender, race, religion, and orientation) using NLP techniques and then fine-tuning on the BERT model. 

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


### Setup

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



### Finetuning
- We utilized weights and biases to track our 20+ fine tuning runs.
- Originally, our model was overfitting so we applied different techniques which included applying regularization through weight decay and early dropout, adjusting learning rate, batch size, and epochs.
- The solution to our issue was modifying the learning rate and learning rate scheduler type to linear rather than a constant one.
- Additionally, we ran into a very high validation loss in which we continued hyperparameter tuning with a focus on learning rate and batch size.

### Results:
- Dataset went from ~28,000 datapoints to ~11,000 datapoints after cleaning/filtering
- ~0.45 validation loss & ~0.4 training loss
- Baseline Logistic Regression Model of 0.74 F1 -> 0.83 F1 (12.16% relative increase)

### Mentors:
- Rajshri Jain (Break Through Tech)
- Candace Ross (META - Research Scientist)
- Megan Ung (META - Research Engineer)
