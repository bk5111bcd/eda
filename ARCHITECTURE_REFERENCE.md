# Quick Reference - Chatbot Architecture

## The Golden Rule

```
LLM should NEVER retrieve data.
Only reason over already retrieved data.
```

## The Two Brains

```
Brain 1: Pandas (Code)
├─ Retrieves exact data
├─ 100% deterministic
└─ Never hallucinates ✓

Brain 2: LLM (Model)
├─ Analyzes patterns
├─ Only called if Brain 1 returns None
└─ Safe because no data responsibility ✓
```

## Function Call Flow

```
User asks question
    ↓
chat_with_context()
    ↓
answer_question()  [Router]
    ├─ retrieve_from_dataset() [Brain 1: Pandas]
    │  └─ Returns data/error/None
    │
    └─ If None → ask_llm_for_analysis() [Brain 2: LLM]
       └─ Returns analysis only
```

## What Pandas Handles (retrieve_from_dataset)

```python
✓ Explicit commands
  - search: John
  - filter: salary | > | 50000
  - stats: age
  - compare: age vs salary
  - columns

✓ Data lookups
  - "What is salary of Arun?"
  - "How old is Neha?"
  - "What department does Leo work in?"

✗ Analysis questions (returns None)
  - "What patterns in salary?"
  - "Describe trends"
  - These go to LLM
```

## What LLM Handles (ask_llm_for_analysis)

```python
✓ Analysis (only if Pandas returned None)
  - "What patterns do you see?"
  - "Describe the data"
  - "Are there trends?"

✗ Data lookups (blocked by prompt)
  - Prompt says: "Never guess factual data"
  - Only called after Pandas fails
  - Safe because isolated from data retrieval
```

## The Router Logic

```python
def answer_question(df, question):
    result = retrieve_from_dataset(df, question)
    
    if result is not None:
        return result  # Pandas answered it
    else:
        return ask_llm_for_analysis(question, df)  # Pandas failed
```

**Key Point:** If Pandas returns ANYTHING (even error), use it. Never fallback to LLM for data.

## Three Test Cases

### Case 1: Data exists
```
Q: "What is the salary of Arun?"
A: "✓ Arun's salary: 45000"
Path: Pandas (Brain 1) → Return immediately
```

### Case 2: Data doesn't exist
```
Q: "What is the salary of Batman?"
A: "❌ 'Batman' not found in dataset"
Path: Pandas (Brain 1) → Return error immediately
```

### Case 3: Analysis question
```
Q: "What patterns in salary?"
A: "Salaries range X to Y, average Z..."
Path: Pandas (Brain 1) returns None → LLM (Brain 2)
```

## Keywords to Trigger Pandas

```
Static: salary, age, department, city, degree, date, etc.
Dynamic: All CSV column names automatically
Semantic: "admission_date" matches "adm_date", "joining_date"

If ANY keyword found → Try Pandas
If NO keyword found → Go to LLM
```

## Error Messages (Explicit, Never Guesses)

```python
"❌ 'John' not found in dataset"
"❌ 'salary' column not found. Available: name, age, ..."
"❌ Cannot parse entity name"
"❌ Column 'xyz' not found"

Never says:
"John is probably a software engineer" ← Guess
"Salary data unavailable" ← Vague
"I think John earns..." ← Hallucination
```

## Why This Beats Old Approaches

| Old Way | New Way |
|---------|---------|
| LLM + CSV → Hallucination | Pandas first → Exact answer |
| "I think..." | "✓ Data says..." OR "❌ Not found" |
| Slow (LLM for everything) | Fast (Pandas for data, LLM for analysis) |
| Unreliable | 100% deterministic for data |
| User confusion | Clear separation |

## Extension Guide

### Add New Keyword
```python
# In retrieve_from_dataset()
if "new_keyword" in q:
    # Handle it with Pandas
```

### Add New Command
```python
# In retrieve_from_dataset()
if q.startswith('newcommand:'):
    # Handle it with Pandas
```

### Add New LLM Feature
```python
# Modify ask_llm_for_analysis()
# Change prompt, temperature, etc.
```

## Safety Checklist

- [ ] Pandas handles data lookup
- [ ] LLM handles analysis only
- [ ] Explicit errors (no guesses)
- [ ] Router never falls through wrong way
- [ ] Prompt prevents hallucination
- [ ] Temperature is low (0.2)
- [ ] Max tokens is limited (120)
- [ ] No CSV in LLM prompt

---

## The One Line You Must Remember

**If Pandas can answer it, let Pandas answer it. Period.**

Never call LLM for data retrieval, no matter how smart the model is.
