import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np

# Professional color palette - Dark theme with neon accents
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'accent_cyan': '#00d9ff',
    'accent_teal': '#00f5dd',
    'accent_magenta': '#d946ef',
    'success': '#10b981',
    'danger': '#ef4444',
    'light': '#f3f4f6',
    'dark': '#0a0e27'
}

# Set professional dark style for matplotlib
plt.style.use('dark_background')
sns.set_palette("husl")
plt.rcParams['figure.facecolor'] = '#0a0e27'
plt.rcParams['axes.facecolor'] = '#111829'
plt.rcParams['axes.edgecolor'] = '#00d9ff'
plt.rcParams['grid.color'] = '#667eea'
plt.rcParams['grid.alpha'] = 0.1
plt.rcParams['text.color'] = '#ffffff'
plt.rcParams['xtick.color'] = '#ffffff'
plt.rcParams['ytick.color'] = '#ffffff'

def sanitize_label(label):
    """Escape special characters in labels for matplotlib mathtext rendering"""
    if not isinstance(label, str):
        label = str(label)
    # Escape special mathtext characters
    label = label.replace('$', r'\$')
    label = label.replace('^', r'\^')
    label = label.replace('_', r'\_')
    label = label.replace('\\', '\\\\')
    # Remove or replace other problematic characters
    label = label.replace('\x00', '')  # Null bytes
    # Keep only safe characters for display
    try:
        label.encode('utf-8')
    except UnicodeEncodeError:
        # Replace non-UTF8 characters
        label = label.encode('utf-8', 'replace').decode('utf-8')
    return label

def show_charts(df):
    """Display comprehensive data visualizations with error handling"""
    
    try:
        # Separate numeric and categorical columns
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        categorical_df = df.select_dtypes(include=['object'])
        
        # Create tabs for different visualization types
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📊 Distribution", 
            "🔗 Relationships", 
            "🏷️ Categorical", 
            "🔥 Correlation", 
            "📈 Summary", 
            "🎨 Advanced",
            "🔍 Data Quality"
        ])
        
        # TAB 1: Distribution Charts
        with tab1:
            st.markdown("### 📊 Distribution Analysis")
            
            if not numeric_df.empty:
                try:
                    col1, col2 = st.columns(2)
                    
                    # Histogram with KDE
                    with col1:
                        st.markdown("#### 📈 Histogram with KDE")
                        for col in numeric_df.columns[:2]:
                            try:
                                fig, ax = plt.subplots(figsize=(9, 5))
                                sns.histplot(numeric_df[col], kde=True, ax=ax, color=COLORS['accent_cyan'], alpha=0.7, edgecolor=COLORS['accent_magenta'], line_kws={'linewidth': 2})
                                ax.set_facecolor('#111829')
                                ax.grid(True, alpha=0.1, color=COLORS['primary'])
                                safe_col = sanitize_label(col)
                                ax.set_title(f"Distribution of {safe_col}", fontsize=12, fontweight='bold', color=COLORS['accent_cyan'])
                                ax.set_xlabel(safe_col, color=COLORS['accent_teal'])
                                ax.set_ylabel("Frequency", color=COLORS['accent_teal'])
                                st.pyplot(fig, use_container_width=True)
                                plt.close()
                            except Exception as e:
                                st.warning(f"Could not render histogram for {col}")
                    
                    # Line Chart
                    with col2:
                        st.markdown("#### 📉 Trend Analysis")
                        try:
                            fig, ax = plt.subplots(figsize=(9, 5))
                            for col in numeric_df.columns[:3]:
                                safe_col = sanitize_label(col)
                                ax.plot(numeric_df[col].values, label=safe_col, linewidth=2, marker='o', markersize=3)
                            ax.set_title("Data Trends", fontsize=12, fontweight='bold')
                            ax.set_xlabel("Index")
                            ax.set_ylabel("Value")
                            ax.legend(fontsize=9)
                            ax.grid(True, alpha=0.3)
                            st.pyplot(fig, use_container_width=True)
                            plt.close()
                        except Exception as e:
                            st.warning("Could not render trend chart")
                except Exception as e:
                    st.error(f"Distribution visualization error: {str(e)}")
            else:
                st.info("📭 No numeric columns found")
        
        # TAB 2: Relationships
        with tab2:
            st.markdown("### 🔗 Relationships Analysis")
            
            if len(numeric_df.columns) >= 2:
                try:
                    col1, col2 = st.columns(2)
                    
                    # Scatter Plot with gradient by value
                    with col1:
                        st.markdown("#### 📍 Scatter Plot (Color-Coded by Value)")
                        try:
                            x_col = numeric_df.columns[0]
                            y_col = numeric_df.columns[1]
                            fig, ax = plt.subplots(figsize=(9, 6))
                            # Use value magnitude for color intensity
                            values = numeric_df[y_col].values
                            scatter = ax.scatter(numeric_df[x_col], numeric_df[y_col], 
                                              c=values, cmap='coolwarm', alpha=0.7, s=100,
                                              edgecolors='white', linewidth=0.5)
                            cbar = plt.colorbar(scatter, ax=ax, label='Value Intensity')
                            cbar.set_label('Low → High', color=COLORS['accent_teal'], fontweight='bold')
                            safe_x = sanitize_label(x_col)
                            safe_y = sanitize_label(y_col)
                            ax.set_xlabel(safe_x, fontweight='bold', color=COLORS['accent_teal'])
                            ax.set_ylabel(safe_y, fontweight='bold', color=COLORS['accent_teal'])
                            ax.set_title(f"{safe_x} vs {safe_y}", fontsize=12, fontweight='bold', color=COLORS['accent_cyan'])
                            ax.set_facecolor('#111829')
                            ax.grid(True, alpha=0.1, color=COLORS['primary'])
                            st.pyplot(fig, use_container_width=True)
                            plt.close()
                        except Exception as e:
                            st.warning(f"Scatter plot error: {str(e)}")
                    
                    # Heatmap (Correlation) with gradient showing strong-weak
                    with col2:
                        st.markdown("#### 🔥 Correlation (Strong ↔ Weak)")
                        try:
                            fig, ax = plt.subplots(figsize=(9, 6))
                            corr_data = numeric_df.corr()
                            sns.heatmap(corr_data, annot=True, cmap="coolwarm", ax=ax, fmt='.2f', 
                                       cbar_kws={'label': 'Correlation'}, square=True, linewidths=1.5,
                                       linecolor='white', vmin=-1, vmax=1, annot_kws={'fontweight': 'bold'})
                            ax.set_facecolor('#111829')
                            ax.set_title("Strong → Weak Correlation", fontsize=12, fontweight='bold', color=COLORS['accent_cyan'])
                            ax.set_xticklabels(ax.get_xticklabels(), color=COLORS['accent_teal'], fontweight='bold', rotation=45, ha='right')
                            ax.set_yticklabels(ax.get_yticklabels(), color=COLORS['accent_teal'], fontweight='bold', rotation=0)
                            st.pyplot(fig, use_container_width=True)
                            plt.close()
                        except Exception as e:
                            st.warning(f"Correlation plot error: {str(e)}")
                except Exception as e:
                    st.error(f"Relationships visualization error: {str(e)}")
            else:
                st.info("📭 Need at least 2 numeric columns")
        
        # TAB 3: Categorical Analysis
        with tab3:
            st.markdown("### 🏷️ Categorical Analysis (High → Low Values)")
            
            if not categorical_df.empty:
                try:
                    for idx, col in enumerate(categorical_df.columns[:4]):
                        try:
                            fig, ax = plt.subplots(figsize=(10, 5))
                            top_vals = categorical_df[col].value_counts().head(10).sort_values(ascending=False)
                            # Create gradient from warm (high) to cool (low)
                            colors_list = plt.cm.coolwarm(np.linspace(0.95, 0.05, len(top_vals)))
                            bars = ax.bar(range(len(top_vals)), top_vals.values, color=colors_list, 
                                        edgecolor='white', linewidth=1.5, alpha=0.85)
                            # Add value labels on bars
                            for bar, val in zip(bars, top_vals.values):
                                height = bar.get_height()
                                ax.text(bar.get_x() + bar.get_width()/2., height,
                                       f'{int(val)}', ha='center', va='bottom', fontsize=9, 
                                       color=COLORS['accent_cyan'], fontweight='bold')
                            safe_col = sanitize_label(col)
                            ax.set_title(f"{safe_col} (Highest → Lowest)", fontsize=12, fontweight='bold', color=COLORS['accent_cyan'])
                            ax.set_xlabel(safe_col, color=COLORS['accent_teal'], fontweight='bold')
                            ax.set_ylabel("Count", color=COLORS['accent_teal'], fontweight='bold')
                            ax.set_xticks(range(len(top_vals)))
                            ax.set_xticklabels([str(x)[:15] for x in top_vals.index], rotation=45, ha='right', color=COLORS['accent_teal'])
                            ax.set_facecolor('#111829')
                            ax.tick_params(colors=COLORS['accent_teal'])
                            ax.grid(True, alpha=0.1, axis='y', color=COLORS['primary'])
                            st.pyplot(fig, use_container_width=True)
                            plt.close()
                        except Exception as e:
                            st.warning(f"Could not render chart for {col}")
                except Exception as e:
                    st.error(f"Categorical visualization error: {str(e)}")
            else:
                st.info("📭 No categorical columns found")
        
        # TAB 4: Detailed Correlation
        with tab4:
            st.markdown("### 🔥 Correlation Analysis (Strong to Weak)")
            
            if not numeric_df.empty and len(numeric_df.columns) > 1:
                try:
                    fig, ax = plt.subplots(figsize=(12, 9))
                    corr_matrix = numeric_df.corr()
                    # Use coolwarm to show strong positive (warm/red) to strong negative (cool/blue)
                    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax, fmt='.2f', 
                               square=True, linewidths=2, linecolor='white',
                               cbar_kws={'label': 'Correlation (-1 to +1)', 'shrink': 0.8},
                               vmin=-1, vmax=1, annot_kws={'fontsize': 10, 'fontweight': 'bold'})
                    ax.set_facecolor('#111829')
                    ax.set_title('Correlation Matrix - High ↔ Low Correlation', fontsize=13, fontweight='bold', color=COLORS['accent_cyan'], pad=20)
                    # Color the axis labels
                    ax.set_xticklabels(ax.get_xticklabels(), color=COLORS['accent_teal'], fontweight='bold', rotation=45, ha='right')
                    ax.set_yticklabels(ax.get_yticklabels(), color=COLORS['accent_teal'], fontweight='bold', rotation=0)
                    st.pyplot(fig, use_container_width=True)
                    plt.close()
                except Exception as e:
                    st.error(f"Correlation heatmap error: {str(e)}")
            else:
                st.warning("⚠️ Need at least 2 numeric columns")
        
        # TAB 5: Data Summary
        with tab5:
            st.markdown("### 📈 Data Summary Statistics")
            
            try:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Rows", len(df))
                with col2:
                    st.metric("Total Columns", len(df.columns))
                with col3:
                    st.metric("Missing Values", df.isnull().sum().sum())
                
                st.divider()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if not numeric_df.empty:
                        st.markdown("#### 🔢 Numeric Columns")
                        numeric_stats = numeric_df.describe().round(3)
                        st.dataframe(numeric_stats, use_container_width=True, height=300)
                
                with col2:
                    if not categorical_df.empty:
                        st.markdown("#### 🏷️ Categorical Columns")
                        for col in categorical_df.columns[:5]:
                            st.markdown(f"**{sanitize_label(col)}**")
                            st.write(f"Unique: {categorical_df[col].nunique()}")
                            st.write(f"Missing: {categorical_df[col].isnull().sum()}")
            except Exception as e:
                st.error(f"Summary statistics error: {str(e)}")
        
        # TAB 6: Advanced Visualizations
        with tab6:
            st.markdown("### 🎨 Advanced Visualizations")
            
            try:
                col1, col2 = st.columns(2)
                
                # Box Plot
                with col1:
                    st.markdown("#### 📦 Box Plot (Outliers)")
                    if not numeric_df.empty and len(numeric_df.columns) > 0:
                        try:
                            fig, ax = plt.subplots(figsize=(9, 5))
                            numeric_df.iloc[:, :min(3, len(numeric_df.columns))].boxplot(ax=ax, patch_artist=True)
                            for patch in ax.artists:
                                patch.set_facecolor(COLORS['primary'])
                                patch.set_alpha(0.7)
                            ax.set_title("Box Plot - Outlier Detection", fontsize=12, fontweight='bold')
                            ax.set_ylabel("Values")
                            st.pyplot(fig, use_container_width=True)
                            plt.close()
                        except Exception as e:
                            st.warning(f"Box plot error: {str(e)}")
                    else:
                        st.info("📭 No numeric data")
                
                # Violin Plot
                with col2:
                    st.markdown("#### 🎻 Distribution Plot")
                    if not numeric_df.empty and len(numeric_df.columns) > 0:
                        try:
                            fig, ax = plt.subplots(figsize=(9, 5))
                            col_to_plot = numeric_df.columns[0]
                            parts = ax.violinplot(numeric_df[col_to_plot].dropna().values, vert=True, showmeans=True, showmedians=True)
                            safe_col = sanitize_label(col_to_plot)
                            ax.set_title(f"Violin Plot - {safe_col}", fontsize=12, fontweight='bold')
                            ax.set_ylabel("Values")
                            st.pyplot(fig, use_container_width=True)
                            plt.close()
                        except Exception as e:
                            st.warning(f"Violin plot error: {str(e)}")
                    else:
                        st.info("📭 No numeric data")
            except Exception as e:
                st.error(f"Advanced visualization error: {str(e)}")
        
        # TAB 7: Data Quality Report
        with tab7:
            st.markdown("### 🔍 Data Quality Report")
            
            try:
                # Missing Values Analysis
                st.subheader("📭 Missing Values")
                missing = df.isnull().sum()
                if missing.sum() > 0:
                    missing_pct = (missing / len(df) * 100).round(2)
                    missing_df = pd.DataFrame({
                        'Column': missing.index,
                        'Missing Count': missing.values,
                        'Missing %': missing_pct.values
                    }).sort_values('Missing Count', ascending=False)
                    missing_df = missing_df[missing_df['Missing Count'] > 0]
                    
                    if not missing_df.empty:
                        fig, ax = plt.subplots(figsize=(10, 4))
                        ax.barh(missing_df['Column'], missing_df['Missing %'], color=COLORS['danger'])
                        ax.set_xlabel("Missing Percentage (%)")
                        ax.set_title("Missing Values by Column", fontsize=12, fontweight='bold')
                        st.pyplot(fig, use_container_width=True)
                        plt.close()
                        
                        st.dataframe(missing_df, use_container_width=True)
                    else:
                        st.success("✅ No missing values found!")
                else:
                    st.success("✅ No missing values found!")
                
                st.divider()
                
                # Data Type Summary
                st.subheader("📋 Data Types")
                dtype_summary = pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes.astype(str),
                    'Non-Null Count': df.count().values,
                    'Null Count': df.isnull().sum().values
                })
                st.dataframe(dtype_summary, use_container_width=True)
                
                st.divider()
                
                # Duplicate Rows
                st.subheader("🔄 Duplicates")
                duplicate_count = df.duplicated().sum()
                st.metric("Duplicate Rows", duplicate_count)
                
                if duplicate_count > 0:
                    st.info(f"⚠️ Found {duplicate_count} duplicate rows ({duplicate_count/len(df)*100:.2f}%)")
                else:
                    st.success("✅ No duplicate rows found!")
                
                st.divider()
                
                # Outliers Summary
                st.subheader("🎯 Outliers Summary")
                if not numeric_df.empty:
                    outlier_info = []
                    for col in numeric_df.columns:
                        Q1 = numeric_df[col].quantile(0.25)
                        Q3 = numeric_df[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        outliers = ((numeric_df[col] < lower_bound) | (numeric_df[col] > upper_bound)).sum()
                        outlier_info.append({
                            'Column': col,
                            'Outlier Count': outliers,
                            'Outlier %': f"{outliers/len(df)*100:.2f}%"
                        })
                    
                    outlier_df = pd.DataFrame(outlier_info)
                    st.dataframe(outlier_df, use_container_width=True)
                else:
                    st.info("📭 No numeric columns for outlier detection")
                    
            except Exception as e:
                st.error(f"Data quality report error: {str(e)}")
                
    except Exception as e:
        st.error(f"Error generating visualizations: {str(e)}")
        st.info("Please check your data and try again")
    
    # TAB 1: Distribution Charts
    with tab1:
        st.markdown("### 📊 Distribution Analysis")
        
        if not numeric_df.empty:
            col1, col2 = st.columns(2)
            
            # Histogram
            with col1:
                st.markdown("#### 📈 Histogram")
                for col in numeric_df.columns[:3]:  # Show first 3 numeric columns
                    try:
                        fig, ax = plt.subplots(figsize=(9, 5))
                        numeric_df[col].hist(bins=30, ax=ax, edgecolor='black', color=COLORS['primary'], alpha=0.8)
                        safe_col = sanitize_label(col)
                        ax.set_title(f"Distribution of {safe_col}", fontsize=14, fontweight='bold', pad=20)
                        ax.set_xlabel(safe_col, fontsize=11, fontweight='bold')
                        ax.set_ylabel("Frequency", fontsize=11, fontweight='bold')
                        ax.grid(True, alpha=0.3, linestyle='--')
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        st.pyplot(fig, use_container_width=True)
                        plt.close()
                    except Exception as e:
                        st.warning(f"Could not render histogram for {col}")
            
            # Line Chart
            with col2:
                st.markdown("#### 📉 Trend Analysis")
                try:
                    fig, ax = plt.subplots(figsize=(9, 5))
                    for col in numeric_df.columns[:3]:
                        safe_col = sanitize_label(col)
                        ax.plot(numeric_df[col].values, label=safe_col, linewidth=2.5, marker='o', markersize=4)
                    ax.set_title("Data Trends", fontsize=14, fontweight='bold', pad=20)
                    ax.set_xlabel("Index", fontsize=11, fontweight='bold')
                    ax.set_ylabel("Value", fontsize=11, fontweight='bold')
                    ax.legend(loc='best', fontsize=10)
                    ax.grid(True, alpha=0.3, linestyle='--')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    st.pyplot(fig, use_container_width=True)
                    plt.close()
                except Exception as e:
                    st.warning("Could not render trend chart")
    
    # TAB 2: Relationships
    with tab2:
        st.markdown("### 🔗 Relationships Analysis")
        
        if len(numeric_df.columns) >= 2:
            col1, col2 = st.columns(2)
            
            # Scatter Plot
            with col1:
                st.markdown("#### 📍 Scatter Plot")
                if len(numeric_df.columns) >= 2:
                    try:
                        x_col = numeric_df.columns[0]
                        y_col = numeric_df.columns[1]
                        fig, ax = plt.subplots(figsize=(9, 6))
                        ax.scatter(numeric_df[x_col], numeric_df[y_col], alpha=0.6, s=100, color=COLORS['secondary'], edgecolors='black', linewidth=0.5)
                        safe_x = sanitize_label(x_col)
                        safe_y = sanitize_label(y_col)
                        ax.set_xlabel(safe_x, fontsize=11, fontweight='bold')
                        ax.set_ylabel(safe_y, fontsize=11, fontweight='bold')
                        ax.set_title(f"{safe_x} vs {safe_y}", fontsize=14, fontweight='bold', pad=20)
                        ax.grid(True, alpha=0.3, linestyle='--')
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        st.pyplot(fig, use_container_width=True)
                        plt.close()
                    except Exception as e:
                        st.warning("Could not render scatter plot")
            
            # Heatmap (Correlation)
            with col2:
                st.markdown("#### 🔥 Correlation Matrix")
                if not numeric_df.empty:
                    try:
                        fig, ax = plt.subplots(figsize=(9, 6))
                        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax, fmt='.2f', 
                                   cbar_kws={'label': 'Correlation'}, square=True, linewidths=1, linecolor='white')
                        ax.set_title("Correlation Heatmap", fontsize=14, fontweight='bold', pad=20)
                        st.pyplot(fig, use_container_width=True)
                        plt.close()
                    except Exception as e:
                        st.warning("Could not render heatmap")
    
    # TAB 3: Categorical Analysis
    with tab3:
        st.markdown("### 🏷️ Categorical Analysis")
        
        if not categorical_df.empty:
            col1, col2 = st.columns(2)
            
            # Bar Chart
            with col1:
                st.markdown("#### 📊 Bar Chart")
                for col in categorical_df.columns[:2]:
                    try:
                        fig, ax = plt.subplots(figsize=(9, 5))
                        top_vals = categorical_df[col].value_counts().head(10)
                        bars = ax.bar(range(len(top_vals)), top_vals.values, color=COLORS['accent'], edgecolor='black', linewidth=1.5, alpha=0.85)
                        safe_col = sanitize_label(col)
                        ax.set_title(f"Bar Chart: {safe_col}", fontsize=14, fontweight='bold', pad=20)
                        ax.set_xlabel(safe_col, fontsize=11, fontweight='bold')
                        ax.set_ylabel("Count", fontsize=11, fontweight='bold')
                        ax.set_xticks(range(len(top_vals)))
                        ax.set_xticklabels([str(x)[:15] for x in top_vals.index], rotation=45, ha='right')
                        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        st.pyplot(fig, use_container_width=True)
                        plt.close()
                    except Exception as e:
                        st.warning(f"Could not render bar chart for {col}")
            
            # Pie Chart
            with col2:
                st.markdown("#### 🥧 Pie Chart")
                if len(categorical_df.columns) > 0:
                    try:
                        col_name = categorical_df.columns[0]
                        fig, ax = plt.subplots(figsize=(9, 6))
                        top_vals = categorical_df[col_name].value_counts().head(8)
                        colors_pie = plt.cm.Set3(np.linspace(0, 1, len(top_vals)))
                        wedges, texts, autotexts = ax.pie(top_vals.values, labels=[str(x)[:20] for x in top_vals.index], 
                                                           autopct='%1.1f%%', colors=colors_pie, startangle=90,
                                                           textprops={'fontsize': 10, 'fontweight': 'bold'})
                        safe_col_name = sanitize_label(col_name)
                        ax.set_title(f"Pie Chart: {safe_col_name}", fontsize=14, fontweight='bold', pad=20)
                        st.pyplot(fig, use_container_width=True)
                        plt.close()
                    except Exception as e:
                        st.warning("Could not render pie chart")
        else:
            st.info("📭 No categorical columns found in dataset")
    
    # TAB 4: Detailed Correlation
    with tab4:
        st.markdown("### 🔥 Correlation Analysis")
        
        if not numeric_df.empty:
            try:
                fig, ax = plt.subplots(figsize=(12, 9))
                corr_matrix = numeric_df.corr()
                sns.heatmap(corr_matrix, annot=True, cmap="RdYlGn", ax=ax, fmt='.2f', 
                           square=True, linewidths=2, linecolor='white', cbar_kws={'label': 'Correlation Coefficient'},
                           vmin=-1, vmax=1)
                ax.set_title('Correlation Matrix - All Numeric Columns', fontsize=14, fontweight='bold', pad=20)
                st.pyplot(fig, use_container_width=True)
                plt.close()
            except Exception as e:
                st.warning("Could not render correlation heatmap")
        else:
            st.warning("⚠️ No numeric columns for correlation analysis")
    
    # TAB 5: Data Summary
    with tab5:
        st.markdown("### 📈 Data Summary Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not numeric_df.empty:
                st.markdown("#### 🔢 Numeric Columns")
                numeric_stats = numeric_df.describe().round(2)
                st.dataframe(numeric_stats, use_container_width=True, height=300)
        
        with col2:
            if not categorical_df.empty:
                st.markdown("#### 🏷️ Categorical Columns")
                for col in categorical_df.columns[:5]:
                    st.markdown(f"**{sanitize_label(col)}**")
                    st.write(f"Unique: {categorical_df[col].nunique()}")
                    st.write(categorical_df[col].value_counts().head(3))
    
    # TAB 6: Advanced Visualizations
    with tab6:
        st.markdown("### 🎨 Advanced Visualizations")
        
        col1, col2 = st.columns(2)
        
        # Box Plot
        with col1:
            st.markdown("#### 📦 Box Plot (Outliers)")
            if not numeric_df.empty and len(numeric_df.columns) > 0:
                try:
                    fig, ax = plt.subplots(figsize=(9, 5))
                    numeric_df.iloc[:, :3].boxplot(ax=ax, patch_artist=True)
                    for patch in ax.artists:
                        patch.set_facecolor(COLORS['primary'])
                        patch.set_alpha(0.7)
                    ax.set_title("Box Plot - Outlier Detection", fontsize=14, fontweight='bold', pad=20)
                    ax.set_ylabel("Values", fontsize=11, fontweight='bold')
                    ax.grid(True, alpha=0.3, axis='y')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    st.pyplot(fig, use_container_width=True)
                    plt.close()
                except Exception as e:
                    st.info("📭 Box plot unavailable for this data")
        
        # Violin Plot
        with col2:
            st.markdown("#### 🎻 Violin Plot (Distribution)")
            if not numeric_df.empty and len(numeric_df.columns) > 0:
                try:
                    fig, ax = plt.subplots(figsize=(9, 5))
                    col_to_plot = numeric_df.columns[0]
                    parts = ax.violinplot(numeric_df[col_to_plot].dropna().values, vert=True, showmeans=True, showmedians=True)
                    safe_col = sanitize_label(col_to_plot)
                    ax.set_title(f"Violin Plot - {safe_col}", fontsize=14, fontweight='bold', pad=20)
                    ax.set_ylabel("Values", fontsize=11, fontweight='bold')
                    ax.grid(True, alpha=0.3, axis='y')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    st.pyplot(fig, use_container_width=True)
                    plt.close()
                except Exception as e:
                    st.info("📭 Violin plot unavailable")
        
        col3, col4 = st.columns(2)
        
        # KDE Plot (Density)
        with col3:
            st.markdown("#### 📊 KDE Plot (Density)")
            if not numeric_df.empty and len(numeric_df.columns) > 0:
                try:
                    fig, ax = plt.subplots(figsize=(9, 5))
                    for idx, col in enumerate(numeric_df.columns[:2]):
                        safe_col = sanitize_label(col)
                        numeric_df[col].plot(kind='density', ax=ax, label=safe_col, linewidth=2.5, color=COLORS['primary'] if idx == 0 else COLORS['secondary'])
                    ax.set_title("Kernel Density Estimation", fontsize=14, fontweight='bold', pad=20)
                    ax.legend(fontsize=10)
                    ax.grid(True, alpha=0.3)
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    st.pyplot(fig, use_container_width=True)
                    plt.close()
                except Exception as e:
                    st.info("📭 KDE plot unavailable")
        
        # Cumulative Distribution
        with col4:
            st.markdown("#### 📈 Cumulative Distribution")
            if not numeric_df.empty and len(numeric_df.columns) > 0:
                try:
                    fig, ax = plt.subplots(figsize=(9, 5))
                    for idx, col in enumerate(numeric_df.columns[:2]):
                        sorted_data = np.sort(numeric_df[col].dropna())
                        cumulative = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
                        safe_col = sanitize_label(col)
                        color = COLORS['primary'] if idx == 0 else COLORS['secondary']
                        ax.plot(sorted_data, cumulative, label=safe_col, linewidth=2.5, color=color)
                    ax.set_xlabel("Values", fontsize=11, fontweight='bold')
                    ax.set_ylabel("Cumulative Probability", fontsize=11, fontweight='bold')
                    ax.set_title("Cumulative Distribution Function", fontsize=14, fontweight='bold', pad=20)
                    ax.legend(fontsize=10)
                    ax.grid(True, alpha=0.3, linestyle='--')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    st.pyplot(fig, use_container_width=True)
                    plt.close()
                except Exception as e:
                    st.info("📭 CDF plot unavailable")


def show_simple_charts(df):
    """Simplified version for quick overview"""
    st.subheader("📊 Data Overview")
    
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    
    if not numeric_df.empty:
        st.line_chart(numeric_df.iloc[:, :3])

