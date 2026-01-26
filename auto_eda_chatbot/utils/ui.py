"""
UI Helper Module
================
Centralized chart display function to enforce consistent sizing and prevent
visualization layout bugs. All charts MUST use this function.
"""

import streamlit as st
import matplotlib.pyplot as plt


def show_chart(fig, width=5, height=3):
    """
    Display matplotlib figure with enforced sizing rules.
    
    This function ensures:
    - Consistent chart dimensions across entire dashboard
    - No accidental Streamlit container stretching
    - Proper cleanup after display
    
    Args:
        fig: matplotlib figure object
        width: chart width in inches (default: 5)
        height: chart height in inches (default: 3)
    
    Usage:
        >>> fig, ax = plt.subplots()
        >>> ax.plot([1,2,3], [1,2,3])
        >>> show_chart(fig)  # Perfect size, no stretching
    """
    fig.set_size_inches(width, height)
    st.pyplot(fig, width="content")
    plt.close(fig)


def show_chart_wide(fig, width=6.5, height=5):
    """Display wider heatmap/correlation charts (6.5 x 5 inches)"""
    fig.set_size_inches(width, height)
    st.pyplot(fig, width="content")
    plt.close(fig)


def show_chart_square(fig, size=5):
    """Display square charts like radar/polar plots (5 x 5 inches)"""
    fig.set_size_inches(size, size)
    st.pyplot(fig, width="content")
    plt.close(fig)
