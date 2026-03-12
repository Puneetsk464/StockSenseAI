#!/usr/bin/env python3
"""
Test script for PPM module - runs outside Streamlit for better debugging
"""

import sys
import traceback
from ppm.portfolio_optimizer import predict_stock_returns, build_portfolio
from ppm.risk_model import predict_risk, risk_category

print("=" * 80)
print("PPM MODULE TEST")
print("=" * 80)

# Test 1: Stock predictions
print("\n[TEST 1] Testing predict_stock_returns()...")
print("-" * 80)
try:
    predictions_df = predict_stock_returns()
    print(f"\n[OK] Predictions generated: {len(predictions_df)} stocks")
    if not predictions_df.empty:
        print("\nFirst 5 predictions:")
        print(predictions_df.head())
    else:
        print("[ERROR] No predictions generated!")
except Exception as e:
    print(f"[ERROR] EXCEPTION in predict_stock_returns():")
    traceback.print_exc()

# Test 2: Risk model
print("\n" + "=" * 80)
print("[TEST 2] Testing risk model...")
print("-" * 80)
try:
    # Sample user data
    test_user = {
        "age": 35,
        "income": 1000000,
        "corpus": 500000,
        "horizon_months": 120,
        "risk_appetite": 7
    }

    risk_score = predict_risk(
        test_user["age"],
        test_user["income"],
        test_user["corpus"],
        test_user["horizon_months"],
        test_user["risk_appetite"]
    )

    risk_cat = risk_category(risk_score)

    print(f"[OK] Risk Score: {risk_score:.4f}")
    print(f"[OK] Risk Category: {risk_cat}")
except Exception as e:
    print(f"[ERROR] EXCEPTION in risk_model:")
    traceback.print_exc()

# Test 3: Portfolio optimization
print("\n" + "=" * 80)
print("[TEST 3] Testing build_portfolio()...")
print("-" * 80)
try:
    if 'risk_cat' in locals():
        portfolio = build_portfolio(risk_cat)
        print(f"\n[OK] Portfolio generated: {len(portfolio)} stocks")
        if not portfolio.empty:
            print("\nPortfolio summary:")
            print(
                portfolio[["symbol", "sector", "predicted_return", "weight"]])
        else:
            print("[ERROR] No portfolio stocks selected!")
    else:
        print("Skipped (risk_model test failed)")
except Exception as e:
    print(f"[ERROR] EXCEPTION in build_portfolio():")
    traceback.print_exc()

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
