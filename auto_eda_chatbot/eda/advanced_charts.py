"""
Advanced Visualization Module
==============================

Comprehensive charting library with modern chart types:
- Area Charts, Column Charts, Doughnut, Bubble Charts
- Radar/Spider Charts, Stacked Bar Charts, Gauges
- Comparison Charts, and more

Uses matplotlib and plotly for rich visualizations.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np
from .eda_palette import EDAPalette, EDAPaletteConfigurator

# Ensure dark theme is applied
EDAPaletteConfigurator.apply_dark_theme()


def create_area_chart(df, col_list=None):
    """
    Create area chart showing cumulative distribution.
    
    Args:
        df: DataFrame with numeric columns
        col_list: List of column names to plot (default: first 3)
    """
    if col_list is None:
        col_list = df.select_dtypes(include=['float64', 'int64']).columns[:3]
    
    try:
        fig, ax = plt.subplots(figsize=(5, 3.5))
        
        for idx, col in enumerate(col_list):
            ax.fill_between(range(len(df)), df[col].values, alpha=0.6, 
                           color=EDAPalette.CATEGORICAL['colors'][idx % 8],
                           label=str(col)[:20])
        
        ax.set_title("Area Chart - Value Distribution Over Index", 
                    fontsize=13, fontweight='bold', color=EDAPalette.ACCENT['glow_cyan'], pad=15)
        ax.set_xlabel("Index", color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold')
        ax.set_ylabel("Values", color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold')
        ax.legend(fontsize=9, loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.15, linestyle='--')
        ax.set_facecolor(EDAPalette.DARK_THEME['background_secondary'])
        
        return fig
    except Exception as e:
        st.warning(f"Area chart error: {str(e)}")
        return None


def create_column_chart(df, col_name, top_n=10):
    """
    Create vertical column chart for categorical data.
    
    Args:
        df: DataFrame
        col_name: Column name to analyze
        top_n: Show top N categories
    """
    try:
        fig, ax = plt.subplots(figsize=(5, 4))
        
        if df[col_name].dtype == 'object':
            # Categorical column
            value_counts = df[col_name].value_counts().head(top_n)
            x_pos = np.arange(len(value_counts))
            colors = EDAPalette.CATEGORICAL['colors'][:len(value_counts)]
            
            bars = ax.bar(x_pos, value_counts.values, color=colors,
                         edgecolor=EDAPalette.ACCENT['glow_cyan'], linewidth=2, alpha=0.85)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom', 
                       color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold', fontsize=9)
            
            ax.set_xticks(x_pos)
            ax.set_xticklabels([str(x)[:15] for x in value_counts.index], 
                              rotation=45, ha='right', color=EDAPalette.ACCENT['glow_cyan'])
        else:
            # Numeric column - create bins
            ax.bar(range(len(df)), df[col_name].values, 
                  color=EDAPalette.ACCENT['glow_cyan'], alpha=0.8,
                  edgecolor='white', linewidth=1)
            ax.set_xlabel("Index", color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold')
        
        ax.set_title(f"Column Chart - {col_name}", fontsize=13, fontweight='bold',
                    color=EDAPalette.ACCENT['glow_cyan'], pad=15)
        ax.set_ylabel("Count/Value", color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold')
        ax.grid(True, alpha=0.15, axis='y', linestyle='--')
        ax.set_facecolor(EDAPalette.DARK_THEME['background_secondary'])
        ax.tick_params(colors=EDAPalette.ACCENT['glow_cyan'])
        
        return fig
    except Exception as e:
        st.warning(f"Column chart error: {str(e)}")
        return None


def create_doughnut_chart(df, col_name, top_n=8):
    """
    Create doughnut (donut) chart.
    
    Args:
        df: DataFrame
        col_name: Column to analyze
        top_n: Top N categories to show
    """
    try:
        fig, ax = plt.subplots(figsize=(7, 6.5))
        
        if df[col_name].dtype == 'object':
            value_counts = df[col_name].value_counts().head(top_n)
            labels = [str(x)[:20] for x in value_counts.index]
            sizes = value_counts.values
        else:
            # Numeric - create bins
            sizes = df[col_name].value_counts().head(top_n).values
            labels = [f"Bin {i+1}" for i in range(len(sizes))]
        
        colors = EDAPalette.CATEGORICAL['colors'][:len(sizes)]
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                          colors=colors, startangle=90,
                                          textprops={'fontsize': 10, 'fontweight': 'bold', 
                                                    'color': 'white'})
        
        # Create doughnut hole
        centre_circle = plt.Circle((0, 0), 0.70, fc=EDAPalette.DARK_THEME['background_secondary'],
                                   edgecolor=EDAPalette.ACCENT['glow_cyan'], linewidth=2)
        ax.add_artist(centre_circle)
        
        ax.set_title(f"Doughnut Chart - {col_name}", fontsize=13, fontweight='bold',
                    color=EDAPalette.ACCENT['glow_cyan'], pad=15)
        
        return fig
    except Exception as e:
        st.warning(f"Doughnut chart error: {str(e)}")
        return None


def create_bubble_chart(df, x_col=None, y_col=None, size_col=None, color_col=None):
    """
    Create bubble chart with size and color dimensions.
    
    Args:
        df: DataFrame
        x_col: X-axis column (default: first numeric)
        y_col: Y-axis column (default: second numeric)
        size_col: Column for bubble size (default: third numeric)
        color_col: Column for bubble color (default: fourth numeric)
    """
    try:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        
        if len(numeric_cols) < 2:
            st.warning("Need at least 2 numeric columns for bubble chart")
            return None
        
        x_col = x_col or numeric_cols[0]
        y_col = y_col or numeric_cols[1]
        size_col = size_col or (numeric_cols[2] if len(numeric_cols) > 2 else numeric_cols[0])
        color_col = color_col or (numeric_cols[3] if len(numeric_cols) > 3 else numeric_cols[1])
        
        fig, ax = plt.subplots(figsize=(5, 4))
        
        x_data = df[x_col].values
        y_data = df[y_col].values
        size_data = df[size_col].values
        color_data = df[color_col].values
        
        # Normalize sizes
        sizes = (size_data - size_data.min()) / (size_data.max() - size_data.min()) * 300 + 50
        
        scatter = ax.scatter(x_data, y_data, s=sizes, c=color_data, 
                           cmap='twilight', alpha=0.7, edgecolors=EDAPalette.ACCENT['glow_cyan'],
                           linewidth=1.5)
        
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label(str(color_col), color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold')
        cbar.ax.tick_params(colors=EDAPalette.ACCENT['glow_cyan'])
        
        ax.set_xlabel(str(x_col), color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold', fontsize=11)
        ax.set_ylabel(str(y_col), color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold', fontsize=11)
        ax.set_title(f"Bubble Chart - Size:{size_col}, Color:{color_col}", 
                    fontsize=13, fontweight='bold', color=EDAPalette.ACCENT['glow_cyan'], pad=15)
        ax.grid(True, alpha=0.15, linestyle='--')
        ax.set_facecolor(EDAPalette.DARK_THEME['background_secondary'])
        ax.tick_params(colors=EDAPalette.ACCENT['glow_cyan'])
        
        return fig
    except Exception as e:
        st.warning(f"Bubble chart error: {str(e)}")
        return None


def create_radar_chart(df, col_list=None):
    """
    Create radar (spider) chart for multiple dimensions.
    
    IMPORTANT: Normalizes all values to 0-1 scale to handle different data ranges.
    This prevents axis scaling issues when mixing salary, age, experience, etc.
    
    Args:
        df: DataFrame
        col_list: Columns to include (default: first 6 numeric)
    """
    try:
        from sklearn.preprocessing import MinMaxScaler
        
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        
        if len(numeric_cols) < 3:
            st.warning("Need at least 3 numeric columns for radar chart")
            return None
        
        col_list = col_list or numeric_cols[:6]
        
        # Get mean values and NORMALIZE to 0-1 scale
        values = df[col_list].mean().values.reshape(-1, 1)
        scaler = MinMaxScaler(feature_range=(0, 1))
        values_normalized = scaler.fit_transform(values).flatten()
        
        # Complete the circle for plotting
        values_plot = np.concatenate((values_normalized, [values_normalized[0]]))
        
        angles = np.linspace(0, 2 * np.pi, len(col_list), endpoint=False).tolist()
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(5.5, 5.5), subplot_kw=dict(projection='polar'))
        
        ax.plot(angles, values_plot, 'o-', linewidth=2.5, color=EDAPalette.ACCENT['glow_magenta'],
               markersize=8, markerfacecolor=EDAPalette.ACCENT['glow_cyan'])
        ax.fill(angles, values_plot, alpha=0.25, color=EDAPalette.ACCENT['glow_magenta'])
        
        # Clean labels - sanitize for display
        labels = [str(x)[:12] for x in col_list]
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, color=EDAPalette.ACCENT['glow_cyan'],
                           fontweight='bold', fontsize=9)
        ax.set_ylim(0, 1.1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
        ax.grid(True, color=EDAPalette.SEMANTIC['info'], alpha=0.3)
        ax.set_facecolor(EDAPalette.DARK_THEME['background_secondary'])
        
        ax.set_title("Radar Chart - Normalized Multi-Dimensional Analysis", 
                    fontsize=13, fontweight='bold', color=EDAPalette.ACCENT['glow_cyan'],
                    pad=20)
        
        return fig
    except Exception as e:
        st.warning(f"Radar chart error: {str(e)}")
        return None


def create_stacked_bar_chart(df, col_name, stack_col=None, top_n=5):
    """
    Create stacked bar chart.
    
    Args:
        df: DataFrame
        col_name: Main category column
        stack_col: Column to stack by (default: first categorical)
        top_n: Top N categories
    """
    try:
        if stack_col is None:
            cat_cols = df.select_dtypes(include=['object']).columns
            if len(cat_cols) < 2:
                st.warning("Need at least 2 categorical columns for stacked bar")
                return None
            stack_col = cat_cols[1]
        
        # Create pivot table
        pivot_data = pd.crosstab(df[col_name], df[stack_col])
        pivot_data = pivot_data.iloc[:top_n, :]
        
        fig, ax = plt.subplots(figsize=(5, 3.5))
        
        pivot_data.plot(kind='bar', stacked=True, ax=ax, 
                       color=EDAPalette.CATEGORICAL['colors'][:len(pivot_data.columns)],
                       edgecolor='white', linewidth=1.5, alpha=0.85)
        
        ax.set_title(f"Stacked Bar Chart - {col_name} by {stack_col}", 
                    fontsize=13, fontweight='bold', color=EDAPalette.ACCENT['glow_cyan'], pad=15)
        ax.set_xlabel(str(col_name), color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold')
        ax.set_ylabel("Count", color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold')
        ax.legend(title=str(stack_col), loc='upper right', framealpha=0.9, fontsize=9)
        ax.grid(True, alpha=0.15, axis='y', linestyle='--')
        ax.set_facecolor(EDAPalette.DARK_THEME['background_secondary'])
        ax.tick_params(colors=EDAPalette.ACCENT['glow_cyan'], labelsize=9)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        return fig
    except Exception as e:
        st.warning(f"Stacked bar chart error: {str(e)}")
        return None


def create_gauge_chart(value, max_value=100, title="Gauge Chart"):
    """
    Create gauge/speedometer chart.
    
    Args:
        value: Current value
        max_value: Maximum value
        title: Chart title
    """
    try:
        fig, ax = plt.subplots(figsize=(5, 4), subplot_kw=dict(projection='polar'))
        
        # Gauge setup
        theta = np.linspace(0, np.pi, 100)
        r = np.ones(100)
        
        # Color zones
        zones = [
            (0, np.pi/3, EDAPalette.SEMANTIC['success']),        # Green: 0-33%
            (np.pi/3, 2*np.pi/3, EDAPalette.SEMANTIC['warning']), # Orange: 33-66%
            (2*np.pi/3, np.pi, EDAPalette.SEMANTIC['danger']),    # Red: 66-100%
        ]
        
        for start, end, color in zones:
            theta_zone = np.linspace(start, end, 50)
            ax.plot(theta_zone, np.ones(50), color=color, linewidth=8, alpha=0.8)
        
        # Needle position
        needle_angle = (value / max_value) * np.pi
        ax.arrow(0, 0, needle_angle, 1, head_width=0.1, head_length=0.1,
                fc=EDAPalette.ACCENT['glow_magenta'], ec=EDAPalette.ACCENT['glow_cyan'],
                linewidth=2)
        
        # Center circle
        circle = plt.Circle((0, 0), 0.1, color=EDAPalette.DARK_THEME['background_secondary'],
                          transform=ax.transData._b, zorder=10)
        ax.add_patch(circle)
        
        ax.set_ylim(0, 1.3)
        ax.set_theta_offset(np.pi)
        ax.set_theta_direction(-1)
        ax.set_xticks([0, np.pi/3, 2*np.pi/3, np.pi])
        ax.set_xticklabels(['0%', '33%', '66%', '100%'], color=EDAPalette.ACCENT['glow_cyan'],
                          fontweight='bold', fontsize=11)
        ax.set_yticks([])
        ax.set_facecolor(EDAPalette.DARK_THEME['background_secondary'])
        ax.grid(True, alpha=0.2)
        
        # Add value text
        ax.text(np.pi/2, 1.5, f'{value:.1f}/{max_value}', ha='center', va='center',
               fontsize=16, fontweight='bold', color=EDAPalette.ACCENT['glow_cyan'],
               bbox=dict(boxstyle='round', facecolor=EDAPalette.DARK_THEME['background_tertiary'],
                        edgecolor=EDAPalette.ACCENT['glow_cyan'], linewidth=2))
        
        ax.set_title(title, fontsize=13, fontweight='bold', 
                    color=EDAPalette.ACCENT['glow_cyan'], pad=20)
        
        return fig
    except Exception as e:
        st.warning(f"Gauge chart error: {str(e)}")
        return None


def create_comparison_chart(df, col_list=None, normalize=True):
    """
    Create comparison chart for multiple metrics.
    
    Args:
        df: DataFrame
        col_list: Columns to compare
        normalize: Normalize to 0-1 scale
    """
    try:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        col_list = col_list or numeric_cols[:6]
        
        comparison_data = df[col_list].describe().loc[['mean', '50%', 'std']].T
        
        if normalize:
            for col in comparison_data.columns:
                max_val = comparison_data[col].max()
                if max_val != 0:
                    comparison_data[col] = comparison_data[col] / max_val
        
        fig, ax = plt.subplots(figsize=(5, 3.5))
        
        x = np.arange(len(comparison_data))
        width = 0.25
        
        for idx, col in enumerate(comparison_data.columns):
            ax.bar(x + idx*width, comparison_data[col], width,
                  label=col, color=EDAPalette.CATEGORICAL['colors'][idx % 8],
                  alpha=0.85, edgecolor='white', linewidth=1.5)
        
        ax.set_xlabel("Columns", color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold')
        ax.set_ylabel("Value", color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold')
        ax.set_title("Comparison Chart - Statistics Across Columns", 
                    fontsize=13, fontweight='bold', color=EDAPalette.ACCENT['glow_cyan'], pad=15)
        ax.set_xticks(x + width)
        ax.set_xticklabels([str(col)[:15] for col in comparison_data.index], 
                          rotation=45, ha='right', color=EDAPalette.ACCENT['glow_cyan'])
        ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
        ax.grid(True, alpha=0.15, axis='y', linestyle='--')
        ax.set_facecolor(EDAPalette.DARK_THEME['background_secondary'])
        ax.tick_params(colors=EDAPalette.ACCENT['glow_cyan'])
        
        return fig
    except Exception as e:
        st.warning(f"Comparison chart error: {str(e)}")
        return None


def create_line_area_combination(df, col_list=None):
    """
    Create combined line and area chart.
    
    Args:
        df: DataFrame
        col_list: Columns to plot
    """
    try:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        col_list = col_list or numeric_cols[:3]
        
        fig, ax = plt.subplots(figsize=(5, 3.5))
        
        for idx, col in enumerate(col_list):
            ax.plot(df.index, df[col], marker='o', linewidth=2.5, markersize=4,
                   label=str(col)[:20], color=EDAPalette.CATEGORICAL['colors'][idx % 8])
            ax.fill_between(df.index, df[col], alpha=0.2, 
                          color=EDAPalette.CATEGORICAL['colors'][idx % 8])
        
        ax.set_title("Line-Area Combination Chart", fontsize=13, fontweight='bold',
                    color=EDAPalette.ACCENT['glow_cyan'], pad=15)
        ax.set_xlabel("Index", color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold')
        ax.set_ylabel("Values", color=EDAPalette.ACCENT['glow_cyan'], fontweight='bold')
        ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
        ax.grid(True, alpha=0.15, linestyle='--')
        ax.set_facecolor(EDAPalette.DARK_THEME['background_secondary'])
        ax.tick_params(colors=EDAPalette.ACCENT['glow_cyan'])
        
        return fig
    except Exception as e:
        st.warning(f"Line-area chart error: {str(e)}")
        return None
