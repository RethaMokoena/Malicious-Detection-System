import pandas as pd

# Load both CSV files
df1 = pd.read_csv('datasets/web-page-phishing-processed.csv')
df2 = pd.read_csv('datasets/web-page-phishing.csv')

# Concatenate them vertically
combined_df = pd.concat([df1, df2], ignore_index=True)

# Save to new CSV
combined_df.to_csv('dataset.csv', index=False)

print(f"Combined {len(df1)} + {len(df2)} = {len(combined_df)} rows")