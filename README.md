# Southern California Counties & Masjid Map Generator

A Python application for generating high-resolution maps of Southern California counties (Los Angeles, Orange, Riverside, San Bernardino) with highway networks and a specific masjid location for large-format printing.

## Current Functionality

This project generates detailed maps showing:
- **4 Southern California Counties**: Los Angeles, Orange, Riverside, San Bernardino
- **Highway Network**: All primary roads with individual highway labels
- **Single Masjid Location**: 1027 E Philadelphia St, Ontario, CA 91761
- **County Labels**: Clear identification of each county
- **Professional Quality**: 300 DPI output suitable for large format printing

## Features

- **Focused Regional View**: Zoomed to Southern California region only
- **Accurate Data**: Uses official TIGER/Line 2023 shapefiles from US Census
- **Comprehensive Labeling**: Counties and highways clearly labeled
- **Single Masjid Marker**: Green star at exact Ontario, CA address
- **Multiple Output Formats**: High-resolution PNG and vector PDF
- **Print Ready**: Optimized for professional large-format printing

## Requirements

- Python 3.8+
- US Counties shapefile (`tl_2023_us_county.shp`) - ✅ Included
- US Primary Roads shapefile (`tl_2023_us_primaryroads.shp`) - ✅ Included

## Quick Start

1. **Navigate to project:**
```bash
cd us_masjid_map
```

2. **Activate virtual environment:**
```bash
source venv/bin/activate
```

3. **Generate the map:**
```bash
python socal_map.py
```

## Output

The application generates:
- **PNG**: `us_masjid_map_final.png` (~2.4 MB) - High-resolution raster
- **PDF**: `us_masjid_map_final.pdf` (~0.5 MB) - Vector format for printing

Files are automatically saved to the `output/` directory, replacing any previous versions.

## Map Specifications

### Geographic Coverage
- **Counties**: Los Angeles, Orange, Riverside, San Bernardino (California)
- **Data Source**: TIGER/Line 2023 shapefiles
- **Coordinate System**: WGS84 (EPSG:4326)

### Visual Elements
- **County Colors**: Soft pastel warm palette with subtle boundaries
- **Highway Network**: Dark gray lines with yellow name labels
- **County Labels**: Blue boxes with county names at centroids
- **Masjid Marker**: Green star with white label box showing name and address

### Technical Specifications
- **Dimensions**: 24" × 24" (configurable to 48" × 48")
- **Resolution**: 300 DPI for print quality
- **File Formats**: PNG (raster) and PDF (vector)

## Project Structure

```
us_masjid_map/
├── socal_map.py           # Main map generator (current)
├── data/
│   └── shapefiles/        # TIGER/Line shapefiles
│       ├── tl_2023_us_county.*
│       └── tl_2023_us_primaryroads.*
├── output/                # Generated maps
│   ├── us_masjid_map_final.png
│   └── us_masjid_map_final.pdf
├── src/                   # Original modular codebase
├── tests/                 # Test suite (15 passing tests)
└── demo.py               # Demo with mock data
```

## Configuration

Key settings in `socal_map.py`:
- **MAP_WIDTH_INCHES / MAP_HEIGHT_INCHES**: Output dimensions
- **DPI**: Print resolution (300 for high quality)
- **TARGET_COUNTIES**: Counties to include in map
- **MASJID**: Single masjid location and details
- **Colors**: County, highway, and marker styling

## Data Processing

1. **Load Shapefiles**: Counties (3,235 total) and highways (17,458 segments)
2. **Filter by Region**: Extract only the 4 target counties and regional highways
3. **Coordinate Alignment**: Ensure consistent CRS across all data layers
4. **Render Layers**: Counties → Highways → Labels → Masjid marker
5. **Export**: Generate both PNG and PDF formats

## Development History

- **Initial Setup**: Modular architecture with comprehensive testing
- **Real Data Integration**: TIGER/Line shapefiles successfully loaded
- **Regional Focus**: Filtered from full US to Southern California only
- **Single Location**: Updated to show only Ontario, CA masjid
- **Enhanced Labeling**: Added county and highway name labels

## Usage Examples

### Basic Generation
```bash
python socal_map.py
```

### Custom Masjid Location
Edit the `MASJID` dictionary in `socal_map.py`:
```python
MASJID = {
    "name": "Your Masjid Name",
    "latitude": 34.0633,
    "longitude": -117.6509,
    "address": "Your Address"
}
```

### Different Counties
Modify `TARGET_COUNTIES` list:
```python
TARGET_COUNTIES = ["Your", "Target", "Counties"]
```

## Testing

Run the test suite:
```bash
pytest  # 15 tests passing
```

Run demo with mock data:
```bash
python demo.py
```

## License

MIT License - See LICENSE file for details.

## Data Sources

- **Counties**: US Census Bureau TIGER/Line Shapefiles 2023
- **Highways**: US Census Bureau TIGER/Line Primary Roads 2023
- **Masjid Location**: 1027 E Philadelphia St, Ontario, CA 91761
