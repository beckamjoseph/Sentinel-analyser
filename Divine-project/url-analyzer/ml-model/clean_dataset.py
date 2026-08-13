import pandas as pd

# Load dataset
df = pd.read_csv("./dataset/malicious_phish.csv")

# Keep only required columns
df = df[['url', 'type']]

# ``defacement`` in this source is a historical page state, not evidence that
# every URL on that host is presently unsafe.  Including it as a positive
# training label was the main source of normal-looking false positives.
# The production classifier therefore focuses on phishing and malware URLs.
df = df[df['type'].isin(['benign', 'phishing', 'malware'])].copy()

# Convert labels
label_mapping = {
    'benign': 0,
    'phishing': 1,
    'malware': 1,
}

df['label'] = df['type'].map(label_mapping)

# Remove rows with missing labels
df = df.dropna()

# Remove duplicates
df = df.drop_duplicates()

# Keep only url + label
df = df[['url', 'label']]

# Save cleaned dataset
df.to_csv("cleaned_urls.csv", index=False)


print(df.head())
print("\nDataset cleaned successfully!")
print(f"Total rows: {len(df)}")


