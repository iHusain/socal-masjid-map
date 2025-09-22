# Southern California Counties & Masjid Map Generator

A Python application for generating high-resolution maps of Southern California counties with highway networks and masjid location, featuring Google Maps-inspired clean design and aligned highway labeling.

## 🗺️ Current Functionality

This project generates professional-quality maps showing:
- **4 Southern California Counties**: Los Angeles (peach), Orange (coral), Riverside (yellow), San Bernardino (salmon)
- **Complete Highway Network**: 532 highway segments with continuous orange lines
- **Aligned Highway Labels**: Text rotated to match highway direction for easy identification
- **Single Masjid Location**: Orange County Masjid at 1027 E Philadelphia St, Ontario, CA 91761
- **Clean Design**: Google Maps-inspired styling with proper color coding

## ✨ Key Features

- **Distinct County Colors**: Each county has a unique pastel color for clear identification
- **Smart Highway Labeling**: Labels align with highway direction, limited to major routes (Interstate/US)
- **Professional Quality**: 300 DPI output suitable for large-format printing (24" × 24")
- **Clean Visual Design**: Minimal clutter with strategic label placement
- **Multiple Formats**: High-resolution PNG and vector PDF outputs
- **Automatic File Management**: Replaces previous versions on each generation

## 🚀 Quick Start

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

## 📊 Output Specifications

### Generated Files
- **PNG**: `us_masjid_map_final.png` (~1.4 MB) - High-resolution raster
- **PDF**: `us_masjid_map_final.pdf` (~0.4 MB) - Vector format for printing

### Map Features
- **Dimensions**: 24" × 24" at 300 DPI (7,200 × 7,200 pixels)
- **Geographic Coverage**: Los Angeles, Orange, Riverside, San Bernardino counties
- **Highway Network**: Complete road system with 12 major highway labels
- **Visual Style**: Clean, professional design suitable for presentations and printing

## 🎨 Design Elements

### County Color Scheme
- **Los Angeles**: Light peach (#FFE5CC)
- **Orange**: Soft coral (#FFD1DC)  
- **Riverside**: Pale yellow (#FFF8DC)
- **San Bernardino**: Light salmon (#FFA07A)

### Highway Styling
- **Color**: Orange (#FF6600) for visibility
- **Width**: 2.0 for clear definition
- **Labels**: Rotated text aligned with highway direction
- **Coverage**: Interstate and US routes labeled

### Masjid Marker
- **Symbol**: Green star (#228B22) with white border
- **Size**: Large (400) for clear visibility
- **Label**: "Orange County Masjid" with full address

## 🛠️ Technical Implementation

### Data Sources
- **Counties**: US Census TIGER/Line 2023 shapefiles (3,235 → filtered to 4)
- **Highways**: US Census TIGER/Line Primary Roads 2023 (17,458 → filtered to 532 regional)
- **Coordinate System**: WGS84 (EPSG:4326)

### Processing Pipeline
1. **Load**: TIGER/Line shapefiles for counties and highways
2. **Filter**: Extract 4 target counties (California FIPS code 06)
3. **Clip**: Highway segments to regional bounds
4. **Render**: Counties (individual colors) → Highways (all segments) → Labels (selective)
5. **Export**: PNG and PDF with white background

### Label Algorithm
- **Highway Labels**: Rotated to match line direction using coordinate geometry
- **Collision Avoidance**: Limits to 12 major highways to prevent overcrowding
- **Smart Positioning**: Uses midpoint of highway segments for optimal placement

## 📁 Project Structure

```
us_masjid_map/
├── socal_map.py           # Main generator (PRODUCTION)
├── data/shapefiles/       # TIGER/Line data (✅ included)
│   ├── tl_2023_us_county.*
│   └── tl_2023_us_primaryroads.*
├── output/                # Generated maps
│   ├── us_masjid_map_final.png
│   └── us_masjid_map_final.pdf
├── src/                   # Original modular codebase
├── tests/                 # Test suite (15 passing tests)
├── venv/                  # Python virtual environment
└── README.md             # This file
```

## ⚙️ Configuration Options

### Easy Customization
```python
# County selection
TARGET_COUNTIES = ["Los Angeles", "Orange", "Riverside", "San Bernardino"]

# Masjid location
MASJID = {
    "name": "Orange County Masjid",
    "latitude": 34.0633,
    "longitude": -117.6509,
    "address": "1027 E Philadelphia St, Ontario, CA 91761"
}

# Output settings
MAP_WIDTH_INCHES = 24    # Adjustable size
DPI = 300               # Print quality
```

### Color Customization
```python
COUNTY_COLORS = {
    "Los Angeles": "#FFE5CC",
    "Orange": "#FFD1DC", 
    "Riverside": "#FFF8DC",
    "San Bernardino": "#FFA07A"
}
```

## 🧪 Development & Testing

### Run Tests
```bash
pytest  # 15 tests passing
```

### Code Quality
```bash
black socal_map.py      # Format code
flake8 socal_map.py     # Lint code
```

### Demo Version
```bash
python demo.py          # Mock data demo
```

## 📈 Performance Metrics

- **Processing Time**: ~30 seconds for complete map generation
- **Memory Usage**: ~2GB during rendering
- **File Sizes**: PNG 1.4MB, PDF 0.4MB
- **Data Processing**: 532 highway segments, 4 counties, 1 masjid location

## 🎯 Use Cases

- **Community Outreach**: Visual representation of masjid location relative to counties
- **Educational Materials**: Geographic reference for Southern California
- **Presentation Graphics**: High-quality maps for reports and presentations
- **Print Materials**: Suitable for posters, banners, and handouts

## 📋 Requirements

- **Python 3.8+**
- **Dependencies**: geopandas, matplotlib, shapely, pandas, numpy
- **Data**: TIGER/Line shapefiles (included)
- **System**: ~4GB RAM recommended for processing

## 🔄 Version History

- **v1.0**: Initial modular architecture with full US coverage
- **v2.0**: Regional focus on Southern California counties
- **v3.0**: Single masjid location with enhanced labeling
- **v4.0**: Google Maps-inspired design with aligned highway labels
- **v4.1**: Fixed county colors and continuous highway lines (CURRENT)

## 📄 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test: `python socal_map.py`
4. Commit: `git commit -m "feat: description"`
5. Push and create pull request

## 📞 Support

For issues or questions:
- Check existing issues in the repository
- Create new issue with map output and error details
- Include system information and Python version
