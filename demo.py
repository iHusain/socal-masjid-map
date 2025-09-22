#!/usr/bin/env python3
"""
Demo script to test map generation with mock data.
This allows testing without requiring actual TIGER/Line shapefiles.
"""

import geopandas as gpd
from shapely.geometry import Polygon, LineString
from src.rendering.map_renderer import USMapRenderer
from src.export.exporters import MapExporter


def create_mock_counties():
    """Create mock county data for testing."""
    # Create a simple grid of counties
    counties = []
    for i in range(5):
        for j in range(4):
            # Create rectangular counties
            x_min, x_max = -120 + i * 10, -120 + (i + 1) * 10
            y_min, y_max = 30 + j * 5, 30 + (j + 1) * 5

            county_poly = Polygon(
                [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]
            )

            counties.append(
                {
                    "NAME": f"County_{i}_{j}",
                    "STATEFP": "06",  # California
                    "geometry": county_poly,
                }
            )

    return gpd.GeoDataFrame(counties, crs="EPSG:4326")


def create_mock_highways():
    """Create mock highway data for testing."""
    highways = []

    # Create some horizontal highways
    for i in range(3):
        y = 35 + i * 10
        line = LineString([(-120, y), (-80, y)])
        highways.append(
            {"FULLNAME": f"Interstate {i + 5}", "RTTYP": "I", "geometry": line}
        )

    # Create some vertical highways
    for i in range(2):
        x = -110 + i * 20
        line = LineString([(x, 30), (x, 50)])
        highways.append(
            {"FULLNAME": f"US Highway {i + 101}", "RTTYP": "U", "geometry": line}
        )

    return gpd.GeoDataFrame(highways, crs="EPSG:4326")


def create_mock_masjids():
    """Create mock masjid data for testing."""
    masjids = [
        {
            "name": "Central Valley Islamic Center",
            "latitude": 37.5,
            "longitude": -115.0,
        },
        {"name": "Bay Area Masjid", "latitude": 42.0, "longitude": -105.0},
        {"name": "Desert Community Mosque", "latitude": 35.0, "longitude": -95.0},
        {
            "name": "Mountain View Islamic Society",
            "latitude": 45.0,
            "longitude": -110.0,
        },
        {"name": "Coastal Masjid Al-Noor", "latitude": 40.0, "longitude": -85.0},
    ]

    return gpd.GeoDataFrame(
        masjids,
        geometry=gpd.points_from_xy(
            [m["longitude"] for m in masjids], [m["latitude"] for m in masjids]
        ),
        crs="EPSG:4326",
    )


def main():
    """Run the demo."""
    print("🗺️  US Masjid Map Demo")
    print("=" * 40)

    # Create mock data
    print("Creating mock data...")
    counties_gdf = create_mock_counties()
    highways_gdf = create_mock_highways()
    masjids_gdf = create_mock_masjids()

    print(f"  📍 {len(counties_gdf)} counties")
    print(f"  🛣️  {len(highways_gdf)} highways")
    print(f"  🕌 {len(masjids_gdf)} masjids")

    # Create renderer with lower DPI for demo
    print("\nRendering map...")
    renderer = USMapRenderer(dpi=100)  # Lower DPI for faster demo

    # Generate map
    fig, ax = renderer.render_complete_map(
        counties_gdf,
        highways_gdf,
        masjids_gdf,
        title="Demo: US Counties, Highways, and Masjids",
    )

    # Export map
    print("Exporting map...")
    exporter = MapExporter()

    # Export only PNG for demo
    png_path = exporter.export_png(fig, "demo_map", dpi=150)

    # Get file info
    info = exporter.get_file_info(png_path)
    print(f"  📁 Exported: {info['filename']} ({info['size_mb']} MB)")

    # Cleanup
    renderer.close()

    print("\n✅ Demo completed successfully!")
    print("Check the output directory for: demo_map.png")


if __name__ == "__main__":
    main()
