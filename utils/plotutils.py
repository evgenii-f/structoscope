import matplotlib.pyplot as plt
import numpy as np
from matplotlib import tri
import plotly.express as px


def plot_xy_scatter(
    df,
    x_col: str,
    y_col: str,
    title: str = None,
    xlabel: str = None,
    ylabel: str = None,
    point_alpha: float = 0.3,
    point_size: float = 1,
    grid: bool = True,
    dpi: int = 150,
    figsize=(4, 4)
):
    """Generic 2D scatter plot for two DataFrame columns."""
    if x_col not in df.columns or y_col not in df.columns:
        print(f"Missing columns: {x_col}, {y_col}")
        return

    plt.figure(dpi=dpi, figsize=figsize)
    plt.plot(df[x_col], df[y_col], 'o', ms=point_size, alpha=point_alpha)
    plt.xlabel(xlabel or x_col.replace("_", " ").title())
    plt.ylabel(ylabel or y_col.replace("_", " ").title())
    if grid:
        plt.grid(True)
    plt.title(title or f"{len(df)} structures")
    plt.tight_layout()
    plt.show()


def plot_contour_interpolation(
        df,
        x_col: str,
        y_col: str,
        z_col: str,
        title: str = None,
        xlabel: str = None,
        ylabel: str = None,
        zlabel: str = "Z",
        levels: int = 55,
        point_alpha: float = 0.2,
        point_size: float = 0.5,
        dpi: int = 200,
        figsize=(4, 4)
):
    """Contour plot from scattered (x,y,z) data with interpolation."""
    for col in [x_col, y_col, z_col]:
        if col not in df.columns:
            print(f"Missing column: {col}")
            return

    x = df[x_col].to_numpy()
    y = df[y_col].to_numpy()
    z = df[z_col].to_numpy()

    if len(x) < 3:
        print(f"Too few data points: {len(x)}")
        return

    fig, ax = plt.subplots(dpi=dpi, figsize=figsize)

    try:
        triang = tri.Triangulation(x, y)
        interpolator = tri.LinearTriInterpolator(triang, z)
        xi = np.linspace(np.min(x), np.max(x), 400)
        yi = np.linspace(np.min(y), np.max(y), 400)
        Xi, Yi = np.meshgrid(xi, yi)
        zi = interpolator(Xi, Yi)

        ax.contour(xi, yi, zi, levels=levels, linewidths=0.5, colors='k')
        cntr = ax.contourf(xi, yi, zi, levels=levels, cmap="RdYlBu")
        fig.colorbar(cntr, ax=ax, label=zlabel)
    except Exception as e:
        ax.text(0.5, 0.5, f"Interpolation failed:\n{str(e)}",
                transform=ax.transAxes, ha='center', va='center')

    ax.plot(x, y, 'ko', ms=point_size, alpha=point_alpha)
    ax.set_xlabel(xlabel or x_col.replace("_", " ").title())
    ax.set_ylabel(ylabel or y_col.replace("_", " ").title())
    ax.set_title(title or f"{len(df)} structures")

    plt.tight_layout()
    plt.show()


def plot_3d_plotly(
    df,
    x_col: str,
    y_col: str,
    z_col: str,
    color_col: str = None,
    title: str = None,
    opacity: float = 0.5,
    height: int = 800,
    size_max: int = 1,
    show: bool = True
):
    """
    Plot 3D scatter using plotly with optional color encoding.

    Parameters:
        df : pd.DataFrame — dataset
        x_col, y_col, z_col : str — column names for 3D axes
        color_col : str or None — column for coloring (defaults to z_col)
        title : str — plot title
        opacity : float — point opacity
        height : int — plot height in pixels
        size_max : int — max marker size
    """
    if df.empty:
        print("No data to plot.")
        return

    for col in [x_col, y_col, z_col]:
        if col not in df.columns:
            print(f"Missing column: {col}")
            return

    color_col = color_col or z_col

    fig = px.scatter_3d(
        df,
        x=x_col,
        y=y_col,
        z=z_col,
        color=color_col,
        opacity=opacity,
        title=title or f"3D Scatter: {len(df)} structures",
        height=height,
        size_max=size_max
    )

    fig.update_layout(scene=dict(
        xaxis_title=x_col.replace("_", " ").title(),
        yaxis_title=y_col.replace("_", " ").title(),
        zaxis_title=z_col.replace("_", " ").title()
    ))

    if show:
        fig.show()
    return fig
