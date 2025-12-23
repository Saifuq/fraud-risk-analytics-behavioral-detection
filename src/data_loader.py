import pandas as pd
from datasets import load_dataset
import os
import numpy as np

# Fix for Windows symlink warning/error
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

def generate_synthetic_data(rows=1000):
    """Generates synthetic data for testing."""
    print("Generating synthetic data...")
    data = {
        'step': np.random.randint(1, 100, rows),
        'type': np.random.choice(['PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT', 'CASH_IN'], rows),
        'amount': np.random.uniform(10, 100000, rows),
        'nameOrig': [f'C{i}' for i in range(rows)],
        'oldbalanceOrg': np.random.uniform(0, 100000, rows),
        'newbalanceOrig': np.random.uniform(0, 100000, rows),
        'nameDest': [f'M{i}' for i in range(rows)],
        'oldbalanceDest': np.random.uniform(0, 100000, rows),
        'newbalanceDest': np.random.uniform(0, 100000, rows),
        'isFraud': np.random.choice([0, 1], rows, p=[0.95, 0.05]),
        'isFlaggedFraud': [0] * rows
    }
    return pd.DataFrame(data)

def load_financial_data(limit=None, use_synthetic=False):
    """
    Loads the Nigerian Financial Transactions and Fraud Detection Dataset.
    Args:
        limit (int, optional): If set, only load this many rows using streaming. 
                               Defaults to 10,000 to avoid crash on Windows.
        use_synthetic (bool): If True, use generated data.
    """
    if limit is None:
        limit = 50000 # Safety default for Windows

    if use_synthetic:
        return generate_synthetic_data(rows=limit if limit else 1000)

    print("Loading dataset...")
    try:
        if limit:
            print(f"Streaming mode enabled: Loading first {limit} rows...")
            dataset = load_dataset("electricsheepafrica/Nigerian-Financial-Transactions-and-Fraud-Detection-Dataset", split="train", streaming=True)
            # Take first 'limit' rows
            data_head = dataset.take(limit)
            df = pd.DataFrame(list(data_head))
        else:
            # Full load (downloads files)
            dataset = load_dataset("electricsheepafrica/Nigerian-Financial-Transactions-and-Fraud-Detection-Dataset")
            if 'train' in dataset:
                df = dataset['train'].to_pandas()
            else:
                df = dataset[list(dataset.keys())[0]].to_pandas()
            
        print(f"Dataset loaded successfully with shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

if __name__ == "__main__":
    df = load_financial_data()
    if df is not None:
        print(df.head())
        # Save a sample for quick inspection
        df.head(100).to_csv("data_sample.csv", index=False)
