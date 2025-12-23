from datasets import load_dataset
import pandas as pd

def inspect_data():
    print("Streaming first 10,000 rows...")
    dataset = load_dataset("electricsheepafrica/Nigerian-Financial-Transactions-and-Fraud-Detection-Dataset", split="train", streaming=True)
    data_head = dataset.take(10000)
    df = pd.DataFrame(list(data_head))
    
    print("Columns:", df.columns)
    if 'is_fraud' in df.columns:
        print("is_fraud unique values:", df['is_fraud'].unique())
        print("is_fraud value counts:\n", df['is_fraud'].astype(int).value_counts())
    
    if 'fraud_type' in df.columns:
        print("fraud_type distinct values:", df['fraud_type'].unique())

if __name__ == "__main__":
    inspect_data()
