"""Visualization utilities and plotting functions."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any

from config import settings

# Set default style
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


def create_plot(
    data: pd.DataFrame,
    plot_type: str = "line",
    title: str = "Plot",
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
    save_path: Optional[Path] = None,
    **kwargs,
) -> plt.Figure:
    """Create a plot from DataFrame data.

    Args:
        data: DataFrame containing the data to plot
        plot_type: Type of plot ('line', 'bar', 'scatter', 'hist', 'box')
        title: Title for the plot
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        save_path: Optional path to save the plot
        **kwargs: Additional arguments passed to the plotting function

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=kwargs.get("figsize", (10, 6)))

    if plot_type == "line":
        data.plot.line(ax=ax, x=x_col, y=y_col, **kwargs)
    elif plot_type == "bar":
        data.plot.bar(ax=ax, x=x_col, y=y_col, **kwargs)
    elif plot_type == "scatter":
        data.plot.scatter(ax=ax, x=x_col, y=y_col, **kwargs)
    elif plot_type == "hist":
        data.plot.hist(ax=ax, **kwargs)
    elif plot_type == "box":
        data.plot.box(ax=ax, **kwargs)
    else:
        raise ValueError(f"Unsupported plot type: {plot_type}")

    ax.set_title(title)
    ax.grid(True, alpha=0.3)

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


def plot_correlation_matrix(
    data: pd.DataFrame,
    title: str = "Correlation Matrix",
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """Create a correlation matrix heatmap.

    Args:
        data: DataFrame with numeric columns
        title: Title for the plot
        save_path: Optional path to save the plot

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Calculate correlation matrix
    corr = data.select_dtypes(include=["number"]).corr()

    # Create heatmap
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, square=True, ax=ax)

    ax.set_title(title)

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


def plot_distribution(
    data: pd.Series,
    title: str = "Distribution",
    bins: int = 30,
    save_path: Optional[Path] = None,
) -> plt.Figure:
    """Create a distribution plot.

    Args:
        data: Series to plot
        title: Title for the plot
        bins: Number of bins for histogram
        save_path: Optional path to save the plot

    Returns:
        matplotlib Figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Histogram
    data.hist(bins=bins, ax=ax1, alpha=0.7)
    ax1.set_title(f"{title} - Histogram")
    ax1.grid(True, alpha=0.3)

    # Box plot
    data.plot.box(ax=ax2)
    ax2.set_title(f"{title} - Box Plot")
    ax2.grid(True, alpha=0.3)

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig


# Example usage
if __name__ == "__main__":
    # Create sample data
    import numpy as np

    sample_data = pd.DataFrame(
        {
            "x": np.random.randn(100),
            "y": np.random.randn(100),
            "category": np.random.choice(["A", "B", "C"], 100),
        }
    )

    # Create plots
    fig1 = create_plot(sample_data, "scatter", "Sample Scatter Plot", "x", "y")
    fig2 = plot_correlation_matrix(sample_data, "Sample Correlation Matrix")
    fig3 = plot_distribution(sample_data["x"], "X Distribution")

    plt.show()
