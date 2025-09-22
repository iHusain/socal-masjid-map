#!/usr/bin/env python3
"""Generate clean Southern California map with proper colors and aligned labels."""

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Configuration
MAP_WIDTH_INCHES = 24
MAP_HEIGHT_INCHES = 24
DPI = 300

# Distinct county colors
COUNTY_COLORS = {
    "Los Angeles": "#FFE5CC",    # Light peach
    "Orange": "#FFD1DC",         # Soft coral  
    "Riverside": "#FFF8DC",      # Pale yellow
    "San Bernardino": "#FFA07A"  # Light salmon
}
COUNTY_EDGE_COLOR = "#CCCCCC"
COUNTY_EDGE_WIDTH = 1.0
HIGHWAY_COLOR = "#FF6600"  # Orange for highways
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
    "address": "1027 E Philadelphia St, Ontario, CA 91761"
}

def main():
    print("🗺️  Southern California Map Generator")
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
            (counties['STATEFP'] == '06')
        ].copy()
        
        print(f"  ✅ Filtered to {len(target_counties)} counties")
        
        # Get bounds and filter highways
        bounds = target_counties.total_bounds
        buffer = 0.05
        
        # Filter highways to region - keep ALL highways, don't remove duplicates
        regional_highways = highways.cx[
            bounds[0]-buffer:bounds[2]+buffer, 
            bounds[1]-buffer:bounds[3]+buffer
        ].copy()
        
        # Filter for major highways only for labeling
        major_highways_for_labels = regional_highways[
            (regional_highways['RTTYP'].isin(['I', 'U'])) &  # Interstate and US routes only
            (regional_highways['FULLNAME'].notna()) &
            (regional_highways['FULLNAME'].str.len() > 0)
        ].copy()
        
        print(f"  ✅ Using {len(regional_highways)} highway segments")
        print(f"  ✅ Will label {len(major_highways_for_labels)} major highways")
        
        # Create single masjid GeoDataFrame
        masjid_gdf = gpd.GeoDataFrame(
            [MASJID],
            geometry=gpd.points_from_xy([MASJID['longitude']], [MASJID['latitude']]),
            crs='EPSG:4326'
        )
        
        # Ensure consistent CRS
        if target_counties.crs != 'EPSG:4326':
            target_counties = target_counties.to_crs('EPSG:4326')
        if regional_highways.crs != 'EPSG:4326':
            regional_highways = regional_highways.to_crs('EPSG:4326')
        
        print("Rendering map...")
        
        # Create figure
        fig, ax = plt.subplots(figsize=(MAP_WIDTH_INCHES, MAP_HEIGHT_INCHES), dpi=DPI)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        plt.tight_layout(pad=0)
        
        # Set extent
        ax.set_xlim(bounds[0]-buffer, bounds[2]+buffer)
        ax.set_ylim(bounds[1]-buffer, bounds[3]+buffer)
        
        # Render counties with specific colors
        print("  🏞️  Rendering counties with colors...")
        for idx, row in target_counties.iterrows():
            county_name = row['NAME']
            color = COUNTY_COLORS.get(county_name, "#F0F0F0")
            
            # Plot individual county
            gpd.GeoDataFrame([row]).plot(
                ax=ax,
                color=color,
                edgecolor=COUNTY_EDGE_COLOR,
                linewidth=COUNTY_EDGE_WIDTH,
                alpha=0.8
            )
            print(f"    Rendered {county_name} in {color}")
        
        # Render ALL highways (no filtering)
        print("  🛣️  Rendering all highways...")
        regional_highways.plot(
            ax=ax,
            color=HIGHWAY_COLOR,
            linewidth=HIGHWAY_WIDTH,
            alpha=0.7
        )
        
        # Add county labels
        print("  🏷️  Adding county labels...")
        for idx, row in target_counties.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(
                row['NAME'],
                xy=(centroid.x, centroid.y),
                ha='center',
                va='center',
                fontsize=18,
                weight='bold',
                color='#333333',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='white', alpha=0.9, edgecolor='gray')
            )
        
        # Add highway labels aligned with lines
        print("  🛣️  Adding highway labels...")
        labeled_highways = set()
        
        for idx, row in major_highways_for_labels.iterrows():
            highway_name = row['FULLNAME']
            
            # Skip if already labeled
            if highway_name in labeled_highways:
                continue
                
            if hasattr(row.geometry, 'coords'):
                coords = list(row.geometry.coords)
                if len(coords) >= 2:
                    # Get midpoint
                    mid_idx = len(coords) // 2
                    mid_point = coords[mid_idx]
                    
                    # Calculate angle of highway line for text rotation
                    if mid_idx > 0:
                        p1 = coords[mid_idx - 1]
                        p2 = coords[mid_idx]
                        angle = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))
                        
                        # Keep text readable (don't flip upside down)
                        if angle > 90:
                            angle -= 180
                        elif angle < -90:
                            angle += 180
                    else:
                        angle = 0
                    
                    # Add label aligned with highway
                    ax.annotate(
                        highway_name,
                        xy=mid_point,
                        ha='center',
                        va='center',
                        fontsize=10,
                        weight='bold',
                        color='#CC4400',
                        rotation=angle,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='orange')
                    )
                    
                    labeled_highways.add(highway_name)
                    
                    # Limit number of labels to avoid clutter
                    if len(labeled_highways) >= 12:
                        break
        
        # Render masjid
        print("  🕌 Rendering masjid...")
        masjid_gdf.plot(
            ax=ax,
            color=MASJID_COLOR,
            marker='*',
            markersize=MASJID_SIZE,
            alpha=1.0,
            edgecolors='white',
            linewidth=3
        )
        
        # Add masjid label
        ax.annotate(
            f"{MASJID['name']}\n{MASJID['address']}",
            xy=(MASJID['longitude'], MASJID['latitude']),
            xytext=(25, 25),
            textcoords='offset points',
            fontsize=14,
            ha='left',
            va='bottom',
            weight='bold',
            color='#1B5E20',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='white', alpha=0.95, edgecolor='green', linewidth=2)
        )
        
        # Add title
        ax.set_title(
            "Southern California Counties\nLos Angeles • Orange • Riverside • San Bernardino",
            fontsize=24,
            fontweight='bold',
            color='#212121',
            pad=30
        )
        
        print("Exporting maps...")
        
        # Export PNG
        png_path = "output/us_masjid_map_final.png"
        fig.savefig(
            png_path,
            format='png',
            dpi=DPI,
            bbox_inches='tight',
            pad_inches=0.3,
            facecolor='white',
            edgecolor='none'
        )
        
        # Export PDF
        pdf_path = "output/us_masjid_map_final.pdf"
        fig.savefig(
            pdf_path,
            format='pdf',
            bbox_inches='tight',
            pad_inches=0.3,
            facecolor='white',
            edgecolor='none'
        )
        
        # Get file sizes
        png_size = os.path.getsize(png_path) / (1024 * 1024)
        pdf_size = os.path.getsize(pdf_path) / (1024 * 1024)
        
        print(f"  📁 PNG: us_masjid_map_final.png ({png_size:.1f} MB)")
        print(f"  📁 PDF: us_masjid_map_final.pdf ({pdf_size:.1f} MB)")
        
        plt.close(fig)
        
        print("\n✅ Southern California map generated successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
