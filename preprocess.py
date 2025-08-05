# preprocess.py
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\\s₹$€£]', '', text)
    text = re.sub(r'\\s+', ' ', text).strip()
    words = word_tokenize(text)
    cleaned_words = [word for word in words if word not in stop_words]
    return ' '.join(cleaned_words)

def merge_and_clean(train_path, test_path, val_path, output_path):
    print("🔄 Merging CSV files...")
    df1 = pd.read_csv(train_path)
    df2 = pd.read_csv(test_path)
    df3 = pd.read_csv(val_path)
    df = pd.concat([df1, df2, df3])

    print("🧹 Cleaning text data...")
    df['article'] = df['article'].fillna('').apply(clean_text)
    df['highlights'] = df['highlights'].fillna('').apply(clean_text)

    before = len(df)
    df.drop_duplicates(subset=['article', 'highlights'], inplace=True)
    after = len(df)
    print(f"✅ Removed {before - after} duplicate rows.")

    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to: {output_path}")

if __name__ == "__main__":
    merge_and_clean(
        train_path="data/train.csv",
        test_path="data/test.csv",
        val_path="data/validation.csv",
        output_path="data/merged_cleaned.csv"
    )
