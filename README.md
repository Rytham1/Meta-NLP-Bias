# META NLP PROJECT

## Exploring Bias Detection in Reddit Comments with NLP

This project was developed in collaboration with Meta researchers as part of the Breakthrough Tech Fellowship. 

Our goal is to study and detect bias in Reddit comments across multiple dimensions (gender, race, religion, and orientation) using NLP techniques and then finetuning the BERT model to detect the bias.

### Dataset:
We used the RedditBias dataset, this contains annoted reddit comments with a bias (binary) column. We split the dataset into training, validation, and test sets.

### Setup

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Model Weights**: The model weights (`model.safetensors`, ~418MB) are not stored in this repository due to GitHub's file size limits. To use the model:
   - Contact a team member to obtain the `model.safetensors` file
   - Place it in `backend/saved_model/` directory
   - The config and tokenizer files are already included in the repo

3. Test the model:
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
- ADD STUFF HERE

### Results:
- Dataset went from ~28,000 datapoints to ~11,000 datapoints after cleaning/filtering
- ADD STUFF HERE 

This Project was developed by:
- Rytham Dawar - Rythamdawar30@gmail.com
- Leonardo Siu - leonardo.siu.dev@gmail.com
- Rianna Lei - rxlei@calpoly.edu
- Wen Fan - wqfan05@gmail.com
- Mia Carter - Mia.L.Carter04@gmail.com
- Jay Chan - jayc10@uci.edu
- Hala Khattab - hala.khattaab@gmail.com

Mentors:
- Rajshri Jain (Break Through Tech)
- Candace Ross (META - Research Scientist)
- Megan Ung (META - Research Engineer)
