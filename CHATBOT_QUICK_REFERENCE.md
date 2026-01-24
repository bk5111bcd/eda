# 🚀 Chatbot Commands at a Glance

## 5 Powerful New Commands

```
┌─────────────────────────────────────────────────────────────────┐
│                    SEARCH DATA 🔍                               │
├─────────────────────────────────────────────────────────────────┤
│  Syntax:  search: keyword                                       │
│  Example: search: John                                          │
│  Returns: All rows containing "John"                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    FILTER DATA 🎯                               │
├─────────────────────────────────────────────────────────────────┤
│  Syntax:  filter: column | operator | value                    │
│  Example: filter: age | > | 30                                 │
│  Returns: Rows where age > 30                                  │
│  Operators: = < > <= >= != contains                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              COLUMN STATISTICS 📊                               │
├─────────────────────────────────────────────────────────────────┤
│  Syntax:  stats: column_name                                   │
│  Example: stats: salary                                        │
│  Returns: Mean, Median, Min, Max, Std Dev, etc.               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│             COMPARE COLUMNS 🔗                                  │
├─────────────────────────────────────────────────────────────────┤
│  Syntax:  compare: column1 vs column2                          │
│  Example: compare: age vs salary                               │
│  Returns: Correlation, Stats for both                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│             LIST COLUMNS 📋                                     │
├─────────────────────────────────────────────────────────────────┤
│  Syntax:  columns (or list columns, show columns)              │
│  Returns: All columns with data types                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│          + NATURAL QUESTIONS 💬 (Still Works!)                 │
├─────────────────────────────────────────────────────────────────┤
│  Example: What patterns exist?                                 │
│  Example: Average value?                                       │
│  Example: Are there outliers?                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Command Reference Table

| # | Command | Syntax | Example | Use |
|---|---------|--------|---------|-----|
| 1️⃣ | SEARCH | `search: term` | `search: apple` | Find specific data |
| 2️⃣ | FILTER | `filter: col \| op \| val` | `filter: age \| > \| 30` | Get subset |
| 3️⃣ | STATS | `stats: column` | `stats: salary` | Column analysis |
| 4️⃣ | COMPARE | `compare: c1 vs c2` | `compare: x vs y` | Correlation |
| 5️⃣ | COLUMNS | `columns` | `columns` | See all data |
| 6️⃣ | ASK | Just type! | `What's avg?` | Natural questions |

---

## 💡 Quick Examples

### 🔍 SEARCH
```
search: customer_name
→ Finds all rows with that customer name

search: 2024
→ Finds all rows with "2024"

search: urgent
→ Finds all "urgent" items
```

### 🎯 FILTER
```
filter: age | > | 30
→ All rows where age > 30

filter: status | = | active
→ All active records

filter: city | contains | New
→ Cities containing "New"
```

### 📊 STATS
```
stats: age
→ Mean, Min, Max, Std Dev

stats: revenue
→ Total, Average, Distribution

stats: category
→ Unique values, Most common
```

### 🔗 COMPARE
```
compare: age vs salary
→ Correlation + Both stats

compare: experience vs rating
→ How related they are
```

### 📋 LIST
```
columns
→ Name | Data Type
   age  | int64
   name | object
   ...
```

---

## 🎯 Common Workflows

### Workflow 1: Find & Analyze
```
1. search: VIP
   ↓
2. stats: spending
   ↓
3. What patterns?
```

### Workflow 2: Filter & Explore
```
1. filter: age | > | 65
   ↓
2. How many found?
   ↓
3. compare: age vs health
```

### Workflow 3: Deep Dive
```
1. columns
   ↓
2. stats: key_column
   ↓
3. filter: column | > | threshold
   ↓
4. What's interesting?
```

---

## 📈 Filter Operators Guide

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | equals | `filter: status \| = \| active` |
| `<` | less than | `filter: age \| < \| 30` |
| `>` | greater than | `filter: salary \| > \| 50000` |
| `<=` | less or equal | `filter: score \| <= \| 80` |
| `>=` | greater or equal | `filter: rating \| >= \| 4` |
| `!=` | not equal | `filter: type \| != \| test` |
| `contains` | text contains | `filter: city \| contains \| York` |

---

## ✨ Features Summary

```
BEFORE:
├─ Ask questions (AI only)
└─ Wait for AI response

AFTER:
├─ Search data instantly ✨
├─ Filter by criteria instantly ✨
├─ Get statistics instantly ✨
├─ Compare columns instantly ✨
├─ List all data instantly ✨
├─ Ask questions (AI still here)
└─ Combine all above
```

---

## 🎮 In the App

### You'll See:
1. **Chat Input Box**
   - Type commands or questions
   - Examples shown
   - Button hints

2. **Available Commands Help** 
   - Click "📚 Available Commands & Help"
   - See all commands
   - Get examples

3. **Suggested Buttons**
   - Quick questions
   - Search/Filter examples
   - Analysis templates

---

## 📝 Command Format Guide

```
✅ CORRECT:
search: apple
filter: age | > | 30
stats: salary
compare: age vs income
columns

❌ WRONG:
search:apple          (no space)
filter: age > 30      (missing pipes)
stats column          (missing colon)
filter age | > | 30   (missing column)
```

---

## 🔄 Command + Question Workflow

```
1. Run command to get data:
   filter: age | > | 30

2. Ask follow-up question:
   What's the average salary?
   
   → AI understands it's about filtered data
```

---

## 📚 Documentation Links

| Doc | Content | Read Time |
|-----|---------|-----------|
| **ADVANCED_CHAT_FEATURES.md** | Full guide, examples, workflows | 20 min |
| **CHATBOT_ENHANCEMENT_SUMMARY.md** | Overview of changes | 5 min |
| **This File** | Quick reference | 2 min |
| **In-App Help** | Built-in documentation | 3 min |

---

## 🚀 Get Started Now!

1. Open the app
2. Upload a CSV
3. Try commands:
   - `columns`
   - `search: any_value`
   - `filter: column | > | value`
   - `stats: column`
   - `compare: col1 vs col2`
4. Ask questions!

---

## 💪 Power Moves

### Multi-Step Analysis:
```
1. columns
2. stats: column_name
3. filter: column | operator | value
4. compare: related_column1 vs related_column2
5. What patterns do you see?
```

### Complex Queries:
```
1. search: specific_value
2. filter: remaining_data | by | criteria
3. stats: key_column (of filtered data)
4. Why these patterns?
```

---

## ⚡ Speed Tips

- **Instant**: search, filter, stats, compare
- **Fast**: columns (shows all)
- **Needs AI**: questions (5-10 sec)

---

## 🎯 When to Use Each

| Situation | Command |
|-----------|---------|
| Find customer #123 | `search:` |
| Get all high values | `filter:` |
| Understand column | `stats:` |
| See relationship | `compare:` |
| What columns? | `columns` |
| General insight | Ask question |

---

## 📞 Need Help?

1. **In App**: Click "📚 Available Commands & Help"
2. **Full Guide**: Read `ADVANCED_CHAT_FEATURES.md`
3. **Examples**: Check button hints in app
4. **This File**: `CHATBOT_QUICK_REFERENCE.md`

---

## ✅ Verification Checklist

Try these to verify everything works:

- [ ] `columns` shows your columns
- [ ] `search: value` finds data
- [ ] `filter: col | > | num` filters rows
- [ ] `stats: col` shows statistics
- [ ] `compare: c1 vs c2` shows correlation
- [ ] Questions still work

---

**Ready to explore your data like never before!** 🚀

---

*Last Updated: January 23, 2026*  
*Version: 2.0*  
*Status: ✅ Production Ready*
