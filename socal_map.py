#!/usr/bin/env python3
"""Generate map for Southern California counties with single masjid and labels."""

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Configuration
MAP_WIDTH_INCHES = 24
MAP_HEIGHT_INCHES = 24
DPI = 300

COUNTY_COLORS = [
    "#FFE5CC", "#FFD1DC", "#FFF8DC", "#FFA07A"
]
COUNTY_EDGE_COLOR = "#CCCCCC"
COUNTY_EDGE_WIDTH = 0.5
HIGHWAY_COLOR = "#404040"
HIGHWAY_WIDTH = 1.5
MASJID_COLOR = "#228B22"
MASJID_SIZE = 300

# Target counties
TARGET_COUNTIES = ["Los Angeles", "Orange", "Riverside", "San Bernardino"]

# Single masjid location: 1027 E Philadelphia St, Ontario, CA 91761
# Coordinates for Ontario, CA
MASJID = {
    "name": "Masjid Ontario", 
    "latitude": 34.0633, 
    "longitude": -117.6509,
    "address": "1027 E Philadelphia St, Ontario, CA 91761"
}

def main():
    print("🗺️  Southern California Counties Map Generator")
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
            (counties['NAME'].isin(TARGET_COUNTIES)) & 
            (counties['STATEFP'] == '06')  # California FIPS code
        ]
        
        print(f"  ✅ Filtered to {len(target_counties)} counties: {', '.join(TARGET_COUNTIES)}")
        
        # Get bounds of target counties
        bounds = target_counties.total_bounds
        buffer = 0.1
        
        # Filter highways to the region
        regional_highways = highways.cx[
            bounds[0]-buffer:bounds[2]+buffer, 
            bounds[1]-buffer:bounds[3]+buffer
        ]
        
        print(f"  ✅ Filtered to {len(regional_highways)} highway segments in region")
        
        # Create single masjid GeoDataFrame
        masjid_gdf = gpd.GeoDataFrame(
            [MASJID],
            geometry=gpd.points_from_xy([MASJID['longitude']], [MASJID['latitude']]),
            crs='EPSG:4326'
        )
        print(f"  ✅ Created masjid at: {MASJID['address']}")
        
        # Ensure consistent CRS
        if target_counties.crs != 'EPSG:4326':
            target_counties = target_counties.to_crs('EPSG:4326')
        if regional_highways.crs != 'EPSG:4326':
            regional_highways = regional_highways.to_crs('EPSG:4326')
        
        print("Rendering Southern California map...")
        
        # Create figure
        fig, ax = plt.subplots(figsize=(MAP_WIDTH_INCHES, MAP_HEIGHT_INCHES), dpi=DPI)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.tight_layout(pad=0)
        
        # Set extent to target counties with buffer
        ax.set_xlim(bounds[0]-buffer, bounds[2]+buffer)
        ax.set_ylim(bounds[1]-buffer, bounds[3]+buffer)
        
        # Render counties
        print("  🏞️  Rendering counties...")
        target_counties.plot(
            ax=ax,
            color=COUNTY_COLORS,
            edgecolor=COUNTY_EDGE_COLOR,
            linewidth=COUNTY_EDGE_WIDTH,
            alpha=0.8
        )
        
        # Render highways
        print("  🛣️  Rendering highways...")
        regional_highways.plot(
            ax=ax,
            color=HIGHWAY_COLOR,
            linewidth=HIGHWAY_WIDTH,
            alpha=0.8
        )
        
        # Add county labels
        print("  🏷️  Adding county labels...")
        for idx, row in target_counties.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(
                f"{row['NAME']} County",
                xy=(centroid.x, centroid.y),
                ha='center',
                va='center',
                fontsize=18,
                weight='bold',
                bbox=dict(boxstyle='round,pad=0.8', facecolor='lightblue', alpha=0.8)
            )
        
        # Add highway labels
        print("  🛣️  Adding highway labels...")
        for idx, row in regional_highways.iterrows():
            if 'FULLNAME' in row and pd.notna(row['FULLNAME']) and row['FULLNAME'].strip():
                # Get midpoint of highway for label placement
                if hasattr(row.geometry, 'coords'):
                    coords = list(row.geometry.coords)
                    if len(coords) > 1:
                        mid_idx = len(coords) // 2
                        mid_point = coords[mid_idx]
                        
                        ax.annotate(
                            row['FULLNAME'],
                            xy=mid_point,
                            ha='center',
                            va='center',
                            fontsize=10,
                            weight='bold',
                            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                            rotation=0
                        )
        
        # Render masjid
        print("  🕌 Rendering masjid...")
        masjid_gdf.plot(
            ax=ax,
            color=MASJID_COLOR,
            marker='*',
            markersize=MASJID_SIZE,
            alpha=0.9
        )
        
        # Add masjid label
        ax.annotate(
            f"{MASJID['name']}\n{MASJID['address']}",
            xy=(MASJID['longitude'], MASJID['latitude']),
            xytext=(15, 15),
            textcoords='offset points',
            fontsize=14,
            ha='left',
            va='bottom',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='white', alpha=0.9),
            weight='bold'
        )
        
        # Add title
        ax.set_title(
            "Southern California: Los Angeles, Orange, Riverside & San Bernardino Counties\nHighways and Masjid Location",
            fontsize=22,
            fontweight='bold',
            pad=40
        )
        
        print("Exporting maps...")
        
        # Export PNG
        png_path = "output/us_masjid_map_final.png"
        fig.savefig(
            png_path,
            format='png',
            dpi=DPI,
            bbox_inches='tight',
            pad_inches=0.2,
            facecolor='white',
            edgecolor='none'
        )
        
        # Export PDF
        pdf_path = "output/us_masjid_map_final.pdf"
        fig.savefig(
            pdf_path,
            format='pdf',
            bbox_inches='tight',
            pad_inches=0.2,
            facecolor='white',
            edgecolor='none'
        )
        
        # Get file sizes
        png_size = os.path.getsize(png_path) / (1024 * 1024)
        pdf_size = os.path.getsize(pdf_path) / (1024 * 1024)
        
        print(f"  📁 PNG: us_masjid_map_final.png ({png_size:.1f} MB)")
        print(f"  📁 PDF: us_masjid_map_final.pdf ({pdf_size:.1f} MB)")
        
        plt.close(fig)
        
        print("\n✅ Southern California map with labels generated successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
