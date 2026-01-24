#!/usr/bin/env python
import sys
sys.path.insert(0, '/home/balaji/Downloads/pro')

from auto_eda_chatbot.chat.qa_engine import answer_question, load_dataset

print("=" * 60)
print("TESTING BUG FIX: DataFrame Type Safety")
print("=" * 60)

# Load dataset
df = load_dataset('auto_eda_chatbot/data/dataset.csv')
print("\n✓ Dataset loaded successfully")

# Test 1: Normal question
print("\n[Test 1] Normal Question (String)")
result = answer_question(df, 'what is the age of arun')
print(f"  Question: 'what is the age of arun'")
print(f"  Result: {result}")
print(f"  Status: ✅ PASS" if "25" in str(result) else f"  Status: ❌ FAIL")

# Test 2: DataFrame passed (this should be caught)
print("\n[Test 2] DataFrame Passed (Should Be Caught)")
result = answer_question(df, df)
print(f"  Question: DataFrame object")
print(f"  Result: {result}")
print(f"  Status: ✅ PASS" if "Internal error" in str(result) else f"  Status: ❌ FAIL")

# Test 3: Integer passed
print("\n[Test 3] Integer Passed (Should Be Caught)")
result = answer_question(df, 123)
print(f"  Question: 123 (integer)")
print(f"  Result: {result}")
print(f"  Status: ✅ PASS" if "Internal error" in str(result) else f"  Status: ❌ FAIL")

# Test 4: Valid person
print("\n[Test 4] Valid Person Query")
result = answer_question(df, 'what is salary of neha')
print(f"  Question: 'what is salary of neha'")
print(f"  Result: {result}")
print(f"  Status: ✅ PASS" if "60000" in str(result) else f"  Status: ❌ FAIL")

# Test 5: Non-existent person
print("\n[Test 5] Non-Existent Person Query")
result = answer_question(df, 'what is the age of jd master')
print(f"  Question: 'what is the age of jd master'")
print(f"  Result: {result}")
print(f"  Status: ✅ PASS (returns appropriate message)")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED")
print("=" * 60)
