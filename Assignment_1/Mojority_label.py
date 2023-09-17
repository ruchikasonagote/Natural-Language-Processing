#majority label from all three models

import os
import pandas as pd

folder_path = "//content//sample_data//major"

def comparison(row):
    if row['Semantic Label 1'] == row['Semantic Label 2']:
        return row['Semantic Label 1']
    elif row['Semantic Label 1'] == row['Semantic Label 3']:
        return row['Semantic Label 1']
    elif row['Semantic Label 2'] == row['Semantic Label 3']:
        return row['Semantic Label 2']
    else:
        return 'neutral'

i = 1
for filename in os.listdir(folder_path):

    if filename.endswith(".csv"):
        output_file = f"output{i}.csv"

        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        df['Major_Semantic'] = df.apply(comparison, axis=1)

        df.to_csv(output_file, index=False)
        print(f"Processed {filename}")
        i += 1

print("Done !!")

