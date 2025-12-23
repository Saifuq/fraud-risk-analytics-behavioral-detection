import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import classification_report, accuracy_score
import joblib
from data_loader import load_financial_data
from preprocessing import FinancialPreprocessor

def train_fraud_model(limit=10000, use_synthetic=True):
    print("Starting model training pipeline...")
    
    # 1. Load Data
    df = load_financial_data(limit=limit, use_synthetic=use_synthetic)
    if df is None:
        print("Failed to load data.")
        return None, None
    
    # 2. Preprocess Data
    # Assuming 'isFraud' or similar is the target. The dataset description usually has 'isFraud' or 'class'.
    # Inspecting common columns for this dataset: step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud
    target_col = 'isFraud' 
    
    # Check if target exists, else try to find it
    if target_col not in df.columns:
        if 'is_fraud' in df.columns: target_col = 'is_fraud'
        elif 'Class' in df.columns: target_col = 'Class'
        else:
            print(f"Target column not found. Available: {df.columns}")
            return None, None
            
    print(f"Using target column: {target_col}")
    
    # Ensure target is integer (0/1) if it's boolean or other
    try:
        df[target_col] = df[target_col].astype(int)
    except:
        pass

    preprocessor = FinancialPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.preprocess_and_split(df, target_col=target_col)
    
    # 3. Train Model
    print("Training XGBoost model...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    model.fit(X_train, y_train)
    
    # 4. Evaluate
    y_pred = model.predict(X_test)
    print("Model Evaluation:")
    print(classification_report(y_test, y_pred))
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    
    # 5. Save Artifacts
    print("Saving model and preprocessor...")
    joblib.dump(model, 'xgboost_fraud_model.pkl')
    joblib.dump(preprocessor, 'preprocessor.pkl')
    
    return model, preprocessor

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Fraud Detection Model")
    parser.add_argument("--use-real", action="store_true", help="Use real dataset from Hugging Face instead of synthetic data")
    parser.add_argument("--limit", type=int, default=10000, help="Limit number of rows for training (default: 10000)")
    parser.add_argument("--no-limit", action="store_true", help="Train on full dataset (overrides --limit)")
    
    args = parser.parse_args()
    
    # Logic for data loading parameters
    use_synthetic = not args.use_real
    limit = args.limit
    if args.no_limit:
        limit = None
        
    print(f"Configuration: Real Data={args.use_real}, Limit={limit if limit else 'All'}")
    
    # Train
    train_fraud_model(limit=limit, use_synthetic=use_synthetic)
