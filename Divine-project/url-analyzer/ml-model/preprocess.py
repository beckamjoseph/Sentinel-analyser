import pandas as pd
from pathlib import Path
from feature_engineering import extract_features

BASE_DIR = Path(__file__).resolve().parents[1]

# Load cleaned dataset
df = pd.read_csv(BASE_DIR / "cleaned_urls.csv")

feature_rows = []

for index, row in df.iterrows():
    url = row['url']
    label = row['label']

    try:
        features = extract_features(url)
        features['label'] = label

        feature_rows.append(features)

    except Exception as e:
        print(f"Error processing URL: {url}")
        print(e)

# Create dataframe
processed_df = pd.DataFrame(feature_rows)

# Save processed features
processed_df.to_csv(BASE_DIR / "processed_data.csv", index=False)

print("\nFeature extraction complete!")
print(processed_df.head())
print(f"\nTotal processed rows: {len(processed_df)}")
