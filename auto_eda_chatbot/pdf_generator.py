"""
PDF Report Generation Module
Creates comprehensive EDA reports as PDF
"""

from fpdf import FPDF
from datetime import datetime
import io
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class EDAPDFReport(FPDF):
    """Custom PDF class for EDA reports"""
    
    def __init__(self, title="Auto EDA Report", username="User"):
        super().__init__()
        self.title = title
        self.username = username
        self.page_count = 0
        
    def header(self):
        """Header for each page"""
        # Logo/Title
        self.set_font("Arial", "B", 20)
        self.set_text_color(102, 126, 234)  # Primary blue
        self.cell(0, 10, "Auto EDA Report", 0, 1, "C")
        self.set_text_color(0, 0, 0)
        
        # Divider
        self.set_draw_color(102, 126, 234)
        self.line(10, 20, 200, 20)
        self.ln(5)
    
    def footer(self):
        """Footer for each page"""
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()} | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 0, "C")
    
    def add_title_page(self, dataset_name="", rows=0, cols=0):
        """Add title/cover page"""
        self.add_page()
        
        # Spacing
        self.ln(30)
        
        # Main title
        self.set_font("Arial", "B", 28)
        self.set_text_color(102, 126, 234)
        self.multi_cell(0, 10, "Auto EDA Report", align="C")
        
        # Subtitle
        self.set_font("Arial", "", 14)
        self.set_text_color(100, 100, 100)
        self.ln(10)
        self.multi_cell(0, 6, f"Exploratory Data Analysis: {dataset_name}", align="C")
        
        # Divider
        self.set_draw_color(200, 200, 200)
        self.ln(10)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(15)
        
        # Report details
        self.set_font("Arial", "", 11)
        self.set_text_color(0, 0, 0)
        details = [
            f"Analyst: {self.username}",
            f"Date: {datetime.now().strftime('%B %d, %Y')}",
            f"Time: {datetime.now().strftime('%H:%M:%S')}",
            f"Dataset Rows: {rows:,}",
            f"Dataset Columns: {cols}"
        ]
        
        for detail in details:
            self.cell(0, 8, detail, 0, 1, "L")
        
        # Divider at bottom
        self.ln(20)
        self.set_draw_color(200, 200, 200)
        self.line(20, self.get_y(), 190, self.get_y())
        
        # Footer message
        self.ln(40)
        self.set_font("Arial", "I", 9)
        self.set_text_color(150, 150, 150)
        self.multi_cell(0, 5, "This report contains comprehensive exploratory data analysis, visualizations, and insights derived from the uploaded dataset.", align="C")

    def add_section(self, title, content=""):
        """Add a new section"""
        self.add_page()
        
        # Section title
        self.set_font("Arial", "B", 16)
        self.set_text_color(102, 126, 234)
        self.cell(0, 10, title, 0, 1)
        
        # Divider
        self.set_draw_color(102, 126, 234)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
        
        # Content
        if content:
            self.set_font("Arial", "", 10)
            self.set_text_color(0, 0, 0)
            self.multi_cell(0, 5, content)
        
        self.ln(2)

    def add_statistics_table(self, df_stats):
        """Add statistics table to PDF"""
        self.set_font("Arial", "B", 11)
        self.set_text_color(102, 126, 234)
        self.cell(0, 8, "Statistical Summary", 0, 1)
        self.ln(2)
        
        # Table header
        self.set_font("Arial", "B", 9)
        self.set_fill_color(230, 230, 250)  # Light blue
        
        col_width = 38
        self.cell(col_width, 6, "Column", 1, 0, "C", True)
        self.cell(col_width, 6, "Type", 1, 0, "C", True)
        self.cell(col_width, 6, "Non-Null", 1, 0, "C", True)
        self.cell(col_width, 6, "Missing", 1, 1, "C", True)
        
        # Table rows
        self.set_font("Arial", "", 8)
        self.set_text_color(0, 0, 0)
        
        for idx, row in df_stats.iterrows():
            col = str(row.get("Column", ""))[:20]
            dtype = str(row.get("Type", ""))[:10]
            non_null = str(row.get("Non-Null Count", "0"))[:8]
            missing = str(row.get("Null Count", "0"))[:8]
            
            self.cell(col_width, 5, col, 1, 0)
            self.cell(col_width, 5, dtype, 1, 0)
            self.cell(col_width, 5, non_null, 1, 0)
            self.cell(col_width, 5, missing, 1, 1)
        
        self.ln(3)

    def add_insights(self, insights_list):
        """Add key insights section"""
        self.set_font("Arial", "B", 11)
        self.set_text_color(102, 126, 234)
        self.cell(0, 8, "Key Insights", 0, 1)
        self.ln(2)
        
        self.set_font("Arial", "", 9)
        self.set_text_color(0, 0, 0)
        
        for i, insight in enumerate(insights_list, 1):
            self.cell(5, 5, f"-", 0, 0)
            self.multi_cell(0, 5, insight)
            self.ln(1)

    def add_image(self, img_path, x=10, y=None, w=190):
        """Add image to PDF"""
        try:
            if y is None:
                y = self.get_y()
            self.image(img_path, x=x, y=y, w=w)
            self.ln(5)
        except:
            pass

def generate_histogram(df, column):
    """Generate histogram for a numeric column"""
    try:
        fig, ax = plt.subplots(figsize=(8, 5))
        # Use gradient from cyan to magenta
        n, bins, patches = ax.hist(df[column].dropna(), bins=20, edgecolor='white', linewidth=0.5, alpha=0.85)
        # Color bars with gradient from low to high
        cm = plt.cm.coolwarm
        for i, patch in enumerate(patches):
            patch.set_facecolor(cm(i/len(patches)))
        ax.set_title(f"Distribution of {column} (Low → High)", fontsize=11, fontweight='bold', color='#00d9ff')
        ax.set_xlabel(column, color='#00f5dd', fontweight='bold')
        ax.set_ylabel("Frequency", color='#00f5dd', fontweight='bold')
        ax.set_facecolor('#111829')
        ax.tick_params(colors='#00f5dd')
        ax.grid(True, alpha=0.1, color='#667eea')
        
        # Save to BytesIO
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png', bbox_inches='tight', dpi=100, facecolor='#0a0e27', edgecolor='none')
        img_bytes.seek(0)
        plt.close(fig)
        return img_bytes
    except Exception as e:
        return None

def generate_correlation_heatmap(df):
    """Generate correlation heatmap for numeric columns"""
    try:
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        if numeric_df.empty or numeric_df.shape[1] < 2:
            return None
        
        fig, ax = plt.subplots(figsize=(8, 6))
        corr_matrix = numeric_df.corr()
        # Use coolwarm to show strong positive (red/warm) to strong negative (blue/cool)
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax, 
                    cbar_kws={'label': 'Strong → Weak'}, vmin=-1, vmax=1,
                    linewidths=1.5, linecolor='white', annot_kws={'fontweight': 'bold', 'fontsize': 9})
        ax.set_facecolor('#111829')
        ax.set_title("Correlation Matrix (High ↔ Low)", fontsize=11, fontweight='bold', color='#00d9ff')
        ax.tick_params(colors='#00f5dd')
        
        # Save to BytesIO
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png', bbox_inches='tight', dpi=100, facecolor='#0a0e27', edgecolor='none')
        img_bytes.seek(0)
        plt.close(fig)
        return img_bytes
    except Exception as e:
        return None

def generate_categorical_chart(df, column):
    """Generate bar chart for categorical column with high-low gradient"""
    try:
        fig, ax = plt.subplots(figsize=(8, 5))
        value_counts = df[column].value_counts().head(10).sort_values(ascending=False)
        # Create gradient from warm (high) to cool (low)
        colors_list = plt.cm.coolwarm(np.linspace(0.95, 0.05, len(value_counts)))
        bars = ax.barh(range(len(value_counts)), value_counts.values, color=colors_list, edgecolor='white', linewidth=1.5, alpha=0.85)
        # Add value labels
        for bar, val in zip(bars, value_counts.values):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2., f' {int(val)}',
                   ha='left', va='center', fontsize=9, color='#00d9ff', fontweight='bold')
        ax.set_yticks(range(len(value_counts)))
        ax.set_yticklabels(value_counts.index, color='#00f5dd', fontweight='bold')
        ax.set_facecolor('#111829')
        ax.tick_params(colors='#00f5dd')
        ax.set_title(f"{column} Distribution (High → Low)", fontsize=11, fontweight='bold', color='#00d9ff')
        ax.set_xlabel("Count", fontweight='bold', color='#00f5dd')
        ax.grid(True, alpha=0.1, axis='x', color='#667eea')
        
        # Save to BytesIO
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png', bbox_inches='tight', dpi=100, facecolor='#0a0e27', edgecolor='none')
        img_bytes.seek(0)
        plt.close(fig)
        return img_bytes
    except Exception as e:
        return None

def generate_pdf_report(df, username="User", dataset_name="Dataset"):
    """Generate complete PDF report for the dataset"""
    
    pdf = EDAPDFReport(username=username)
    
    # Title page
    pdf.add_title_page(
        dataset_name=dataset_name,
        rows=len(df),
        cols=len(df.columns)
    )
    
    # Dataset Overview
    pdf.add_section("Dataset Overview")
    overview_text = f"""
    Dataset Name: {dataset_name}
    Total Records: {len(df):,}
    Total Columns: {len(df.columns)}
    Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
    
    This section provides comprehensive information about your dataset structure and contents.
    """
    pdf.multi_cell(0, 5, overview_text)
    
    # Statistics
    pdf.add_section("Data Quality Report")
    
    dtype_summary = pd.DataFrame({
        'Column': df.columns,
        'Type': df.dtypes.astype(str),
        'Non-Null Count': df.count().values,
        'Null Count': df.isnull().sum().values
    })
    pdf.add_statistics_table(dtype_summary)
    
    # Key insights
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    insights = [
        f"Numeric Columns: {len(numeric_cols)} ({', '.join(numeric_cols[:3])}{'...' if len(numeric_cols) > 3 else ''})",
        f"Categorical Columns: {len(categorical_cols)} ({', '.join(categorical_cols[:3])}{'...' if len(categorical_cols) > 3 else ''})",
        f"Missing Values: {df.isnull().sum().sum()} ({df.isnull().sum().sum()/len(df)/len(df.columns)*100:.2f}% of dataset)",
        f"Duplicate Rows: {df.duplicated().sum()} ({df.duplicated().sum()/len(df)*100:.2f}% of dataset)",
        f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
    ]
    pdf.add_insights(insights)
    
    # Numeric Summary
    if not df.select_dtypes(include=['float64', 'int64']).empty:
        pdf.add_section("Numeric Column Summary")
        numeric_stats = df.describe().round(3).T
        numeric_stats['Column'] = numeric_stats.index
        numeric_stats = numeric_stats[['Column', 'count', 'mean', 'std', 'min', 'max']]
        
        pdf.set_font("Arial", "B", 9)
        pdf.set_fill_color(230, 230, 250)
        pdf.cell(35, 6, "Column", 1, 0, "C", True)
        pdf.cell(25, 6, "Count", 1, 0, "C", True)
        pdf.cell(30, 6, "Mean", 1, 0, "C", True)
        pdf.cell(30, 6, "Std Dev", 1, 0, "C", True)
        pdf.cell(25, 6, "Min", 1, 0, "C", True)
        pdf.cell(35, 6, "Max", 1, 1, "C", True)
        
        pdf.set_font("Arial", "", 8)
        for idx, row in numeric_stats.iterrows():
            pdf.cell(35, 5, str(row['Column'])[:15], 1, 0)
            pdf.cell(25, 5, f"{row['count']:.0f}", 1, 0)
            pdf.cell(30, 5, f"{row['mean']:.2f}", 1, 0)
            pdf.cell(30, 5, f"{row['std']:.2f}", 1, 0)
            pdf.cell(25, 5, f"{row['min']:.2f}", 1, 0)
            pdf.cell(35, 5, f"{row['max']:.2f}", 1, 1)
    
    # Categorical Summary
    if not df.select_dtypes(include=['object']).empty:
        pdf.add_section("Categorical Column Summary")
        cat_info = []
        for col in df.select_dtypes(include=['object']).columns[:5]:
            cat_info.append(f"- {col}: {df[col].nunique()} unique values")
        
        for info in cat_info:
            pdf.cell(0, 5, info, 0, 1)
    
    # VISUALIZATION SECTION
    pdf.add_page()
    pdf.add_section("Visualizations")
    
    # Numeric distributions
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if numeric_cols:
        pdf.ln(3)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, "Numeric Distributions", 0, 1)
        pdf.ln(2)
        
        for i, col in enumerate(numeric_cols[:3]):  # Limit to 3 distributions
            img_bytes = generate_histogram(df, col)
            if img_bytes:
                pdf.set_xy(10, pdf.get_y())
                pdf.image(img_bytes, x=10, y=None, w=190)
                pdf.ln(5)
    
    # Correlation heatmap
    if len(numeric_cols) > 1:
        pdf.add_page()
        pdf.add_section("Correlation Analysis")
        img_bytes = generate_correlation_heatmap(df)
        if img_bytes:
            pdf.set_xy(10, pdf.get_y())
            pdf.image(img_bytes, x=10, y=None, w=190)
            pdf.ln(5)
    
    # Categorical visualizations
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    if categorical_cols:
        pdf.add_page()
        pdf.add_section("Categorical Analysis")
        
        for i, col in enumerate(categorical_cols[:2]):  # Limit to 2 categorical charts
            img_bytes = generate_categorical_chart(df, col)
            if img_bytes:
                pdf.set_xy(10, pdf.get_y())
                pdf.image(img_bytes, x=10, y=None, w=190)
                pdf.ln(5)
    
    return pdf

def get_pdf_bytes(pdf):
    """Get PDF as bytes for download"""
    pdf_bytes = pdf.output()
    if isinstance(pdf_bytes, bytearray):
        pdf_bytes = bytes(pdf_bytes)
    return pdf_bytes
