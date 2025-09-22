#!/usr/bin/env python3
"""Generate the real US Masjid Map with actual TIGER/Line shapefiles."""

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# Configuration
MAP_WIDTH_INCHES = 24  # Smaller for testing
MAP_HEIGHT_INCHES = 24
DPI = 150

COUNTY_COLORS = [
    "#FFE5CC", "#FFD1DC", "#FFF8DC", "#FFA07A", "#F5F5DC",
    "#FFEFD5", "#FFE4E1", "#FAFAD2"
]
COUNTY_EDGE_COLOR = "#CCCCCC"
COUNTY_EDGE_WIDTH = 0.3
HIGHWAY_COLOR = "#404040"
HIGHWAY_WIDTH = 0.8
MASJID_COLOR = "#228B22"
MASJID_SIZE = 50

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
    
    try:
        # Load real shapefiles
        print("Loading shapefiles...")
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
        
        print("Rendering map (this may take several minutes)...")
        
        # Create figure
        fig, ax = plt.subplots(figsize=(MAP_WIDTH_INCHES, MAP_HEIGHT_INCHES), dpi=DPI)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.tight_layout(pad=0)
        
        # Set extent based on continental US
        ax.set_xlim(-130, -65)
        ax.set_ylim(20, 50)
        
        # Render counties with random colors
        print("  Rendering counties...")
        n_counties = len(counties)
        color_indices = np.random.choice(len(COUNTY_COLORS), n_counties)
        colors = [COUNTY_COLORS[i] for i in color_indices]
        
        counties.plot(
            ax=ax,
            color=colors,
            edgecolor=COUNTY_EDGE_COLOR,
            linewidth=COUNTY_EDGE_WIDTH,
            alpha=0.8
        )
        
        # Render highways
        print("  Rendering highways...")
        highways.plot(
            ax=ax,
            color=HIGHWAY_COLOR,
            linewidth=HIGHWAY_WIDTH,
            alpha=0.8
        )
        
        # Render masjids
        print("  Rendering masjids...")
        masjids.plot(
            ax=ax,
            color=MASJID_COLOR,
            marker='*',
            markersize=MASJID_SIZE,
            alpha=0.9
        )
        
        # Add masjid labels
        for idx, row in masjids.iterrows():
            ax.annotate(
                row['name'],
                xy=(row.geometry.x, row.geometry.y),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=6,
                ha='left',
                va='bottom',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7)
            )
        
        # Add title
        ax.set_title(
            "US Counties, Highways, and Masjids - 2024",
            fontsize=16,
            fontweight='bold',
            pad=20
        )
        
        print("Exporting map...")
        
        # Export PNG
        output_path = "output/us_masjid_map_real.png"
        fig.savefig(
            output_path,
            format='png',
            dpi=DPI,
            bbox_inches='tight',
            pad_inches=0.1,
            facecolor='white',
            edgecolor='none'
        )
        
        # Get file size
        import os
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  📁 Exported: us_masjid_map_real.png ({file_size:.1f} MB)")
        
        plt.close(fig)
        
        print("\n✅ Real map generated successfully!")
        print("📂 Check the output directory for the generated map.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
