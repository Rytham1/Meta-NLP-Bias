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
