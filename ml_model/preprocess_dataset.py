import pandas as pd
from url_features import extract_url_features
import os

def preprocess_url_dataset(input_csv, output_csv):
    """Convert raw URL dataset to feature dataset"""
    print(f"Loading dataset from {input_csv}...")
    df = pd.read_csv(input_csv)
    
    print(f"Found {len(df)} URLs")
    print(f"Label distribution:\n{df['Label'].value_counts()}")
    
    # Extract features for each URL
    print("\nExtracting features...")
    features_list = []
    for idx, row in df.iterrows():
        url = row['URL']
        features = extract_url_features(url)
        features_list.append(features)
        
        if (idx + 1) % 1000 == 0:
            print(f"Processed {idx + 1}/{len(df)} URLs...")
    
    # Create features dataframe
    features_df = pd.DataFrame(features_list)
    
    # Add label column (convert 'bad' to 1, 'good' to 0)
    features_df['phishing'] = df['Label'].apply(lambda x: 1 if x == 'bad' else 0)
    
    # Save to CSV
    features_df.to_csv(output_csv, index=False)
    print(f"\nFeature dataset saved to {output_csv}")
    print(f"Shape: {features_df.shape}")
    print(f"\nFirst few rows:")
    print(features_df.head())
    
    return features_df

if __name__ == "__main__":
    input_file = 'datasets/phishing_site_urls.csv'
    output_file = 'datasets/web-page-phishing-processed.csv'
    
    preprocess_url_dataset(input_file, output_file)