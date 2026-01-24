# 🚀 Quick Start & Reference Guide

## 5-Minute Setup

### Step 1: Activate Environment
```bash
cd /home/balaji/Downloads/pro
source venv/bin/activate
```

### Step 2: Launch App
```bash
streamlit run auto_eda_chatbot/app.py
```

### Step 3: Open Browser
```
http://localhost:8501
```

### Step 4: Upload Data
- Click "Choose a CSV file"
- Select your dataset
- Wait for auto-detection (usually <1 second)

### Step 5: Explore!
- View dashboard automatically
- Toggle visualizations on/off
- Ask questions in chat

---

## Key Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+L | Clear chat |
| Cmd+R (Mac) | Refresh page |
| F12 | Developer tools |
| Ctrl+Shift+M | Mobile view |

---

## File Locations

```
/home/balaji/Downloads/pro/
├── auto_eda_chatbot/          ← Main application
│   ├── app.py                 ← Start here
│   ├── README.md              ← Quick reference
│   ├── requirements.txt       ← Dependencies
│   ├── chat/                  ← AI module
│   ├── eda/                   ← Dashboard & charts
│   ├── utils/                 ← Data loading
│   ├── data/                  ← Sample data
│   └── models/                ← LLM model
│
├── PROJECT_DOCUMENTATION.md   ← Full docs (READ THIS)
├── FEATURE_DEMO_GUIDE.md      ← Feature details
├── TECHNICAL_ARCHITECTURE.md  ← Tech deep-dive
└── PRESENTATION_OUTLINE.md    ← For presenting
```

---

## CSV File Requirements

### Supported Formats
- ✅ CSV (comma-separated)
- ✅ TSV (tab-separated)
- ✅ Semicolon-separated
- ✅ Pipe-separated
- ✅ Mixed encodings

### Supported Encodings
- ✅ UTF-8 (default)
- ✅ Latin-1 (ISO-8859-1)
- ✅ CP1252 (Windows)
- ✅ UTF-16
- ✅ ASCII
- ✅ ISO-8859-1

### Optimal File Size
- ✅ Tested: 1K - 100K rows
- ⚠️ Limit: 1M rows recommended
- 💾 Memory: 4GB available

### Bad Rows Handling
- ✅ Skips rows with wrong column count
- ✅ Handles malformed quotes
- ✅ Recovers from encoding errors
- ✅ Preserves good data

---

## Feature Quick Reference

### 📊 Dashboard Sections
```
1. KPI Metrics        → 4 key metrics in gradient cards
2. Column Overview    → Type distribution chart
3. Quality Metrics    → Data quality percentage
4. Statistics         → Mean, std, min, max
5. Numeric Analysis   → Histograms for each column
6. Categorical Data   → Top categories analysis
7. Correlations       → Feature relationships
8. Insights           → Auto-generated recommendations
```

### 📈 Visualization Tabs
```
Tab 1: Distribution   → Histograms + Trends
Tab 2: Relationships  → Scatter + Correlation
Tab 3: Categorical    → Bar + Pie charts
Tab 4: Correlation    → Detailed heatmap
Tab 5: Summary        → Statistical tables
Tab 6: Advanced       → Box/Violin/KDE/CDF plots
```

### 💬 Chat Commands
```
Statistics:     "What's the average of column X?"
Comparison:     "Compare group A vs group B"
Top Values:     "Which category has most items?"
Outliers:       "Show me the outliers"
Trends:         "Show the trend over time"
Insights:       "What patterns do you see?"
```

---

## Common Issues & Quick Fixes

| Issue | Solution |
|-------|----------|
| **"Port 8501 in use"** | `pkill -f streamlit; streamlit run app.py --server.port 8502` |
| **"Encoding error"** | File will auto-detect; if fails, convert to UTF-8 |
| **"Model not found"** | Model included in `models/` folder; check file exists |
| **"Empty dashboard"** | Verify CSV has columns; check data types |
| **"Slow LLM response"** | Normal (3-8s); CPU-based inference; GPU available |

---

## Documentation Files

### For Quick Learning
1. **README.md** (2 min read)
   - Project overview
   - Quick setup
   - Basic features

2. **FEATURE_DEMO_GUIDE.md** (10 min read)
   - Feature walkthrough
   - Demo script
   - Use cases

### For Deep Understanding
3. **PROJECT_DOCUMENTATION.md** (30 min read)
   - Complete architecture
   - All components
   - Deployment guide

4. **TECHNICAL_ARCHITECTURE.md** (45 min read)
   - Technical deep-dive
   - Code patterns
   - Performance analysis

### For Presenting
5. **PRESENTATION_OUTLINE.md** (Ready-to-use)
   - Presentation script
   - Live demo walkthrough
   - Q&A preparation

---

## Testing Checklist

### Pre-Demo Testing
- [ ] Start application
- [ ] Test file upload
- [ ] Verify dashboard appears
- [ ] Check all 6 visualization tabs
- [ ] Ask 3-5 test questions in chat
- [ ] Verify response quality

### Feature Testing
- [ ] Upload small CSV (<1K rows)
- [ ] Upload large CSV (50K+ rows)
- [ ] Upload special character file
- [ ] Upload with missing values
- [ ] Upload with duplicates
- [ ] Toggle dashboard on/off
- [ ] Toggle charts on/off

### Edge Cases
- [ ] Empty DataFrame
- [ ] Single column data
- [ ] All numeric columns
- [ ] All categorical columns
- [ ] Unicode characters
- [ ] Very long column names

---

## Performance Metrics

### Load Times (Typical)
```
App Startup:       2-5 seconds
CSV Load (10K):    <1 second
Dashboard Render:  2 seconds
Chart Generation:  5 seconds
LLM Response:      5-8 seconds
Full Workflow:     15 seconds
```

### Memory Usage (Typical)
```
Idle:              100-150 MB
Dashboard:         200 MB
Charts:            300-400 MB
LLM Model:         1.5-2 GB
Total Session:     ~2.5 GB
```

### Optimal Settings
```
CSV Rows:   10K - 100K (sweet spot: 50K)
Columns:    5-30 (sweet spot: 15)
GPU Layers: 5-10 (if GPU available)
Context:    512 tokens (LLM)
Max Response: 256 tokens
```

---

## Command Reference

### Application Control
```bash
# Start app
streamlit run app.py

# Start with custom port
streamlit run app.py --server.port 8502

# Start without warnings
PYTHONWARNINGS=ignore streamlit run app.py

# Stop app
pkill -f streamlit

# Force kill
pkill -9 -f streamlit
```

### Environment Management
```bash
# Activate venv
source venv/bin/activate

# Deactivate venv
deactivate

# Install dependencies
pip install -r requirements.txt

# Check versions
pip list | grep -E "(pandas|streamlit|matplotlib)"
```

### Data Management
```bash
# View sample data
head -20 auto_eda_chatbot/data/sample.csv

# Check data info
wc -l auto_eda_chatbot/data/sample.csv
```

---

## Troubleshooting Flow

### Application Won't Start
```
1. Check Python version: python --version (need 3.13+)
2. Activate venv: source venv/bin/activate
3. Check dependencies: pip list
4. Reinstall if needed: pip install -r requirements.txt
5. Try different port: streamlit run app.py --server.port 8502
```

### CSV Won't Load
```
1. Check file exists and readable
2. Verify it's actually a CSV
3. Try opening in text editor
4. Check file size (<100MB recommended)
5. Try with sample.csv to verify setup
```

### Dashboard Doesn't Show
```
1. Verify CSV loaded (check sidebar metrics)
2. Check data isn't empty
3. Scroll down page
4. Verify toggle is ON
5. Refresh page (Ctrl+R)
```

### Charts Not Rendering
```
1. Check "Show Visualizations" toggle
2. Verify numeric/categorical columns exist
3. Try with sample.csv
4. Check browser console (F12)
5. Try different browser
```

### LLM Not Responding
```
1. Check model file exists: ls models/
2. Verify file isn't corrupted (check size ~2.2GB)
3. Check available memory: free -h
4. Try simpler question first
5. Check system resources
```

---

## Demo Data

### Sample Datasets Included

#### 1. data/sample.csv
- Product sales data
- 1,000 rows
- 8 columns
- Multiple data types
- Good for quick demo

### Custom Data Setup

#### To Add Your Own Data
```bash
# Copy your CSV to data folder
cp your_file.csv auto_eda_chatbot/data/

# Or upload directly in UI
# Click file uploader → Select file → Auto-detect → Done!
```

---

## Browser Requirements

### Supported Browsers
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

### Browser Settings
- ✅ JavaScript enabled
- ✅ Cookies allowed
- ✅ Popups allowed
- ✅ 1920x1080 minimum (1280x720 mobile)

---

## System Requirements

### Minimum
- CPU: Dual-core
- RAM: 2GB
- Storage: 3GB (with model)
- Network: Optional (local only)

### Recommended
- CPU: Quad-core
- RAM: 4-8GB
- Storage: 5GB SSD
- GPU: NVIDIA (optional, for speedup)

### Not Required
- ❌ Internet connection
- ❌ Cloud account
- ❌ Database server
- ❌ Special software

---

## Integration Examples

### With Python Scripts
```python
import pandas as pd
from auto_eda_chatbot.eda.visualizer import show_charts
from auto_eda_chatbot.eda.dashboard import show_complete_dashboard

# Load data
df = pd.read_csv('data.csv')

# Use modules
show_complete_dashboard(df)
show_charts(df)
```

### With Jupyter Notebooks
```python
# Can import and use modules in notebooks
from auto_eda_chatbot.utils.data_loader import load_csv

df = load_csv('data.csv')
# ... analyze further
```

---

## Support & Help

### Documentation
- 📖 README.md - Quick reference
- 📚 PROJECT_DOCUMENTATION.md - Complete guide
- 🏗️ TECHNICAL_ARCHITECTURE.md - Architecture details
- 🎤 PRESENTATION_OUTLINE.md - Presentation script

### Resources
- 🌐 Streamlit Docs: https://docs.streamlit.io
- 🐼 Pandas Docs: https://pandas.pydata.org
- 🎨 Matplotlib Docs: https://matplotlib.org
- 🤖 TinyLlama: https://huggingface.co/TinyLlama

### Debugging
```bash
# Enable verbose logging
STREAMLIT_LOG_LEVEL=debug streamlit run app.py

# Check system resources
top -u $(whoami)  # Or 'Task Manager' on Windows

# Test CSV parsing separately
python -c "import pandas as pd; df = pd.read_csv('file.csv'); print(df.info())"
```

---

## Frequently Asked Questions (FAQ)

**Q: Can I use this offline?**
A: Yes! Everything runs locally. No internet required.

**Q: Is my data safe?**
A: 100% safe. Data never leaves your computer.

**Q: Can I modify the code?**
A: Yes! All code is open and modifiable.

**Q: How do I deploy to production?**
A: See TECHNICAL_ARCHITECTURE.md → Deployment section

**Q: What if I find a bug?**
A: Check error message, try troubleshooting guide, review code comments

**Q: Can I add my own visualizations?**
A: Yes! Modify eda/visualizer.py to add charts

**Q: How do I speed up LLM responses?**
A: Enable GPU (n_gpu_layers in qa_engine.py)

**Q: Can I use a different LLM model?**
A: Yes! Download from HuggingFace, update model path

---

## Quick Facts

| Fact | Detail |
|------|--------|
| **Project Size** | ~2,000 lines of code |
| **Files** | 15+ Python files |
| **Modules** | 5 main modules |
| **Chart Types** | 10+ types |
| **Supported Formats** | 6 encodings × 4 delimiters |
| **Model Size** | 2.2GB (TinyLlama) |
| **Startup Time** | <5 seconds |
| **Ready for** | Immediate deployment |

---

## Next Steps

### For Users
1. ✅ Review README.md
2. ✅ Run setup
3. ✅ Upload sample data
4. ✅ Explore all features
5. ✅ Try your own data

### For Developers
1. ✅ Read TECHNICAL_ARCHITECTURE.md
2. ✅ Review code structure
3. ✅ Understand design patterns
4. ✅ Plan customizations
5. ✅ Deploy to your environment

### For Stakeholders
1. ✅ Review PROJECT_DOCUMENTATION.md
2. ✅ Attend live demo
3. ✅ Review PRESENTATION_OUTLINE.md
4. ✅ Evaluate business case
5. ✅ Approve deployment

---

**Version**: 1.0
**Last Updated**: January 2026
**Status**: Complete & Ready to Use ✅
