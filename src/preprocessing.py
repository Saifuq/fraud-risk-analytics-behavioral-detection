import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

class FinancialPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def fit_transform(self, df, target_col='fraud_status'):
        """
        Preprocesses the dataframe: cleans, encodes, and scales.
        """
        df_clean = df.copy()
        
        # Drop potential leakage columns or high-null columns
        if 'fraud_type' in df_clean.columns:
            df_clean = df_clean.drop(columns=['fraud_type'])
            
        # Handle missing values (simple strategy for now)
        df_clean = df_clean.dropna()

        # Convert boolean columns to integer
        bool_cols = df_clean.select_dtypes(include=['bool']).columns
        for col in bool_cols:
            df_clean[col] = df_clean[col].astype(int)
        
        # Identify categorical and numerical columns
        cat_cols = df_clean.select_dtypes(include=['object', 'category']).columns
        num_cols = df_clean.select_dtypes(include=['int64', 'float64']).columns
        
        # Remove target from numerical columns if present
        if target_col in num_cols:
            num_cols = num_cols.drop(target_col)
            
        # Encode categorical variables
        for col in cat_cols:
            le = LabelEncoder()
            df_clean[col] = le.fit_transform(df_clean[col].astype(str))
            self.label_encoders[col] = le
            
        # Scale numerical variables
        if len(num_cols) > 0:
            df_clean[num_cols] = self.scaler.fit_transform(df_clean[num_cols])
            
        return df_clean

    def preprocess_and_split(self, df, target_col='fraud_status', test_size=0.2, random_state=42):
        """
        Preprocesses the data and splits it into train and test sets.
        """
        df_processed = self.fit_transform(df, target_col)
        
        X = df_processed.drop(columns=[target_col])
        y = df_processed[target_col]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        
        return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Test with dummy data
    data = {
        'amount': [100.0, 200.0, 500.0, 20.0, 1000.0],
        'merchant': ['A', 'B', 'A', 'C', 'B'],
        'fraud_status': [0, 0, 1, 0, 1]
    }
    df = pd.DataFrame(data)
    preprocessor = FinancialPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.preprocess_and_split(df)
    print("Train shape:", X_train.shape)
    print("Test shape:", X_test.shape)
