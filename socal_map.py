#!/usr/bin/env python3
"""Generate clean Southern California map with highway legend and color coding."""

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from matplotlib.patches import Rectangle

# Configuration
MAP_WIDTH_INCHES = 24
MAP_HEIGHT_INCHES = 24
DPI = 300

# Distinct county colors
COUNTY_COLORS = {
    "Los Angeles": "#FFE5CC",  # Light peach
    "Orange": "#FFD1DC",  # Soft coral
    "Riverside": "#FFF8DC",  # Pale yellow
    "San Bernardino": "#FFA07A",  # Light salmon
}
COUNTY_EDGE_COLOR = "#CCCCCC"
COUNTY_EDGE_WIDTH = 1.0

# Highway color coding by type
HIGHWAY_COLORS = {
    "I": "#FF0000",  # Red for Interstate
    "U": "#0066CC",  # Blue for US routes
    "S": "#FF6600",  # Orange for State routes
    "C": "#666666",  # Gray for County routes
}
HIGHWAY_WIDTH = 2.0
MASJID_COLOR = "#228B22"  # Green
MASJID_SIZE = 400

# Target counties
TARGET_COUNTIES = ["Los Angeles", "Orange", "Riverside", "San Bernardino"]

# Single masjid location
MASJID = {
    "name": "Orange County Masjid",
    "latitude": 34.0633,
    "longitude": -117.6509,
    "address": "1027 E Philadelphia St, Ontario, CA 91761",
}


def add_highway_legend(ax, bounds):
    """Add highway legend with color coding."""
    legend_x = bounds[2] - 1.5  # Right side of map
    legend_y = bounds[3] - 0.5  # Top of map

    # Legend background
    legend_width = 1.2
    legend_height = 1.0

    # Add white background for legend
    legend_bg = Rectangle(
        (legend_x - 0.1, legend_y - legend_height - 0.1),
        legend_width + 0.2,
        legend_height + 0.2,
        facecolor="white",
        edgecolor="black",
        alpha=0.9,
        linewidth=1,
    )
    ax.add_patch(legend_bg)

    # Legend title
    ax.text(
        legend_x + legend_width / 2,
        legend_y - 0.1,
        "HIGHWAYS",
        ha="center",
        va="top",
        fontsize=12,
        weight="bold",
    )

    # Legend items
    legend_items = [
        ("I", "Interstate", HIGHWAY_COLORS["I"]),
        ("U", "US Route", HIGHWAY_COLORS["U"]),
        ("S", "State Route", HIGHWAY_COLORS["S"]),
        ("C", "County Route", HIGHWAY_COLORS["C"]),
    ]

    y_offset = 0.25
    for i, (code, name, color) in enumerate(legend_items):
        y_pos = legend_y - y_offset - (i * 0.15)

        # Draw line sample
        ax.plot(
            [legend_x, legend_x + 0.3],
            [y_pos, y_pos],
            color=color,
            linewidth=3,
            alpha=0.8,
        )

        # Add text
        ax.text(
            legend_x + 0.4,
            y_pos,
            f"{code} - {name}",
            ha="left",
            va="center",
            fontsize=9,
            weight="bold",
        )


def main():
    print("🗺️  Southern California Map with Highway Legend")
    print("=" * 50)

    # Delete existing files
    for filename in ["us_masjid_map_final.png", "us_masjid_map_final.pdf"]:
        filepath = f"output/{filename}"
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"🗑️  Deleted: {filename}")

    try:
        # Load shapefiles
        print("Loading shapefiles...")
        counties = gpd.read_file("data/shapefiles/tl_2023_us_county.shp")
        highways = gpd.read_file("data/shapefiles/tl_2023_us_primaryroads.shp")

        # Filter for target counties in California
        target_counties = counties[
            (counties["NAME"].isin(TARGET_COUNTIES)) & (counties["STATEFP"] == "06")
        ].copy()

        print(f"  ✅ Filtered to {len(target_counties)} counties")

        # Get bounds and filter highways
        bounds = target_counties.total_bounds
        buffer = 0.05

        # Filter highways to region
        regional_highways = highways.cx[
            bounds[0] - buffer : bounds[2] + buffer,
            bounds[1] - buffer : bounds[3] + buffer,
        ].copy()

        # Add color column based on route type
        regional_highways["color"] = (
            regional_highways["RTTYP"].map(HIGHWAY_COLORS).fillna(HIGHWAY_COLORS["C"])
        )

        # Filter for major highways for labeling
        major_highways_for_labels = regional_highways[
            (regional_highways["RTTYP"].isin(["I", "U"]))
            & (regional_highways["FULLNAME"].notna())
            & (regional_highways["FULLNAME"].str.len() > 0)
        ].copy()

        print(f"  ✅ Using {len(regional_highways)} highway segments")
        print(f"  ✅ Will label {len(major_highways_for_labels)} major highways")

        # Create single masjid GeoDataFrame
        masjid_gdf = gpd.GeoDataFrame(
            [MASJID],
            geometry=gpd.points_from_xy([MASJID["longitude"]], [MASJID["latitude"]]),
            crs="EPSG:4326",
        )

        # Ensure consistent CRS
        if target_counties.crs != "EPSG:4326":
            target_counties = target_counties.to_crs("EPSG:4326")
        if regional_highways.crs != "EPSG:4326":
            regional_highways = regional_highways.to_crs("EPSG:4326")

        print("Rendering map with legend...")

        # Create figure
        fig, ax = plt.subplots(figsize=(MAP_WIDTH_INCHES, MAP_HEIGHT_INCHES), dpi=DPI)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_facecolor("white")
        fig.patch.set_facecolor("white")
        plt.tight_layout(pad=0)

        # Set extent
        ax.set_xlim(bounds[0] - buffer, bounds[2] + buffer)
        ax.set_ylim(bounds[1] - buffer, bounds[3] + buffer)

        # Render counties with specific colors
        print("  🏞️  Rendering counties with colors...")
        for idx, row in target_counties.iterrows():
            county_name = row["NAME"]
            color = COUNTY_COLORS.get(county_name, "#F0F0F0")

            gpd.GeoDataFrame([row]).plot(
                ax=ax,
                color=color,
                edgecolor=COUNTY_EDGE_COLOR,
                linewidth=COUNTY_EDGE_WIDTH,
                alpha=0.8,
            )

        # Render highways by type with color coding
        print("  🛣️  Rendering color-coded highways...")
        for highway_type in ["I", "U", "S", "C"]:
            type_highways = regional_highways[
                regional_highways["RTTYP"] == highway_type
            ]
            if not type_highways.empty:
                type_highways.plot(
                    ax=ax,
                    color=HIGHWAY_COLORS.get(highway_type, HIGHWAY_COLORS["C"]),
                    linewidth=HIGHWAY_WIDTH,
                    alpha=0.8,
                )
                print(f"    Rendered {len(type_highways)} {highway_type} routes")

        # Add county labels
        print("  🏷️  Adding county labels...")
        for idx, row in target_counties.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(
                row["NAME"],
                xy=(centroid.x, centroid.y),
                ha="center",
                va="center",
                fontsize=18,
                weight="bold",
                color="#333333",
                bbox=dict(
                    boxstyle="round,pad=0.6",
                    facecolor="white",
                    alpha=0.9,
                    edgecolor="gray",
                ),
            )

        # Add selective highway labels
        print("  🛣️  Adding highway labels...")
        labeled_highways = set()

        for idx, row in major_highways_for_labels.iterrows():
            highway_name = row["FULLNAME"]

            if highway_name in labeled_highways:
                continue

            if hasattr(row.geometry, "coords"):
                coords = list(row.geometry.coords)
                if len(coords) >= 2:
                    mid_idx = len(coords) // 2
                    mid_point = coords[mid_idx]

                    # Calculate angle
                    if mid_idx > 0:
                        p1 = coords[mid_idx - 1]
                        p2 = coords[mid_idx]
                        angle = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))

                        if angle > 90:
                            angle -= 180
                        elif angle < -90:
                            angle += 180
                    else:
                        angle = 0

                    # Get color for label border
                    route_color = HIGHWAY_COLORS.get(row["RTTYP"], HIGHWAY_COLORS["C"])

                    ax.annotate(
                        highway_name,
                        xy=mid_point,
                        ha="center",
                        va="center",
                        fontsize=10,
                        weight="bold",
                        color="white",
                        rotation=angle,
                        bbox=dict(
                            boxstyle="round,pad=0.3",
                            facecolor=route_color,
                            alpha=0.9,
                            edgecolor="white",
                        ),
                    )

                    labeled_highways.add(highway_name)

                    if len(labeled_highways) >= 12:
                        break

        # Add highway legend
        print("  📋 Adding highway legend...")
        add_highway_legend(ax, bounds)

        # Render masjid
        print("  🕌 Rendering masjid...")
        masjid_gdf.plot(
            ax=ax,
            color=MASJID_COLOR,
            marker="*",
            markersize=MASJID_SIZE,
            alpha=1.0,
            edgecolors="white",
            linewidth=3,
        )

        # Add masjid label
        ax.annotate(
            f"{MASJID['name']}\n{MASJID['address']}",
            xy=(MASJID["longitude"], MASJID["latitude"]),
            xytext=(25, 25),
            textcoords="offset points",
            fontsize=14,
            ha="left",
            va="bottom",
            weight="bold",
            color="#1B5E20",
            bbox=dict(
                boxstyle="round,pad=0.8",
                facecolor="white",
                alpha=0.95,
                edgecolor="green",
                linewidth=2,
            ),
        )

        # Add title
        ax.set_title(
            "Southern California Counties & Highway Network\nLos Angeles • Orange • Riverside • San Bernardino",
            fontsize=24,
            fontweight="bold",
            color="#212121",
            pad=30,
        )

        print("Exporting maps...")

        # Export PNG
        png_path = "output/us_masjid_map_final.png"
        fig.savefig(
            png_path,
            format="png",
            dpi=DPI,
            bbox_inches="tight",
            pad_inches=0.3,
            facecolor="white",
            edgecolor="none",
        )

        # Export PDF
        pdf_path = "output/us_masjid_map_final.pdf"
        fig.savefig(
            pdf_path,
            format="pdf",
            bbox_inches="tight",
            pad_inches=0.3,
            facecolor="white",
            edgecolor="none",
        )

        # Get file sizes
        png_size = os.path.getsize(png_path) / (1024 * 1024)
        pdf_size = os.path.getsize(pdf_path) / (1024 * 1024)

        print(f"  📁 PNG: us_masjid_map_final.png ({png_size:.1f} MB)")
        print(f"  📁 PDF: us_masjid_map_final.pdf ({pdf_size:.1f} MB)")

        plt.close(fig)

        print("\n✅ Southern California map with highway legend generated!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
