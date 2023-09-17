# Labels according to model 3 -->  Seethal/sentiment_analysis_generic_dataset
!pip install -q transformers
# Use a pipeline as a high-level helper
import pandas as pd
import os

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load model directly
tokenizer = AutoTokenizer.from_pretrained("Seethal/sentiment_analysis_generic_dataset")
model = AutoModelForSequenceClassification.from_pretrained("Seethal/sentiment_analysis_generic_dataset")

import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))

id_to_sentiment = {
    0: "negative",
    1: "neutral",
    2: "positive"
}

i=0

folder_path = "//content//sample_data"

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        file_df = pd.read_csv(file_path)
        file_comments = file_df["Comment Text"].tolist()

        # List to store sentiment labels for this file
        file_sentiments = []

        for comment in file_comments:
            inputs = tokenizer(comment, return_tensors="pt", padding="max_length", truncation=True, max_length=128)
            with torch.no_grad():
                outputs = model(**inputs)
                predicted_class = torch.argmax(outputs.logits, dim=1)

            sentiment_label = id_to_sentiment[predicted_class.item()]
            file_sentiments.append(sentiment_label)

        # Add a new column with semantic labels to the file DataFrame
        file_df["Semantic Label 3"] = file_sentiments

        # Save the updated file DataFrame
        folder_path_new = '//content//sample_data'

        updated_file_path = os.path.join(folder_path_new, "Model_3" + filename)
        # updated_file_path='/content/Model1_updated'
        file_df.to_csv(updated_file_path, index=False)
        i+=1
        print(f"Semantic labels added to {filename}")
        print(i)
        os.remove(file_path)

print("Semantic labels added to all files in the folder.")
