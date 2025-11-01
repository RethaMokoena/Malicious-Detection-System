# In your terminal, run Python and check:
import pandas as pd
df = pd.read_csv('ml_model/datasets/web-page-phishing.csv')
print(df['phishing'].value_counts())
print(df.describe())