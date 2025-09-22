#!/usr/bin/env python3
"""Generate the final high-resolution US Masjid Map for 4ft x 4ft printing."""

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# Final print configuration
MAP_WIDTH_INCHES = 48  # 4 feet
MAP_HEIGHT_INCHES = 48  # 4 feet
PRINT_DPI = 300  # High resolution for printing

COUNTY_COLORS = [
    "#FFE5CC", "#FFD1DC", "#FFF8DC", "#FFA07A", "#F5F5DC",
    "#FFEFD5", "#FFE4E1", "#FAFAD2"
]
COUNTY_EDGE_COLOR = "#CCCCCC"
COUNTY_EDGE_WIDTH = 0.2
HIGHWAY_COLOR = "#404040"
HIGHWAY_WIDTH = 1.0
MASJID_COLOR = "#228B22"
MASJID_SIZE = 150

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
    print("🖨️  Final High-Resolution US Masjid Map Generator")
    print("=" * 60)
    print(f"📐 Dimensions: {MAP_WIDTH_INCHES}\" x {MAP_HEIGHT_INCHES}\" at {PRINT_DPI} DPI")
    print(f"📊 Output size: {MAP_WIDTH_INCHES * PRINT_DPI} x {MAP_HEIGHT_INCHES * PRINT_DPI} pixels")
    
    try:
        # Load real shapefiles
        print("\nLoading shapefiles...")
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
        
        print("\\n🎨 Rendering final high-resolution map...")
        print("⚠️  This will take several minutes and use significant memory...")
        
        # Create high-resolution figure
        fig, ax = plt.subplots(figsize=(MAP_WIDTH_INCHES, MAP_HEIGHT_INCHES), dpi=PRINT_DPI)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.tight_layout(pad=0)
        
        # Set extent for continental US
        ax.set_xlim(-130, -65)
        ax.set_ylim(20, 50)
        
        # Render counties
        print("  🏞️  Rendering counties...")
        n_counties = len(counties)
        np.random.seed(42)  # Consistent colors
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
        print("  🛣️  Rendering highways...")
        highways.plot(
            ax=ax,
            color=HIGHWAY_COLOR,
            linewidth=HIGHWAY_WIDTH,
            alpha=0.8
        )
        
        # Render masjids
        print("  🕌 Rendering masjids...")
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
                xytext=(8, 8),
                textcoords='offset points',
                fontsize=12,
                ha='left',
                va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8),
                weight='bold'
            )
        
        # Add title
        ax.set_title(
            "United States: Counties, Highways, and Masjids",
            fontsize=48,
            fontweight='bold',
            pad=40
        )
        
        print("\\n💾 Exporting final maps...")
        
        # Export PNG
        print("  📄 Exporting PNG...")
        png_path = "output/us_masjid_map_final.png"
        fig.savefig(
            png_path,
            format='png',
            dpi=PRINT_DPI,
            bbox_inches='tight',
            pad_inches=0.2,
            facecolor='white',
            edgecolor='none'
        )
        
        # Export PDF
        print("  📄 Exporting PDF...")
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
        import os
        png_size = os.path.getsize(png_path) / (1024 * 1024)
        pdf_size = os.path.getsize(pdf_path) / (1024 * 1024)
        
        print(f"  📁 PNG: us_masjid_map_final.png ({png_size:.1f} MB)")
        print(f"  📁 PDF: us_masjid_map_final.pdf ({pdf_size:.1f} MB)")
        
        plt.close(fig)
        
        print("\\n🎉 Final high-resolution map generated successfully!")
        print("🖨️  Ready for 4ft x 4ft professional printing!")
        
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
