# 🚀 Advanced Chatbot Features Guide

## Overview
Your chatbot now has **5 powerful data search and analysis commands** plus natural language questions!

---

## 🎯 Quick Command Reference

| Command | Syntax | Example | Use Case |
|---------|--------|---------|----------|
| **Search** | `search: <term>` | `search: John` | Find specific data entries |
| **Filter** | `filter: col \| op \| val` | `filter: age \| > \| 30` | Filter rows by criteria |
| **Stats** | `stats: <column>` | `stats: salary` | Get detailed column statistics |
| **Compare** | `compare: col1 vs col2` | `compare: age vs income` | Analyze two columns together |
| **List** | `columns` | `columns` | Show all available columns |
| **Ask** | Just type! | `What's the average?` | Natural language questions |

---

## 📖 Detailed Examples

### 1️⃣ SEARCH DATA
**Find specific values anywhere in your dataset**

```
search: keyword
```

**Examples:**
```
search: New York
search: Customer_123
search: high priority
search: 2024
```

**What it does:**
- Searches across ALL columns
- Case-insensitive
- Returns all matching rows
- Shows exact matches

**When to use:**
- Looking for specific customer
- Finding particular transaction
- Searching for specific values
- Quick data lookup

---

### 2️⃣ FILTER DATA
**Get rows matching specific criteria**

```
filter: column_name | operator | value
```

**Operators Available:**
- `=` → equals
- `<` → less than
- `>` → greater than
- `<=` → less than or equal
- `>=` → greater than or equal
- `!=` → not equal
- `contains` → text contains

**Examples:**

**Numeric Filtering:**
```
filter: age | > | 30
filter: salary | >= | 50000
filter: score | < | 80
filter: months | = | 12
```

**Text Filtering:**
```
filter: city | contains | Los
filter: status | = | active
filter: department | != | sales
```

**When to use:**
- Filter by age, salary, score
- Find active/inactive records
- Get data from specific location
- Find data in specific date range

---

### 3️⃣ COLUMN STATISTICS
**Get detailed statistics about any column**

```
stats: column_name
```

**Examples:**
```
stats: age
stats: salary
stats: customer_id
stats: revenue
```

**Returns (for numeric columns):**
- Count
- Mean (average)
- Median (middle value)
- Std Dev (variation)
- Min value
- Max value
- 25th percentile (Q1)
- 75th percentile (Q3)
- Missing values
- Unique values
- Data type

**Returns (for text columns):**
- Count
- Unique values
- Most common values (top 5)
- Missing values
- Data type

**When to use:**
- Understand column distribution
- Find min/max values
- Check data quality
- Get summary statistics
- Identify outliers

---

### 4️⃣ COMPARE COLUMNS
**Analyze relationships between two columns**

```
compare: column1 vs column2
```

**Examples:**
```
compare: age vs salary
compare: experience vs performance
compare: budget vs actual
compare: height vs weight
```

**Returns:**
- Correlation coefficient (how related they are)
- Statistics for column 1
- Statistics for column 2
- Side-by-side comparison
- Unique values
- Missing data info

**When to use:**
- Understand correlations
- Find relationships
- Compare similar metrics
- Analyze cause and effect

**Correlation Interpretation:**
- `1.0` = Perfect positive correlation
- `0.0` = No correlation
- `-1.0` = Perfect negative correlation
- `0.7+` = Strong correlation
- `0.3-0.7` = Moderate correlation
- `<0.3` = Weak/no correlation

---

### 5️⃣ LIST COLUMNS
**See all available columns**

```
columns
```

**Variations:**
```
list columns
show columns
```

**Returns:**
- Column name
- Data type (int64, float64, object)
- Available for search, filter, stats

**When to use:**
- First time using dataset
- Forget column names
- See all available data
- Plan your analysis

---

### 6️⃣ NATURAL LANGUAGE QUESTIONS
**Ask questions in plain English**

```
Just type your question!
```

**Examples:**
```
What's the average salary?
How many unique customers?
What patterns do you see?
Describe the data quality
Are there outliers?
What's the data range?
Summarize this dataset
What correlations exist?
```

**AI can help with:**
- Data summaries
- Pattern identification
- Anomaly detection
- Quality assessment
- Trend analysis
- Business insights
- Recommendation

---

## 💡 Workflow Examples

### Scenario 1: Analyze Customer Age
```
1. stats: age
   → Get age distribution

2. filter: age | > | 65
   → Find elderly customers

3. search: VIP
   → Find VIP customers in that group

4. What's the average age of VIPs?
   → Ask AI for insight
```

### Scenario 2: Find Top Performers
```
1. stats: performance_score
   → Understand score range

2. filter: performance_score | >= | 80
   → Get high performers

3. search: promoted
   → Check if they're promoted

4. Describe top performers
   → Ask AI for summary
```

### Scenario 3: Compare Two Metrics
```
1. compare: revenue vs cost
   → See correlation

2. filter: profit | < | 0
   → Find unprofitable items

3. search: 2024
   → Filter to specific year

4. What's driving low profit?
   → Ask AI for analysis
```

### Scenario 4: Data Quality Check
```
1. columns
   → See all columns

2. What's the data quality?
   → Ask for assessment

3. stats: key_column
   → Check specific column

4. search: NULL or empty
   → Find missing data
```

---

## 🎨 Command Tips & Tricks

### ✅ DO's

✓ **Be specific with column names**
```
search: John Davis
filter: customer_age | > | 30
stats: monthly_revenue
```

✓ **Use exact operators**
```
filter: status | = | active     ← Correct
filter: status contains active  ← Wrong format
```

✓ **Combine multiple commands**
```
1. stats: score
2. filter: score | < | 50
3. How many failed?
```

✓ **Follow up questions work**
```
1. filter: age | > | 30
2. What's the average salary?
   → AI understands it's about filtered data
```

### ❌ DON'Ts

✗ **Don't use wrong syntax**
```
search:John    ← Missing space
stats column   ← Missing colon
filter age 30  ← Missing pipes
```

✗ **Don't quote column names**
```
stats: "age"  ← Wrong (sometimes)
stats: age    ← Correct
```

✗ **Don't mix operators**
```
filter: age > 30 | and | < 65  ← Wrong
filter: age | > | 30           ← Correct, then ask follow-up
```

✗ **Don't assume data structure**
```
→ Always use "columns" first
→ Use "stats" to understand data
→ Then create filters
```

---

## 🔧 Advanced Usage

### Multi-Step Analysis

**Step 1: Explore**
```
columns
→ See what you have
```

**Step 2: Understand**
```
stats: key_column
→ Get distribution
```

**Step 3: Filter**
```
filter: status | = | active
→ Get subset
```

**Step 4: Analyze**
```
What's the pattern?
→ Ask AI about filtered data
```

**Step 5: Deep Dive**
```
compare: column1 vs column2
→ Find relationships
```

### Chaining Commands

1. Start with search
2. Then filter results
3. Compare related columns
4. Get statistics
5. Ask questions about insights

---

## 📊 Common Analysis Patterns

### Sales Analysis
```
filter: status | = | completed
stats: amount
compare: region vs revenue
Which region performs best?
```

### Customer Segmentation
```
stats: age
filter: age | > | 30
search: premium
compare: age vs purchase_value
```

### Quality Control
```
stats: quality_score
filter: quality_score | < | 80
search: defect
Are there patterns?
```

### Performance Review
```
stats: rating
filter: rating | >= | 4
compare: experience vs rating
Who are top performers?
```

---

## 🆘 Troubleshooting

### "Column not found"
✓ Run `columns` to see exact names
✓ Check spelling carefully
✓ Column names are case-sensitive

### "Search returned nothing"
✓ Try broader search terms
✓ Check if value exists with `columns`
✓ Try different search terms

### "Filter shows no results"
✓ Check data type (number vs text)
✓ Use `stats: column` to see range
✓ Verify operator and value

### "Comparison shows N/A"
✓ Columns might be text, not numeric
✓ Use `stats: column` to check type
✓ Compare only numeric columns

---

## 🎓 Learning Path

**Beginner:**
1. Use `columns` to explore
2. Ask simple questions
3. Use `stats` for one column

**Intermediate:**
1. Try `search` and `filter`
2. Compare two columns
3. Ask follow-up questions

**Advanced:**
1. Combine multiple commands
2. Multi-step analysis
3. Complex patterns
4. Custom insights

---

## 📝 Example Queries

### Data Exploration
- `columns` → See all columns
- `What's in this dataset?` → Get overview
- `stats: [main_column]` → Understand key data

### Searching
- `search: specific_value` → Find entries
- `search: 2024` → Filter by year
- `search: premium` → Find category

### Filtering
- `filter: age | > | 25` → Age-based
- `filter: status | = | active` → Status
- `filter: price | < | 100` → Price range

### Analysis
- `compare: x vs y` → Relationship
- `What patterns exist?` → Insights
- `Are there outliers?` → Anomalies
- `Summarize the data` → Overview

### Business Questions
- `Top customers?` → Who to focus on
- `Most common value?` → Trends
- `Data quality report` → Health check
- `Recommendations?` → Next steps

---

## 🚀 Pro Tips

1. **Start with exploration**
   - Always run `columns` first
   - Use `stats` on key columns
   - Ask AI for overview

2. **Be methodical**
   - One filter at a time
   - Check each result
   - Build on findings

3. **Combine methods**
   - Search → Filter → Analyze
   - Multiple perspectives
   - Cross-validate findings

4. **Ask follow-ups**
   - Results trigger questions
   - AI understands context
   - Build on answers

5. **Document insights**
   - Save important findings
   - Note patterns
   - Create reports

---

## ❓ FAQ

**Q: Can I search in specific columns?**
A: Not directly, but search across all columns works well.

**Q: How specific can filters be?**
A: One column, one operator, one value per command.

**Q: Can I combine filters?**
A: Do multiple filters sequentially or ask AI for complex logic.

**Q: Will AI remember my filters?**
A: AI sees the current session; follow-ups understand context.

**Q: What if I make a typo?**
A: Error message shows; correct and try again.

**Q: How fast are responses?**
A: Search/Filter: instant, Stats: 1-2 seconds, AI: 5-10 seconds

---

## 🎯 Next Steps

1. **Start Exploring**: Use `columns` command
2. **Try Searching**: Find specific data
3. **Experiment Filtering**: Create queries
4. **Ask Questions**: Get AI insights
5. **Combine Commands**: Multi-step analysis

**Happy analyzing!** 📊✨

---

**Last Updated**: January 2026  
**Version**: 2.0 (Enhanced)  
**Status**: Ready to use
