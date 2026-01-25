import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import professional color palette
from .eda_palette import EDAPalette, EDAPaletteConfigurator
from .advanced_charts import (create_area_chart, create_column_chart, create_doughnut_chart,
                              create_bubble_chart, create_radar_chart, create_stacked_bar_chart,
                              create_gauge_chart, create_comparison_chart, create_line_area_combination)
from utils.ui import show_chart, show_chart_wide, show_chart_square

# Auto-configure matplotlib with professional palette
EDAPaletteConfigurator.apply_dark_theme()

# Set futuristic dark style for matplotlib - High quality rendering
# (Already configured by EDAPaletteConfigurator.apply_dark_theme() above)

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
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📊 Distribution", 
            "🔗 Relationships", 
            "🏷️ Categorical", 
            "🔥 Correlation", 
            "📈 Summary", 
            "🎨 Advanced",
            "🌈 Extended Charts",
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
                        st.markdown("#### 📈 Histogram")
                        for col in numeric_df.columns[:2]:
                            try:
                                fig, ax = plt.subplots(figsize=(5, 3))
                                col_data = numeric_df[col].dropna()
                                
                                if len(col_data) < 2:
                                    continue
                                
                                # Create histogram with gradient color
                                n, bins, patches = ax.hist(col_data, bins=30, alpha=0.8, edgecolor='#00d9ff', linewidth=1.5)
                                
                                # Apply neon plasma gradient
                                cm = plt.cm.get_cmap('plasma')
                                for i, patch in enumerate(patches):
                                    patch.set_facecolor(cm(i/len(patches)))
                                    patch.set_alpha(0.85)
                                
                                # Add KDE curve if possible
                                try:
                                    from scipy.stats import gaussian_kde
                                    if len(col_data) > 1:
                                        density = gaussian_kde(col_data)
                                        xs = np.linspace(col_data.min(), col_data.max(), 200)
                                        kde_values = density(xs) * len(col_data) * (bins[1]-bins[0])
                                        ax.plot(xs, kde_values, color='#00d9ff', linewidth=3, label='KDE', alpha=0.9)
                                except:
                                    pass
                                
                                ax.set_facecolor('#111829')
                                ax.grid(True, alpha=0.15, color='#667eea', linestyle='--')
                                ax.set_axisbelow(True)
                                safe_col = sanitize_label(col)
                                ax.set_title(f"Distribution of {safe_col}", fontsize=13, fontweight='bold', color='#00d9ff', pad=15)
                                ax.set_xlabel(safe_col, color='#00d9ff', fontweight='bold', fontsize=11)
                                ax.set_ylabel("Frequency", color='#00d9ff', fontweight='bold', fontsize=11)
                                
                                # Only show legend if there's content
                                handles, labels = ax.get_legend_handles_labels()
                                if handles:
                                    ax.legend(fontsize=10, loc='upper right', framealpha=0.9)
                                
                                # Style spines
                                for spine in ax.spines.values():
                                    spine.set_edgecolor('#00d9ff')
                                    spine.set_linewidth(1.5)
                                    spine.set_alpha(0.3)
                                
                                show_chart(fig)
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
                            show_chart(fig)
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
                        st.markdown("#### 📍 Scatter Plot (Neon Gradient)")
                        try:
                            x_col = numeric_df.columns[0]
                            y_col = numeric_df.columns[1]
                            fig, ax = plt.subplots(figsize=(5, 3.5))
                            
                            # Use value magnitude for color intensity with neon gradient
                            values = numeric_df[y_col].values
                            scatter = ax.scatter(numeric_df[x_col], numeric_df[y_col], 
                                              c=values, cmap='twilight', alpha=0.8, s=120,
                                              edgecolors='#00d9ff', linewidth=1, vmin=values.min(), vmax=values.max())
                            
                            cbar = plt.colorbar(scatter, ax=ax)
                            cbar.set_label('Value Intensity', color='#00d9ff', fontweight='bold', fontsize=10)
                            cbar.ax.tick_params(colors='#00d9ff', labelsize=9)
                            
                            safe_x = sanitize_label(x_col)
                            safe_y = sanitize_label(y_col)
                            ax.set_xlabel(safe_x, fontweight='bold', color='#00d9ff', fontsize=11)
                            ax.set_ylabel(safe_y, fontweight='bold', color='#00d9ff', fontsize=11)
                            ax.set_title(f"{safe_x} vs {safe_y}", fontsize=13, fontweight='bold', color='#00d9ff', pad=15)
                            ax.set_facecolor('#111829')
                            ax.grid(True, alpha=0.15, color='#667eea', linestyle='--')
                            ax.set_axisbelow(True)
                            
                            # Enhance spines
                            for spine in ax.spines.values():
                                spine.set_edgecolor('#00d9ff')
                                spine.set_linewidth(1.5)
                                spine.set_alpha(0.3)
                            
                            show_chart(fig)
                            plt.close()
                        except Exception as e:
                            st.warning(f"Scatter plot error: {str(e)}")
                    
                    # Heatmap (Correlation) with gradient showing strong-weak
                    with col2:
                        st.markdown("#### 🔥 Correlation (Strong ↔ Weak)")
                        try:
                            fig, ax = plt.subplots(figsize=(5, 4))
                            corr_data = numeric_df.corr()
                            
                            # Create custom neon colormap
                            sns.heatmap(corr_data, annot=True, cmap="coolwarm", ax=ax, fmt='.2f', 
                                       cbar_kws={'label': 'Correlation', 'shrink': 0.8},
                                       square=True, linewidths=2, linecolor='#111829',
                                       vmin=-1, vmax=1, annot_kws={'fontweight': 'bold', 'fontsize': 10, 'color': 'white'})
                            
                            ax.set_facecolor('#111829')
                            ax.set_title("Correlation Matrix - Strong → Weak", fontsize=13, fontweight='bold', color='#00d9ff', pad=15)
                            ax.set_xticklabels(ax.get_xticklabels(), color='#00d9ff', fontweight='bold', rotation=45, ha='right', fontsize=10)
                            ax.set_yticklabels(ax.get_yticklabels(), color='#00d9ff', fontweight='bold', rotation=0, fontsize=10)
                            
                            # Enhance colorbar
                            cbar = ax.collections[0].colorbar
                            cbar.ax.tick_params(colors='#00d9ff', labelsize=9)
                            cbar.set_label('Correlation', color='#00d9ff', fontweight='bold', fontsize=10)
                            
                            show_chart(fig)
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
                            fig, ax = plt.subplots(figsize=(5, 3.5))
                            top_vals = categorical_df[col].value_counts().head(10).sort_values(ascending=False)
                            
                            # Create neon gradient from cyan to magenta
                            n_bars = len(top_vals)
                            colors_list = []
                            for i in range(n_bars):
                                # Interpolate between cyan and magenta
                                ratio = i / max(n_bars - 1, 1)
                                r = int(0 + (217 - 0) * ratio)  # 0 to 217
                                g = int(217 + (70 - 217) * ratio)  # 217 to 70
                                b = int(255 + (239 - 255) * ratio)  # 255 to 239
                                colors_list.append(f'#{r:02x}{g:02x}{b:02x}')
                            
                            bars = ax.bar(range(len(top_vals)), top_vals.values, color=colors_list, 
                                        edgecolor='#00d9ff', linewidth=2, alpha=0.9, width=0.7)
                            
                            # Add value labels on bars with glow effect
                            for bar, val in zip(bars, top_vals.values):
                                height = bar.get_height()
                                ax.text(bar.get_x() + bar.get_width()/2., height,
                                       f'{int(val)}', ha='center', va='bottom', fontsize=10, 
                                       color='#00d9ff', fontweight='bold',
                                       bbox=dict(boxstyle='round,pad=0.3', facecolor='#111829', edgecolor='#00d9ff', alpha=0.7, linewidth=1))
                            
                            safe_col = sanitize_label(col)
                            ax.set_title(f"{safe_col} (Highest → Lowest)", fontsize=13, fontweight='bold', color='#00d9ff', pad=15)
                            ax.set_xlabel(safe_col, color='#00d9ff', fontweight='bold', fontsize=11)
                            ax.set_ylabel("Count", color='#00d9ff', fontweight='bold', fontsize=11)
                            ax.set_xticks(range(len(top_vals)))
                            ax.set_xticklabels([str(x)[:15] for x in top_vals.index], rotation=45, ha='right', color='#00d9ff', fontsize=10)
                            ax.set_facecolor('#111829')
                            ax.tick_params(colors='#00d9ff', labelsize=10)
                            ax.grid(True, alpha=0.15, axis='y', color='#667eea', linestyle='--')
                            ax.set_axisbelow(True)
                            
                            # Enhance spines
                            for spine in ax.spines.values():
                                spine.set_edgecolor('#00d9ff')
                                spine.set_linewidth(1.5)
                                spine.set_alpha(0.3)
                            
                            show_chart(fig)
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
                    fig, ax = plt.subplots(figsize=(6, 5))
                    corr_matrix = numeric_df.corr()
                    # Use coolwarm to show strong positive (warm/red) to strong negative (cool/blue)
                    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax, fmt='.2f', 
                               square=True, linewidths=2.5, linecolor='#111829',
                               cbar_kws={'label': 'Correlation (-1 to +1)', 'shrink': 0.85},
                               vmin=-1, vmax=1, annot_kws={'fontsize': 11, 'fontweight': 'bold', 'color': 'white'})
                    
                    ax.set_facecolor('#111829')
                    ax.set_title('Correlation Matrix - High ↔ Low Correlation', fontsize=14, fontweight='bold', 
                                color='#00d9ff', pad=20)
                    
                    # Color the axis labels with neon
                    ax.set_xticklabels(ax.get_xticklabels(), color='#00d9ff', fontweight='bold', 
                                      rotation=45, ha='right', fontsize=11)
                    ax.set_yticklabels(ax.get_yticklabels(), color='#00d9ff', fontweight='bold', 
                                      rotation=0, fontsize=11)
                    
                    # Enhance colorbar
                    cbar = ax.collections[0].colorbar
                    cbar.ax.tick_params(colors='#00d9ff', labelsize=10)
                    cbar.set_label('Correlation', color='#00d9ff', fontweight='bold', fontsize=11)
                    
                    show_chart(fig)
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
                            fig, ax = plt.subplots(figsize=(5, 3.5))
                            bp = numeric_df.iloc[:, :min(3, len(numeric_df.columns))].boxplot(ax=ax, patch_artist=True, 
                                                                                                widths=0.6, return_type='dict')
                            
                            # Style box plot with neon colors
                            for patch in ax.artists:
                                patch.set_facecolor('#667eea')
                                patch.set_edgecolor('#00d9ff')
                                patch.set_linewidth(2)
                                patch.set_alpha(0.8)
                            
                            # Style whiskers and caps
                            for whisker in ax.get_lines():
                                if 'LINEWIDTH' not in str(whisker):
                                    whisker.set_color('#00d9ff')
                                    whisker.set_linewidth(2)
                                    whisker.set_alpha(0.8)
                            
                            ax.set_title("Box Plot - Outlier Detection", fontsize=13, fontweight='bold', 
                                       color='#00d9ff', pad=15)
                            ax.set_ylabel("Values", color='#00d9ff', fontweight='bold', fontsize=11)
                            ax.set_facecolor('#111829')
                            ax.grid(True, alpha=0.15, axis='y', color='#667eea', linestyle='--')
                            ax.set_axisbelow(True)
                            ax.tick_params(colors='#00d9ff', labelsize=10)
                            
                            # Enhance spines
                            for spine in ax.spines.values():
                                spine.set_edgecolor('#00d9ff')
                                spine.set_linewidth(1.5)
                                spine.set_alpha(0.3)
                            
                            show_chart(fig)
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
                            fig, ax = plt.subplots(figsize=(5, 3.5))
                            col_to_plot = numeric_df.columns[0]
                            parts = ax.violinplot(numeric_df[col_to_plot].dropna().values, vert=True, 
                                                 showmeans=True, showmedians=True)
                            
                            # Style violin plot with neon colors
                            for pc in parts['bodies']:
                                pc.set_facecolor('#667eea')
                                pc.set_edgecolor('#00d9ff')
                                pc.set_alpha(0.8)
                                pc.set_linewidth(2)
                            
                            for partname in ('cbars', 'cmins', 'cmaxes', 'cmedians', 'cmeans'):
                                if partname in parts:
                                    vp = parts[partname]
                                    vp.set_edgecolor('#00d9ff')
                                    vp.set_linewidth(2)
                            
                            safe_col = sanitize_label(col_to_plot)
                            ax.set_title(f"Violin Plot - {safe_col}", fontsize=13, fontweight='bold', 
                                       color='#00d9ff', pad=15)
                            ax.set_ylabel("Values", color='#00d9ff', fontweight='bold', fontsize=11)
                            ax.set_facecolor('#111829')
                            ax.grid(True, alpha=0.15, axis='y', color='#667eea', linestyle='--')
                            ax.set_axisbelow(True)
                            ax.tick_params(colors='#00d9ff', labelsize=10)
                            
                            # Enhance spines
                            for spine in ax.spines.values():
                                spine.set_edgecolor('#00d9ff')
                                spine.set_linewidth(1.5)
                                spine.set_alpha(0.3)
                            
                            show_chart(fig)
                            plt.close()
                        except Exception as e:
                            st.warning(f"Violin plot error: {str(e)}")
                    else:
                        st.info("📭 No numeric data")
            except Exception as e:
                st.error(f"Advanced visualization error: {str(e)}")
        
        # TAB 7: Extended Charts (Area, Doughnut, Bubble, Radar, etc.)
        with tab7:
            st.markdown("### 🌈 Extended Chart Types")
            
            if not numeric_df.empty or not categorical_df.empty:
                # Create sub-tabs for different chart types
                sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5, sub_tab6, sub_tab7, sub_tab8 = st.tabs([
                    "📈 Area", "📊 Column", "🍩 Doughnut", "🫧 Bubble",
                    "🕷️ Radar", "📚 Stacked Bar", "🔷 Comparison", "⚡ Line-Area"
                ])
                
                # Area Chart
                with sub_tab1:
                    st.markdown("#### 📈 Area Chart")
                    if not numeric_df.empty:
                        fig = create_area_chart(numeric_df)
                        if fig:
                            show_chart(fig)
                            plt.close()
                    else:
                        st.info("📭 No numeric columns for area chart")
                
                # Column Chart
                with sub_tab2:
                    st.markdown("#### 📊 Column Chart")
                    if not categorical_df.empty:
                        col_choice = st.selectbox("Select column:", categorical_df.columns, key="col_chart")
                        fig = create_column_chart(df, col_choice, top_n=10)
                        if fig:
                            show_chart(fig)
                            plt.close()
                    elif not numeric_df.empty:
                        col_choice = st.selectbox("Select numeric column:", numeric_df.columns, key="col_chart_num")
                        fig = create_column_chart(df, col_choice, top_n=10)
                        if fig:
                            show_chart(fig)
                            plt.close()
                    else:
                        st.info("📭 No columns available")
                
                # Doughnut Chart
                with sub_tab3:
                    st.markdown("#### 🍩 Doughnut Chart")
                    if not categorical_df.empty:
                        col_choice = st.selectbox("Select column:", categorical_df.columns, key="doughnut")
                        fig = create_doughnut_chart(df, col_choice, top_n=8)
                        if fig:
                            show_chart(fig)
                            plt.close()
                    else:
                        st.info("📭 No categorical columns for doughnut chart")
                
                # Bubble Chart
                with sub_tab4:
                    st.markdown("#### 🫧 Bubble Chart")
                    if len(numeric_df.columns) >= 2:
                        col1_bubble, col2_bubble = st.columns(2)
                        with col1_bubble:
                            x_col = st.selectbox("X-axis:", numeric_df.columns, key="bubble_x")
                        with col2_bubble:
                            y_col = st.selectbox("Y-axis:", numeric_df.columns, key="bubble_y", 
                                               index=min(1, len(numeric_df.columns)-1))
                        
                        fig = create_bubble_chart(df, x_col, y_col)
                        if fig:
                            show_chart(fig)
                            plt.close()
                    else:
                        st.info("📭 Need at least 2 numeric columns for bubble chart")
                
                # Radar Chart
                with sub_tab5:
                    st.markdown("#### 🕷️ Radar (Spider) Chart")
                    if len(numeric_df.columns) >= 3:
                        fig = create_radar_chart(numeric_df)
                        if fig:
                            show_chart(fig)
                            plt.close()
                    else:
                        st.info("📭 Need at least 3 numeric columns for radar chart")
                
                # Stacked Bar Chart
                with sub_tab6:
                    st.markdown("#### 📚 Stacked Bar Chart")
                    if len(categorical_df.columns) >= 2:
                        col_choice = st.selectbox("Main category:", categorical_df.columns, key="stacked")
                        fig = create_stacked_bar_chart(df, col_choice, top_n=5)
                        if fig:
                            show_chart(fig)
                            plt.close()
                    else:
                        st.info("📭 Need at least 2 categorical columns for stacked bar chart")
                
                # Comparison Chart
                with sub_tab7:
                    st.markdown("#### 🔷 Comparison Chart (Statistics)")
                    if not numeric_df.empty:
                        fig = create_comparison_chart(numeric_df)
                        if fig:
                            show_chart(fig)
                            plt.close()
                    else:
                        st.info("📭 No numeric columns for comparison chart")
                
                # Line-Area Combination
                with sub_tab8:
                    st.markdown("#### ⚡ Line-Area Combination")
                    if not numeric_df.empty:
                        fig = create_line_area_combination(numeric_df)
                        if fig:
                            show_chart(fig)
                            plt.close()
                    else:
                        st.info("📭 No numeric columns for line-area chart")
        
        # TAB 8: Data Quality Report
        with tab8:
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
                        fig, ax = plt.subplots(figsize=(5, 3.5))
                        colors_missing = plt.cm.plasma(np.linspace(0, 1, len(missing_df)))
                        bars = ax.barh(missing_df['Column'], missing_df['Missing %'], color=colors_missing, 
                                      edgecolor='#00d9ff', linewidth=2, alpha=0.85)
                        
                        # Add percentage labels
                        for i, (idx, row) in enumerate(missing_df.iterrows()):
                            ax.text(row['Missing %'] + 1, i, f"{row['Missing %']:.1f}%", 
                                   va='center', color='#00d9ff', fontweight='bold', fontsize=10)
                        
                        ax.set_xlabel("Missing Percentage (%)", color='#00d9ff', fontweight='bold', fontsize=11)
                        ax.set_title("Missing Values by Column", fontsize=13, fontweight='bold', 
                                   color='#00d9ff', pad=15)
                        ax.set_facecolor('#111829')
                        ax.tick_params(colors='#00d9ff', labelsize=10)
                        ax.grid(True, alpha=0.15, axis='x', color='#667eea', linestyle='--')
                        ax.set_axisbelow(True)
                        
                        # Enhance spines
                        for spine in ax.spines.values():
                            spine.set_edgecolor('#00d9ff')
                            spine.set_linewidth(1.5)
                            spine.set_alpha(0.3)
                        
                        show_chart(fig)
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


def show_simple_charts(df):
    """Simplified version for quick overview"""
    st.subheader("📊 Data Overview")
    
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    
    if not numeric_df.empty:
        st.line_chart(numeric_df.iloc[:, :3])
