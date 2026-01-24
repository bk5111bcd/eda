# 🤖 Auto EDA Chatbot Dashboard

A comprehensive data analysis application that combines **Exploratory Data Analysis (EDA)** with **AI-powered Q&A** capabilities. Upload a CSV file and get instant insights with beautiful visualizations and intelligent answers to your data questions.

---

## 📋 Project Overview

This project is a full-stack data analysis tool that automates the process of:
- **Data Exploration** - Automatic statistical analysis
- **Data Visualization** - Multiple chart types and insights
- **Intelligent Q&A** - AI-powered answers about your dataset

---

## 🛠️ Technologies & Languages Used

### **Primary Language**
- **Python 3.13** - Core programming language

### **Frontend Framework**
- **Streamlit** - Web UI framework for rapid data app development
  - Used for: Dashboard, file upload, interactive components, caching

### **Data Processing Libraries**
- **Pandas** - Data manipulation and analysis
  - CSV loading, data cleaning, statistics
- **NumPy** - Numerical computing
  - Array operations, numerical calculations

### **Visualization Libraries**
- **Matplotlib** - Static plotting library
  - Bar charts, line charts, scatter plots
- **Seaborn** - Statistical data visualization
  - Heatmaps, correlation analysis, styled plots

### **Machine Learning**
- **Scikit-learn** - ML library
  - For future ML capabilities and data preprocessing

### **AI/LLM Components**
- **llama-cpp-python** - Local LLM inference
  - Runs TinyLlama model locally (no API needed)
  - Text generation for Q&A functionality

### **Model**
- **TinyLlama-1.1B-Chat-Q4_K_M.gguf** - Quantized LLM
  - 1.1B parameters (lightweight)
  - Q4 quantization (optimized for CPU/GPU)
  - Chat-optimized variant

---

## 📁 Project Structure

```
auto_eda_chatbot/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── chat/                     # Q&A Engine Module
│   ├── __init__.py
│   └── qa_engine.py          # AI-powered question answering
│
├── eda/                      # Exploratory Data Analysis Module
│   ├── __init__.py
│   ├── visualizer.py         # Data visualization functions
│   ├── insights.py           # Statistical insights (future)
│   ├── profiler.py           # Data profiling (future)
│   └── __pycache__/
│
├── utils/                    # Utility Functions Module
│   ├── __init__.py
│   ├── data_loader.py        # CSV loading utilities
│   └── __pycache__/
│
├── data/                     # Sample Data
│   └── sample.csv            # Example dataset
│
└── models/                   # AI Models
    ├── TinyLlama-1.1B-Chat-Q4_K_M.gguf  # Main LLM (2.2GB)
    └── tinyllama.gguf        # Alternative model (backup)
```

---

## 🎯 Key Features

### 1️⃣ **Data Upload & Preview**
```python
- Upload CSV files
- Automatic data type detection
- Display dataset metrics (rows, columns, missing values)
```

### 2️⃣ **Automated Visualizations**
Multiple chart types organized in 5 tabs:
- **Distribution Tab**: Histograms, Line Charts
- **Relationships Tab**: Scatter plots, Correlation heatmaps
- **Categorical Tab**: Bar charts, Pie charts
- **Correlation Tab**: Detailed correlation analysis
- **Summary Tab**: Statistical summaries

### 3️⃣ **Intelligent Q&A System**
- Ask questions about your data
- AI analyzes dataset context
- Provides data-driven answers
- Uses local LLM (no internet required)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Streamlit Web Interface         │
│  (app.py - File upload, UI components)  │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
    ┌───▼───┐    ┌────▼────┐
    │  EDA  │    │  Chat   │
    │Module │    │ Module  │
    └───┬───┘    └────┬────┘
        │             │
    ┌───▼────────────▼────┐
    │   Data Processing   │
    │  (Pandas, NumPy)    │
    └─────────┬───────────┘
              │
    ┌─────────▼──────────┐
    │  Visualizations    │
    │ (Matplotlib/Seaborn)
    │  + AI Responses    │
    │(llama-cpp-python)  │
    └────────────────────┘
```

---

## 🚀 How It Works

### **Workflow:**

1. **User uploads CSV** → Streamlit handles file upload
2. **Data is loaded** → Pandas reads and parses data
3. **Metrics calculated** → NumPy & Pandas compute statistics
4. **Visualizations generated** → Matplotlib & Seaborn create charts
5. **User asks question** → Text input captured
6. **AI analyzes data** → llama-cpp-python runs local LLM
7. **Answer displayed** → Streamlit shows response

### **Data Flow:**

```
CSV File
   ↓
Pandas DataFrame
   ↓
├─→ Visualization Pipeline (EDA Module)
│   ├─→ Histograms, Line Charts, Scatter Plots
│   ├─→ Heatmaps, Bar Charts, Pie Charts
│   └─→ Statistical Summaries
│
└─→ Q&A Pipeline (Chat Module)
    ├─→ Extract dataset info
    ├─→ Create context prompt
    ├─→ LLM inference (TinyLlama)
    └─→ Return answer
```

---

## 💻 Installation & Setup

### **1. Clone/Setup Project**
```bash
cd /home/balaji/Downloads/pro/auto_eda_chatbot
```

### **2. Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run Application**
```bash
streamlit run app.py
```

The app will open at: `http://localhost:8501`

---

## 📦 Dependencies Explained

| Library | Version | Purpose |
|---------|---------|---------|
| **streamlit** | Latest | Web framework & UI components |
| **pandas** | Latest | Data manipulation & analysis |
| **numpy** | Latest | Numerical computations |
| **matplotlib** | Latest | Static plots & charts |
| **seaborn** | Latest | Statistical visualizations |
| **scikit-learn** | Latest | ML preprocessing & algorithms |
| **llama-cpp-python** | Latest | Local LLM inference engine |
| **wordcloud** | Latest | Future: word cloud visualizations |

---

## 🔧 Module Details

### **app.py** (Main Entry Point)
```python
✓ Streamlit page configuration
✓ CSV file upload widget
✓ Dataset metrics display
✓ Visualization rendering
✓ Q&A interface
✓ Caching for performance
```

### **chat/qa_engine.py** (Q&A System)
```python
✓ Load local TinyLlama model
✓ Extract dataset context
✓ Generate intelligent prompts
✓ Perform LLM inference
✓ Return formatted answers
```

### **eda/visualizer.py** (Visualization System)
```python
✓ Distribution analysis (histograms, line charts)
✓ Relationship analysis (scatter plots, heatmaps)
✓ Categorical analysis (bar charts, pie charts)
✓ Correlation analysis (detailed heatmaps)
✓ Statistical summaries
```

### **utils/data_loader.py** (Data Utilities)
```python
✓ CSV file loading
✓ Data validation
✓ Type inference
```

---

## 🎓 Use Cases

1. **Data Scientists** - Quick EDA before modeling
2. **Business Analysts** - Explore datasets interactively
3. **Students** - Learn data analysis concepts
4. **Researchers** - Rapid data exploration
5. **Decision Makers** - Get insights without coding

---

## 🤖 AI Model Details

### **TinyLlama-1.1B-Chat-Q4_K_M**
- **Parameters**: 1.1 Billion (compact model)
- **Quantization**: Q4_K_M (8-bit quantized)
- **Size**: ~2.2GB
- **Speed**: Fast inference on CPU/GPU
- **Capability**: Chat and text generation
- **License**: Open source
- **No internet required**: Runs locally

---

## 📊 Example Questions

The chatbot can answer questions like:
- "What is the average value in the dataset?"
- "Which column has the most missing values?"
- "What patterns do you see in the data?"
- "Are there any outliers?"
- "What are the key correlations?"
- "How many unique values are in each column?"

---

## ⚙️ Configuration

### **Model Loading**
- GPU acceleration: Automatic fallback to CPU if unavailable
- Context size: 2048 tokens
- Temperature: 0.3 (for factual answers)
- Max tokens: 300 per response

### **Visualization**
- Auto-detects numeric vs categorical columns
- Handles missing values gracefully
- Responsive layout with tabs
- Caches data for performance

---

## 🚦 Performance Considerations

| Operation | Time | Notes |
|-----------|------|-------|
| App startup | ~5-10s | Model loading |
| CSV upload (1MB) | <1s | Pandas parsing |
| Visualizations | 2-5s | Matplotlib rendering |
| Q&A response | 10-30s | LLM inference |

---

## 🐛 Troubleshooting

### **Model not found**
```
Solution: Ensure TinyLlama model is in models/ directory
```

### **Slow performance**
```
Solution: Reduce dataset size or use GPU-enabled system
```

### **Memory issues**
```
Solution: Use smaller model or close other apps
```

---

## 📝 Future Enhancements

- [ ] Support for Excel files (.xlsx, .xls)
- [ ] Time series analysis
- [ ] Advanced statistical tests
- [ ] Data export (PDF reports)
- [ ] Custom chart creation
- [ ] Data preprocessing tools
- [ ] Predictive analytics
- [ ] Multi-file analysis

---

## 📄 License

Open Source Project

---

## 👨‍💻 Author

Created for automated data exploration and analysis

---

## 🤝 Support

For issues or questions, refer to the documentation or check the code comments.

---

**Made with ❤️ for Data Analysis** 📊
