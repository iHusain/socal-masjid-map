"""Main application for generating the US Masjid Map."""

import sys
from typing import List, Dict, Any, Optional
from data.loaders import ShapefileLoader, MasjidLoader, ensure_crs
from rendering.map_renderer import USMapRenderer
from export.exporters import MapExporter


# Sample masjid data (replace with actual data)
SAMPLE_MASJIDS = [
    {"name": "Islamic Center of Greater Cincinnati", "latitude": 39.1031, "longitude": -84.5120},
    {"name": "Masjid Al-Noor", "latitude": 40.7128, "longitude": -74.0060},
    {"name": "Islamic Society of Boston", "latitude": 42.3601, "longitude": -71.0589},
    {"name": "Dar Al-Hijrah", "latitude": 38.9072, "longitude": -77.0369},
    {"name": "Islamic Center of Southern California", "latitude": 34.0522, "longitude": -118.2437},
    {"name": "Masjid Al-Farah", "latitude": 41.8781, "longitude": -87.6298},
    {"name": "Islamic Center of Nashville", "latitude": 36.1627, "longitude": -86.7816},
    {"name": "Masjid Al-Islam", "latitude": 33.4484, "longitude": -112.0740},
    {"name": "Islamic Center of Detroit", "latitude": 42.3314, "longitude": -83.0458},
    {"name": "Masjid Al-Taqwa", "latitude": 29.7604, "longitude": -95.3698},
]


class USMasjidMapGenerator:
    """Main class for generating the US Masjid Map."""
    
    def __init__(self):
        """Initialize the map generator."""
        self.counties_gdf = None
        self.highways_gdf = None
        self.masjids_gdf = None
        self.renderer = None
        self.exporter = None
    
    def load_data(self, masjid_data: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Load all required data for the map.
        
        Args:
            masjid_data: Optional list of masjid dictionaries
        """
        print("Loading data...")
        
        try:
            # Load shapefiles
            print("  Loading counties shapefile...")
            self.counties_gdf = ShapefileLoader.load_counties()
            
            print("  Loading highways shapefile...")
            self.highways_gdf = ShapefileLoader.load_highways()
            
            # Load masjid data
            print("  Loading masjid data...")
            if masjid_data is None:
                masjid_data = SAMPLE_MASJIDS
            
            self.masjids_gdf = MasjidLoader.load_from_list(masjid_data)
            
            # Ensure consistent CRS (WGS84)
            print("  Ensuring consistent coordinate systems...")
            self.counties_gdf = ensure_crs(self.counties_gdf, 'EPSG:4326')
            self.highways_gdf = ensure_crs(self.highways_gdf, 'EPSG:4326')
            self.masjids_gdf = ensure_crs(self.masjids_gdf, 'EPSG:4326')
            
            print(f"  Loaded {len(self.counties_gdf)} counties")
            print(f"  Loaded {len(self.highways_gdf)} highway segments")
            print(f"  Loaded {len(self.masjids_gdf)} masjids")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
    
    def generate_map(self, title: Optional[str] = None) -> None:
        """
        Generate the complete map.
        
        Args:
            title: Optional map title
        """
        if any(gdf is None for gdf in [self.counties_gdf, self.highways_gdf, self.masjids_gdf]):
            raise ValueError("Data must be loaded first. Call load_data().")
        
        print("Generating map...")
        
        # Initialize renderer
        self.renderer = USMapRenderer()
        
        # Render complete map
        fig, ax = self.renderer.render_complete_map(
            self.counties_gdf,
            self.highways_gdf,
            self.masjids_gdf,
            title=title
        )
        
        print("Map generation complete.")
    
    def export_map(self, filename: str = "us_masjid_map") -> List[str]:
        """
        Export the map in all formats.
        
        Args:
            filename: Base filename for exports
            
        Returns:
            List of exported file paths
        """
        if self.renderer is None or self.renderer.fig is None:
            raise ValueError("Map must be generated first. Call generate_map().")
        
        print("Exporting map...")
        
        # Initialize exporter
        self.exporter = MapExporter()
        
        # Export in all formats
        exported_files = self.exporter.export_all_formats(
            self.renderer.fig,
            filename
        )
        
        # Print file information
        print("\nExported files:")
        for filepath in exported_files:
            info = self.exporter.get_file_info(filepath)
            print(f"  {info['filename']}: {info['size_mb']} MB")
        
        return exported_files
    
    def cleanup(self) -> None:
        """Clean up resources."""
        if self.renderer:
            self.renderer.close()
    
    def run(
        self, 
        masjid_data: Optional[List[Dict[str, Any]]] = None,
        title: Optional[str] = None,
        output_filename: str = "us_masjid_map"
    ) -> List[str]:
        """
        Run the complete map generation process.
        
        Args:
            masjid_data: Optional masjid data
            title: Optional map title
            output_filename: Base filename for output
            
        Returns:
            List of exported file paths
        """
        try:
            self.load_data(masjid_data)
            self.generate_map(title)
            exported_files = self.export_map(output_filename)
            return exported_files
        
        except Exception as e:
            print(f"Error during map generation: {e}")
            raise
        
        finally:
            self.cleanup()


def main():
    """Main entry point."""
    print("US Masjid Map Generator")
    print("=" * 50)
    
    # Create generator
    generator = USMasjidMapGenerator()
    
    try:
        # Run complete process
        exported_files = generator.run(
            title="US Counties, Highways, and Masjids",
            output_filename="us_masjid_map_2024"
        )
        
        print(f"\n✅ Successfully generated map!")
        print(f"📁 Output files: {len(exported_files)}")
        
    except Exception as e:
        print(f"\n❌ Failed to generate map: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
