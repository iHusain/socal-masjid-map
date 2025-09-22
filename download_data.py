#!/usr/bin/env python3
"""Download TIGER/Line shapefiles for the Southern California map generator."""

import os
import urllib.request
import zipfile
from pathlib import Path

# TIGER/Line 2023 download URLs
DOWNLOADS = {
    "counties": {
        "url": "https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip",
        "filename": "tl_2023_us_county.zip"
    },
    "highways": {
        "url": "https://www2.census.gov/geo/tiger/TIGER2023/PRIMARYROADS/tl_2023_us_primaryroads.zip", 
        "filename": "tl_2023_us_primaryroads.zip"
    }
}

def download_file(url, filename):
    """Download a file with progress indication."""
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extract a zip file."""
    print(f"Extracting {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✅ Extracted {zip_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to extract {zip_path}: {e}")
        return False

def main():
    """Download and extract TIGER/Line shapefiles."""
    print("🗺️  TIGER/Line Shapefile Downloader")
    print("=" * 40)
    
    # Create data directory
    data_dir = Path("data/shapefiles")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Change to data directory
    os.chdir(data_dir)
    
    success_count = 0
    
    for name, info in DOWNLOADS.items():
        url = info["url"]
        filename = info["filename"]
        
        # Download file
        if download_file(url, filename):
            # Extract file
            if extract_zip(filename, "."):
                # Remove zip file
                os.remove(filename)
                print(f"🗑️  Removed {filename}")
                success_count += 1
            else:
                print(f"⚠️  Keeping {filename} due to extraction failure")
        
        print()
    
    if success_count == len(DOWNLOADS):
        print("🎉 All shapefiles downloaded and extracted successfully!")
        print("\nYou can now run: python socal_map.py")
    else:
        print(f"⚠️  {success_count}/{len(DOWNLOADS)} downloads successful")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()
