"""
3D EDA Visualization Module
Provides comprehensive 3D plotting techniques for exploratory data analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class Visualizer3D:
    """3D visualization techniques for EDA"""
    
    @staticmethod
    def get_numeric_columns(df, min_count=2):
        """Get numeric columns for 3D plots"""
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        return numeric_cols[:min_count] if len(numeric_cols) >= min_count else numeric_cols
    
    @staticmethod
    def scatter_3d(df, x_col=None, y_col=None, z_col=None, color_col=None, size_col=None):
        """
        3D Scatter Plot - Identify clusters, correlations, and outliers
        
        Args:
            df: DataFrame
            x_col, y_col, z_col: Column names for axes
            color_col: Column for color coding
            size_col: Column for bubble size
        """
        numeric_cols = Visualizer3D.get_numeric_columns(df, min_count=3)
        
        if len(numeric_cols) < 3:
            st.warning("Need at least 3 numeric columns for 3D scatter plot")
            return None
        
        # Use provided columns or defaults
        x_col = x_col or numeric_cols[0]
        y_col = y_col or numeric_cols[1]
        z_col = z_col or numeric_cols[2]
        
        # Create interactive 3D scatter with Plotly
        fig = go.Figure(data=[go.Scatter3d(
            x=df[x_col].fillna(df[x_col].mean()),
            y=df[y_col].fillna(df[y_col].mean()),
            z=df[z_col].fillna(df[z_col].mean()),
            mode='markers',
            marker=dict(
                size=5,
                color=df[color_col].fillna(df[color_col].mean()) if color_col and color_col in df.columns else df[z_col],
                colorscale='Viridis',
                showscale=True,
                opacity=0.8,
                line=dict(width=0.5, color='white')
            ),
            text=[f"{x_col}: {x:.2f}<br>{y_col}: {y:.2f}<br>{z_col}: {z:.2f}" 
                  for x, y, z in zip(df[x_col], df[y_col], df[z_col])],
            hovertemplate='%{text}<extra></extra>'
        )])
        
        fig.update_layout(
            title=f'3D Scatter Plot: {x_col} vs {y_col} vs {z_col}',
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col,
                bgcolor='rgba(20, 24, 82, 0.9)',
                xaxis=dict(backgroundcolor='rgba(0, 0, 0, 0.5)', gridcolor='rgba(128, 128, 128, 0.2)'),
                yaxis=dict(backgroundcolor='rgba(0, 0, 0, 0.5)', gridcolor='rgba(128, 128, 128, 0.2)'),
                zaxis=dict(backgroundcolor='rgba(0, 0, 0, 0.5)', gridcolor='rgba(128, 128, 128, 0.2)'),
            ),
            paper_bgcolor='rgba(20, 24, 82, 0.95)',
            font=dict(color='white', size=12),
            hovermode='closest',
            height=700
        )
        
        return fig
    
    @staticmethod
    def surface_3d(df, x_col=None, y_col=None, z_col=None):
        """
        3D Surface Plot - Visualize how Z changes across X and Y
        Used for topographical or temperature mapping
        """
        numeric_cols = Visualizer3D.get_numeric_columns(df, min_count=3)
        
        if len(numeric_cols) < 3:
            st.warning("Need at least 3 numeric columns for 3D surface plot")
            return None
        
        x_col = x_col or numeric_cols[0]
        y_col = y_col or numeric_cols[1]
        z_col = z_col or numeric_cols[2]
        
        # Create grid for surface plot
        x_data = df[x_col].dropna().values
        y_data = df[y_col].dropna().values
        z_data = df[z_col].dropna().values
        
        # Normalize for better visualization
        x_norm = (x_data - x_data.min()) / (x_data.max() - x_data.min() + 1e-10)
        y_norm = (y_data - y_data.min()) / (y_data.max() - y_data.min() + 1e-10)
        z_norm = (z_data - z_data.min()) / (z_data.max() - z_data.min() + 1e-10)
        
        # Create mesh grid
        x_mesh = np.linspace(0, 1, 30)
        y_mesh = np.linspace(0, 1, 30)
        X, Y = np.meshgrid(x_mesh, y_mesh)
        
        # Interpolate Z values
        from scipy.interpolate import griddata
        Z = griddata((x_norm, y_norm), z_norm, (X, Y), method='cubic')
        
        fig = go.Figure(data=[go.Surface(
            x=X,
            y=Y,
            z=Z,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title=z_col, len=0.7)
        )])
        
        fig.update_layout(
            title=f'3D Surface Plot: {z_col} vs {x_col} & {y_col}',
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col,
                bgcolor='rgba(20, 24, 82, 0.9)',
            ),
            paper_bgcolor='rgba(20, 24, 82, 0.95)',
            font=dict(color='white', size=12),
            height=700
        )
        
        return fig
    
    @staticmethod
    def line_3d(df, x_col=None, y_col=None, z_col=None):
        """
        3D Line Plot - Track changes across three dimensions over time/metrics
        """
        numeric_cols = Visualizer3D.get_numeric_columns(df, min_count=3)
        
        if len(numeric_cols) < 3:
            st.warning("Need at least 3 numeric columns for 3D line plot")
            return None
        
        x_col = x_col or numeric_cols[0]
        y_col = y_col or numeric_cols[1]
        z_col = z_col or numeric_cols[2]
        
        # Sort by first column for line continuity
        df_sorted = df.sort_values(by=x_col)
        
        fig = go.Figure(data=[go.Scatter3d(
            x=df_sorted[x_col].fillna(df_sorted[x_col].mean()),
            y=df_sorted[y_col].fillna(df_sorted[y_col].mean()),
            z=df_sorted[z_col].fillna(df_sorted[z_col].mean()),
            mode='lines+markers',
            line=dict(
                color=df_sorted[z_col].fillna(df_sorted[z_col].mean()),
                colorscale='Plasma',
                showscale=True,
                width=4
            ),
            marker=dict(
                size=4,
                color=df_sorted[z_col].fillna(df_sorted[z_col].mean()),
                colorscale='Plasma',
                showscale=False,
                opacity=0.8
            ),
            hovertemplate=f'{x_col}: %{{x:.2f}}<br>{y_col}: %{{y:.2f}}<br>{z_col}: %{{z:.2f}}<extra></extra>'
        )])
        
        fig.update_layout(
            title=f'3D Line Plot: {x_col}, {y_col}, {z_col}',
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col,
                bgcolor='rgba(20, 24, 82, 0.9)',
            ),
            paper_bgcolor='rgba(20, 24, 82, 0.95)',
            font=dict(color='white', size=12),
            hovermode='closest',
            height=700
        )
        
        return fig
    
    @staticmethod
    def bar_3d(df, x_col=None, y_col=None, z_col=None):
        """
        3D Bar Chart - Compare multiple variables across categories
        """
        # For 3D bars, we'll use top categories to avoid clutter
        numeric_cols = Visualizer3D.get_numeric_columns(df, min_count=2)
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if len(numeric_cols) < 2 or len(categorical_cols) < 1:
            st.warning("Need at least 2 numeric columns and 1 categorical column")
            return None
        
        cat_col = categorical_cols[0]
        x_col = x_col or numeric_cols[0]
        y_col = y_col or numeric_cols[1]
        
        # Get top categories
        top_n = 10
        df_plot = df.nlargest(top_n, x_col)
        
        fig = go.Figure(data=[go.Bar3d(
            x=df_plot[cat_col].astype(str),
            y=df_plot[x_col],
            z=df_plot[y_col],
            marker=dict(
                color=df_plot[y_col],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title=y_col)
            ),
            text=df_plot[cat_col],
            hovertemplate='<b>%{text}</b><br>' + f'{x_col}: %{{y:.2f}}<br>{y_col}: %{{z:.2f}}<extra></extra>'
        )])
        
        fig.update_layout(
            title=f'3D Bar Chart: Top {top_n} by {x_col}',
            scene=dict(
                xaxis_title=cat_col,
                yaxis_title=x_col,
                zaxis_title=y_col,
                bgcolor='rgba(20, 24, 82, 0.9)',
            ),
            paper_bgcolor='rgba(20, 24, 82, 0.95)',
            font=dict(color='white', size=12),
            height=700
        )
        
        return fig
    
    @staticmethod
    def bubble_3d(df, x_col=None, y_col=None, z_col=None, size_col=None, color_col=None):
        """
        3D Bubble Plot - Extended scatter plot with size and additional dimensions
        """
        numeric_cols = Visualizer3D.get_numeric_columns(df, min_count=3)
        
        if len(numeric_cols) < 3:
            st.warning("Need at least 3 numeric columns")
            return None
        
        x_col = x_col or numeric_cols[0]
        y_col = y_col or numeric_cols[1]
        z_col = z_col or numeric_cols[2]
        size_col = size_col or numeric_cols[-1]
        color_col = color_col or z_col
        
        # Normalize size for better visualization
        size_data = df[size_col].fillna(df[size_col].mean())
        size_normalized = (size_data - size_data.min()) / (size_data.max() - size_data.min() + 1e-10) * 30 + 5
        
        fig = go.Figure(data=[go.Scatter3d(
            x=df[x_col].fillna(df[x_col].mean()),
            y=df[y_col].fillna(df[y_col].mean()),
            z=df[z_col].fillna(df[z_col].mean()),
            mode='markers',
            marker=dict(
                size=size_normalized,
                color=df[color_col].fillna(df[color_col].mean()),
                colorscale='Plasma',
                showscale=True,
                opacity=0.7,
                line=dict(width=0.5, color='white'),
                colorbar=dict(title=color_col, len=0.7)
            ),
            text=[f"{x_col}: {x:.2f}<br>{y_col}: {y:.2f}<br>{z_col}: {z:.2f}<br>{size_col}: {s:.2f}" 
                  for x, y, z, s in zip(df[x_col], df[y_col], df[z_col], size_data)],
            hovertemplate='%{text}<extra></extra>'
        )])
        
        fig.update_layout(
            title=f'3D Bubble Plot: {x_col} vs {y_col} vs {z_col} (size={size_col})',
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col,
                bgcolor='rgba(20, 24, 82, 0.9)',
            ),
            paper_bgcolor='rgba(20, 24, 82, 0.95)',
            font=dict(color='white', size=12),
            height=700
        )
        
        return fig
    
    @staticmethod
    def show_3d_eda(df):
        """Display comprehensive 3D EDA visualizations"""
        
        if df.empty or len(df.select_dtypes(include=['float64', 'int64']).columns) < 3:
            st.warning("⚠️ Requires at least 3 numeric columns for 3D visualizations")
            return
        
        st.markdown("### 🎯 3D EDA Techniques")
        
        # Create tabs for different 3D visualization types
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔴 3D Scatter",
            "📊 3D Surface",
            "📈 3D Line",
            "📦 3D Bars",
            "🫧 3D Bubble"
        ])
        
        # TAB 1: 3D Scatter Plot
        with tab1:
            st.subheader("3D Scatter Plot")
            st.info("Identify clusters, correlations, and outliers across three numerical variables")
            
            col1, col2, col3 = st.columns(3)
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            
            with col1:
                x_col = st.selectbox("X-axis", numeric_cols, key="scatter_x")
            with col2:
                y_col = st.selectbox("Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0, key="scatter_y")
            with col3:
                z_col = st.selectbox("Z-axis", numeric_cols, index=2 if len(numeric_cols) > 2 else 0, key="scatter_z")
            
            fig = Visualizer3D.scatter_3d(df, x_col, y_col, z_col)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # TAB 2: 3D Surface Plot
        with tab2:
            st.subheader("3D Surface Plot")
            st.info("Visualize how a dependent variable changes across two continuous independent variables")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                x_col = st.selectbox("X-axis", numeric_cols, key="surface_x")
            with col2:
                y_col = st.selectbox("Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0, key="surface_y")
            with col3:
                z_col = st.selectbox("Z-axis", numeric_cols, index=2 if len(numeric_cols) > 2 else 0, key="surface_z")
            
            fig = Visualizer3D.surface_3d(df, x_col, y_col, z_col)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # TAB 3: 3D Line Plot
        with tab3:
            st.subheader("3D Line Plot")
            st.info("Track changes or movements across three dimensions over time or metrics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                x_col = st.selectbox("X-axis", numeric_cols, key="line_x")
            with col2:
                y_col = st.selectbox("Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0, key="line_y")
            with col3:
                z_col = st.selectbox("Z-axis", numeric_cols, index=2 if len(numeric_cols) > 2 else 0, key="line_z")
            
            fig = Visualizer3D.line_3d(df, x_col, y_col, z_col)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # TAB 4: 3D Bar Chart
        with tab4:
            st.subheader("3D Bar Chart")
            st.info("Compare multiple categorical variables across a common numerical metric")
            
            fig = Visualizer3D.bar_3d(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # TAB 5: 3D Bubble Plot
        with tab5:
            st.subheader("3D Bubble Plot")
            st.info("Extended visualization with variable bubble sizes and color coding")
            
            fig = Visualizer3D.bubble_3d(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
