"""Main map rendering functionality."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
import geopandas as gpd
import numpy as np
from typing import Optional, Tuple, List
from ..utils.config import (
    MAP_WIDTH_INCHES,
    MAP_HEIGHT_INCHES,
    PRINT_DPI,
    COUNTY_COLORS,
    COUNTY_EDGE_COLOR,
    COUNTY_EDGE_WIDTH,
    COUNTY_ALPHA,
    HIGHWAY_COLOR,
    HIGHWAY_WIDTH,
    MASJID_COLOR,
    MASJID_SIZE,
    MASJID_SYMBOL,
    TITLE_FONT_SIZE,
)


class USMapRenderer:
    """Render the complete US map with counties, highways, and masjids."""

    def __init__(self, dpi: int = PRINT_DPI):
        """
        Initialize the map renderer.

        Args:
            dpi: Dots per inch for rendering
        """
        self.dpi = dpi
        self.fig = None
        self.ax = None

    def create_figure(self) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create the main figure and axes for the map.

        Returns:
            Tuple of (figure, axes) objects
        """
        self.fig, self.ax = plt.subplots(
            figsize=(MAP_WIDTH_INCHES, MAP_HEIGHT_INCHES), dpi=self.dpi
        )

        # Remove axes and set clean appearance
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        # Set tight layout
        plt.tight_layout(pad=0)

        return self.fig, self.ax

    def render_counties(self, counties_gdf: gpd.GeoDataFrame) -> None:
        """
        Render US counties with pastel colors.

        Args:
            counties_gdf: GeoDataFrame containing county geometries
        """
        if self.ax is None:
            raise ValueError("Must call create_figure() first")

        # Create color mapping for counties
        n_counties = len(counties_gdf)
        color_indices = np.random.choice(len(COUNTY_COLORS), n_counties)
        colors = [COUNTY_COLORS[i] for i in color_indices]

        # Plot counties
        counties_gdf.plot(
            ax=self.ax,
            color=colors,
            edgecolor=COUNTY_EDGE_COLOR,
            linewidth=COUNTY_EDGE_WIDTH,
            alpha=COUNTY_ALPHA,
        )

    def render_highways(self, highways_gdf: gpd.GeoDataFrame) -> None:
        """
        Render highways/primary roads.

        Args:
            highways_gdf: GeoDataFrame containing highway geometries
        """
        if self.ax is None:
            raise ValueError("Must call create_figure() first")

        # Plot highways
        highways_gdf.plot(
            ax=self.ax, color=HIGHWAY_COLOR, linewidth=HIGHWAY_WIDTH, alpha=0.8
        )

    def render_masjids(self, masjids_gdf: gpd.GeoDataFrame) -> None:
        """
        Render masjid locations with markers and labels.

        Args:
            masjids_gdf: GeoDataFrame containing masjid points
        """
        if self.ax is None:
            raise ValueError("Must call create_figure() first")

        # Plot masjid points
        masjids_gdf.plot(
            ax=self.ax,
            color=MASJID_COLOR,
            marker=MASJID_SYMBOL,
            markersize=MASJID_SIZE,
            alpha=0.9,
        )

        # Add labels for each masjid
        for idx, row in masjids_gdf.iterrows():
            self.ax.annotate(
                row["name"],
                xy=(row.geometry.x, row.geometry.y),
                xytext=(5, 5),  # Offset from point
                textcoords="offset points",
                fontsize=8,
                ha="left",
                va="bottom",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7),
            )

    def add_title(self, title: str = "US Counties, Highways, and Masjids") -> None:
        """
        Add title to the map.

        Args:
            title: Map title text
        """
        if self.ax is None:
            raise ValueError("Must call create_figure() first")

        self.ax.set_title(title, fontsize=TITLE_FONT_SIZE, fontweight="bold", pad=20)

    def set_extent(self, gdf: gpd.GeoDataFrame, buffer_percent: float = 0.02) -> None:
        """
        Set map extent based on data bounds.

        Args:
            gdf: GeoDataFrame to base extent on
            buffer_percent: Buffer around data as percentage of extent
        """
        if self.ax is None:
            raise ValueError("Must call create_figure() first")

        bounds = gdf.total_bounds
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]

        buffer_x = width * buffer_percent
        buffer_y = height * buffer_percent

        self.ax.set_xlim(bounds[0] - buffer_x, bounds[2] + buffer_x)
        self.ax.set_ylim(bounds[1] - buffer_y, bounds[3] + buffer_y)

    def render_complete_map(
        self,
        counties_gdf: gpd.GeoDataFrame,
        highways_gdf: gpd.GeoDataFrame,
        masjids_gdf: gpd.GeoDataFrame,
        title: Optional[str] = None,
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Render the complete map with all layers.

        Args:
            counties_gdf: County geometries
            highways_gdf: Highway geometries
            masjids_gdf: Masjid points
            title: Optional map title

        Returns:
            Tuple of (figure, axes) objects
        """
        # Create figure
        self.create_figure()

        # Set extent based on counties (largest layer)
        self.set_extent(counties_gdf)

        # Render layers in order (bottom to top)
        self.render_counties(counties_gdf)
        self.render_highways(highways_gdf)
        self.render_masjids(masjids_gdf)

        # Add title if provided
        if title:
            self.add_title(title)

        return self.fig, self.ax

    def close(self) -> None:
        """Close the figure to free memory."""
        if self.fig:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
