#!/usr/bin/env python3
"""Generate the real US Masjid Map with actual TIGER/Line shapefiles."""

import sys
import os
sys.path.append('src')

import geopandas as gpd
from rendering.map_renderer import USMapRenderer
from export.exporters import MapExporter

# Sample masjid data
MASJIDS = [
    {"name": "Islamic Center of Greater Cincinnati", "latitude": 39.1031, "longitude": -84.5120},
    {"name": "Masjid Al-Noor NYC", "latitude": 40.7128, "longitude": -74.0060},
    {"name": "Islamic Society of Boston", "latitude": 42.3601, "longitude": -71.0589},
    {"name": "Dar Al-Hijrah VA", "latitude": 38.9072, "longitude": -77.0369},
    {"name": "ICSC Los Angeles", "latitude": 34.0522, "longitude": -118.2437},
    {"name": "Masjid Al-Farah Chicago", "latitude": 41.8781, "longitude": -87.6298},
    {"name": "Islamic Center of Nashville", "latitude": 36.1627, "longitude": -86.7816},
    {"name": "Masjid Al-Islam Phoenix", "latitude": 33.4484, "longitude": -112.0740},
    {"name": "Islamic Center of Detroit", "latitude": 42.3314, "longitude": -83.0458},
    {"name": "Masjid Al-Taqwa Houston", "latitude": 29.7604, "longitude": -95.3698},
]

def main():
    print("🗺️  US Masjid Map Generator - Real Data")
    print("=" * 50)
    
    # Load real shapefiles
    print("Loading shapefiles...")
    
    try:
        counties = gpd.read_file("data/shapefiles/tl_2023_us_county.shp")
        print(f"  ✅ Loaded {len(counties)} counties")
        
        highways = gpd.read_file("data/shapefiles/tl_2023_us_primaryroads.shp")
        print(f"  ✅ Loaded {len(highways)} highway segments")
        
        # Create masjid GeoDataFrame
        masjids = gpd.GeoDataFrame(
            MASJIDS,
            geometry=gpd.points_from_xy([m['longitude'] for m in MASJIDS], 
                                       [m['latitude'] for m in MASJIDS]),
            crs='EPSG:4326'
        )
        print(f"  ✅ Created {len(masjids)} masjid points")
        
        # Ensure consistent CRS
        print("Ensuring consistent coordinate systems...")
        if counties.crs != 'EPSG:4326':
            counties = counties.to_crs('EPSG:4326')
        if highways.crs != 'EPSG:4326':
            highways = highways.to_crs('EPSG:4326')
        
        print("Rendering map (this may take a few minutes)...")
        
        # Create renderer with lower DPI for initial test
        renderer = USMapRenderer(dpi=150)  # Lower DPI for faster processing
        
        # Generate map
        fig, ax = renderer.render_complete_map(
            counties,
            highways,
            masjids,
            title="US Counties, Highways, and Masjids - 2024"
        )
        
        print("Exporting map...")
        exporter = MapExporter()
        
        # Export PNG first (fastest)
        png_path = exporter.export_png(fig, "us_masjid_map_real", dpi=150)
        
        # Get file info
        info = exporter.get_file_info(png_path)
        print(f"  📁 Exported: {info['filename']} ({info['size_mb']} MB)")
        
        # Cleanup
        renderer.close()
        
        print("\n✅ Real map generated successfully!")
        print("📂 Check the output directory for the generated map.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
