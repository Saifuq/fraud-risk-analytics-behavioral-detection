

-- 1. DATA VALIDATION: Check Fraud vs. Non-Fraud Distribution
SELECT 
    is_fraud, 
    COUNT(*) AS total_transactions,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM finance), 2) AS percentage
FROM finance
GROUP BY is_fraud;


-- 3. RISK BUCKETING: Tri-Tier Risk Scoring System

SELECT 
    transaction_id,
    amount_ngn,
    CASE 
        WHEN velocity_score > 15 OR spending_deviation_score > 3.0 OR geo_anomaly_score > 0.8 THEN 'High Risk'
        WHEN velocity_score BETWEEN 10 AND 15 OR spending_deviation_score BETWEEN 1.5 AND 3.0 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_segment,
    is_fraud
FROM finance;

-- 5. MERCHANT CATEGORY ANALYSIS: High-Risk Merchants

SELECT 
    merchant_category,
    COUNT(transaction_id) AS total_txns,
    SUM(CASE WHEN is_fraud = TRUE THEN 1 ELSE 0 END) AS fraud_count,
    ROUND(AVG(CASE WHEN is_fraud = TRUE THEN 1.0 ELSE 0.0 END) * 100, 2) AS category_fraud_rate_pct
FROM  finance
GROUP BY merchant_category
HAVING fraud_count > 0
ORDER BY category_fraud_rate_pct DESC;

-- 6. TIME-BASED ANALYSIS: Night-Time vs. Salary Week Trends

SELECT 
    is_night_txn,
    is_salary_week,
    COUNT(transaction_id) AS total_txns,
    SUM(CASE WHEN is_fraud = TRUE THEN 1 ELSE 0 END) AS fraud_count
FROM  finance
GROUP BY is_night_txn, is_salary_week;

-- 7. PERSONA-BASED RISK: Fraud Distribution by User Type
SELECT 
    sender_persona,
    COUNT(*) AS txn_count,
    SUM(CASE WHEN is_fraud = TRUE THEN 1 ELSE 0 END) AS fraud_count,
    ROUND(AVG(CASE WHEN is_fraud = TRUE THEN 1.0 ELSE 0.0 END) * 100, 2) AS persona_fraud_rate_pct
FROM finance
GROUP BY sender_persona
ORDER BY persona_fraud_rate_pct DESC;


