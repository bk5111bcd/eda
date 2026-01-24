import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

def sanitize_label(label):
    """Escape special characters in labels for matplotlib mathtext rendering"""
    if not isinstance(label, str):
        label = str(label)
    label = label.replace('$', r'\$')
    label = label.replace('^', r'\^')
    label = label.replace('_', r'\_')
    label = label.replace('\\', '\\\\')
    label = label.replace('\x00', '')
    try:
        label.encode('utf-8')
    except UnicodeEncodeError:
        label = label.encode('utf-8', 'replace').decode('utf-8')
    return label

def show_complete_dashboard(df):
    """Display professional student performance dashboard"""
    
    # Add professional CSS styling
    st.markdown("""
    <style>
    .dashboard-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-top: 4px solid #667eea;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .dashboard-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
    }
    
    .stat-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .stat-label {
        font-size: 13px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    try:
        total_rows = len(df)
        total_cols = len(df.columns)
        missing_pct = (df.isnull().sum().sum() / (total_rows * total_cols) * 100) if (total_rows * total_cols) > 0 else 0
        duplicate_pct = (df.duplicated().sum() / total_rows * 100) if total_rows > 0 else 0
        
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return
    
    st.markdown("""
    <style>
    .dashboard-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
    }
    .dashboard-header h1 {
        margin: 0;
        font-size: 32px;
    }
    .dashboard-header p {
        margin: 5px 0 0 0;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='dashboard-header'>
        <h1>📊 Data Analysis Dashboard</h1>
        <p>Comprehensive dataset overview and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 📈 Key Metrics")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">📊 Total Records</div>
            <div class="stat-value">{total_rows:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">🔢 Features</div>
            <div class="stat-value">{total_cols}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">✅ Data Quality</div>
            <div class="stat-value">{100-missing_pct:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi4:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">🔁 Duplicates</div>
            <div class="stat-value">{duplicate_pct:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("#### 📋 Column Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📊 Column Type Breakdown")
        col_info = pd.DataFrame({
            'Type': ['Numeric', 'Categorical'],
            'Count': [len(numeric_cols), len(categorical_cols)]
        })
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#667eea', '#764ba2']
        bars = ax.bar(col_info['Type'], col_info['Count'], color=colors, edgecolor='#2c3e50', linewidth=2, alpha=0.85)
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax.set_title('Data Type Distribution', fontsize=13, fontweight='bold', pad=15)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.3, axis='y')
        st.pyplot(fig, use_container_width=True)
        plt.close()
    
    with col2:
        st.markdown("##### ✨ Data Quality Metrics")
        quality_metrics = pd.DataFrame({
            'Metric': ['✅ Complete', '⚠️ Missing', '🔁 Duplicate', '✓ Unique'],
            'Value': [
                f"{100-missing_pct:.1f}%",
                f"{missing_pct:.1f}%",
                f"{duplicate_pct:.1f}%",
                f"{100-duplicate_pct:.1f}%"
            ]
        })
        st.dataframe(quality_metrics, use_container_width=True, hide_index=True)
    
    st.divider()
    
    if numeric_cols:
        st.markdown("#### 📊 Numeric Columns Analysis")
        
        numeric_stats = df[numeric_cols].describe().T[['count', 'mean', 'std', 'min', 'max']]
        numeric_stats.columns = ['Count', 'Mean', 'Std Dev', 'Min', 'Max']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📈 Statistical Summary")
            st.dataframe(numeric_stats.style.format('{:.2f}'), use_container_width=True, height=300)
        
        with col2:
            st.markdown("##### 📉 Distribution Overview")
            try:
                fig, axes = plt.subplots(min(3, len(numeric_cols)), 1, figsize=(9, 10))
                
                if len(numeric_cols) == 1:
                    axes = [axes]
                
                for idx, col in enumerate(numeric_cols[:3]):
                    if idx < len(axes):
                        axes[idx].hist(df[col].dropna(), bins=30, color='#667eea', edgecolor='#2c3e50', alpha=0.8)
                        safe_col = sanitize_label(col)
                        axes[idx].set_title(f'{safe_col}', fontsize=11, fontweight='bold')
                        axes[idx].set_xlabel('Value', fontsize=10)
                        axes[idx].set_ylabel('Frequency', fontsize=10)
                        axes[idx].spines['top'].set_visible(False)
                        axes[idx].spines['right'].set_visible(False)
                        axes[idx].grid(True, alpha=0.3, axis='y')
                
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close()
            except Exception as e:
                st.warning("Could not render distribution charts")
        
        st.divider()
    
    if categorical_cols:
        st.markdown("#### 🏷️ Categorical Columns Analysis")
        
        cat_info = []
        for col in categorical_cols:
            cat_info.append({
                'Column': sanitize_label(col),
                'Unique': df[col].nunique(),
                'Top Value': str(df[col].value_counts().index[0])[:30] if len(df[col].value_counts()) > 0 else 'N/A',
                'Missing': df[col].isnull().sum()
            })
        
        cat_df = pd.DataFrame(cat_info)
        st.dataframe(cat_df, use_container_width=True, hide_index=True)
        
        st.markdown("##### 📊 Top Category Values")
        col1, col2 = st.columns(2)
        
        for idx, col in enumerate(categorical_cols[:2]):
            plot_col = col1 if idx == 0 else col2
            
            with plot_col:
                try:
                    fig, ax = plt.subplots(figsize=(9, 5))
                    top_categories = df[col].value_counts().head(8)
                    colors = plt.cm.Set3(np.linspace(0, 1, len(top_categories)))
                    bars = ax.barh(range(len(top_categories)), top_categories.values, color=colors, edgecolor='#2c3e50', linewidth=1.5)
                    ax.set_yticks(range(len(top_categories)))
                    ax.set_yticklabels([str(x)[:20] for x in top_categories.index], fontsize=10)
                    ax.set_xlabel('Count', fontweight='bold', fontsize=11)
                    safe_col = sanitize_label(col)
                    ax.set_title(f'Top Categories - {safe_col}', fontweight='bold', fontsize=12, pad=15)
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.grid(True, alpha=0.3, axis='x')
                    st.pyplot(fig, use_container_width=True)
                    plt.close()
                except Exception as e:
                    st.warning(f"Could not render chart for {col}")
            
            with plot_col:
                try:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    top_categories = df[col].value_counts().head(8)
                    colors = plt.cm.Set2(np.linspace(0, 1, len(top_categories)))
                    top_categories.plot(kind='barh', ax=ax, color=colors, edgecolor='#2c3e50', linewidth=1.5)
                    ax.set_xlabel('Count', fontweight='bold')
                    safe_col = sanitize_label(col)
                    ax.set_title(f'Top Categories - {safe_col}', fontweight='bold')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    st.pyplot(fig, use_container_width=True)
                    plt.close()
                except:
                    st.write("Chart unavailable")
        
        st.divider()
    
    if len(numeric_cols) > 1:
        st.markdown("### 🔗 Correlation Analysis")
        
        try:
            corr_matrix = df[numeric_cols].corr()
            
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                       square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                       ax=ax, vmin=-1, vmax=1)
            ax.set_title('Correlation Matrix', fontsize=12, fontweight='bold', pad=20)
            st.pyplot(fig, use_container_width=True)
            plt.close()
        except Exception as e:
            st.warning(f"Could not generate correlation matrix: {str(e)}")
        
        st.divider()
    
    st.markdown("### 👁️ Data Preview")
    
    tab1, tab2, tab3, tab4 = st.tabs(["First Rows", "Last Rows", "Random Sample", "Full Info"])
    
    with tab1:
        st.dataframe(df.head(10), use_container_width=True, height=400)
    
    with tab2:
        st.dataframe(df.tail(10), use_container_width=True, height=400)
    
    with tab3:
        sample_size = min(10, len(df))
        st.dataframe(df.sample(n=sample_size), use_container_width=True, height=400)
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Dataset Dimensions**")
            st.write(f"• Rows: **{total_rows:,}**")
            st.write(f"• Columns: **{total_cols}**")
            st.write(f"• Total Cells: **{total_rows * total_cols:,}**")
            st.write(f"• Memory: **{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB**")
        
        with col2:
            st.markdown("**Data Characteristics**")
            st.write(f"• Numeric Columns: **{len(numeric_cols)}**")
            st.write(f"• Categorical Columns: **{len(categorical_cols)}**")
            st.write(f"• Missing Data: **{missing_pct:.2f}%**")
            st.write(f"• Duplicate Rows: **{duplicate_pct:.2f}%**")
    
    st.divider()
    
    st.markdown("### 🔍 Detailed Column Information")
    
    col_details = pd.DataFrame({
        'Column': df.columns,
        'Type': df.dtypes.astype(str),
        'Non-Null': df.count().values,
        'Null': df.isnull().sum().values,
        'Unique': [df[col].nunique() for col in df.columns]
    })
    
    st.dataframe(col_details, use_container_width=True, height=400)
    
    st.divider()
    
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d; font-size: 12px; padding: 20px;'>
        <p>Dashboard generated on """ + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        <p>Ready for analysis and insights!</p>
    </div>
    """, unsafe_allow_html=True)

show_dashboard = show_complete_dashboard
