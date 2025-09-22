# US County/Highway/Masjid Map Generator

A Python application for generating large-format infographic maps showing US counties, highways, and masjid locations suitable for 4ft × 4ft printing.

## Features

- **US Counties**: Rendered with soft pastel warm colors and subtle boundaries
- **Primary Highways**: Clear labeling from TIGER/Line shapefiles
- **Masjid Locations**: Star markers with labels from coordinate data
- **High-Resolution Output**: 300 DPI suitable for large format printing
- **Multiple Formats**: PDF (vector), SVG (vector), and PNG (raster) exports

## Requirements

- Python 3.8+
- US Counties shapefile (`tl_2023_us_county.shp`)
- US Primary Roads shapefile (`tl_2023_us_primaryroads.shp`)
- Masjid coordinates (CSV or embedded data)

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd us_masjid_map
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install development dependencies (optional):**
```bash
pip install -r requirements-dev.txt
```

## Data Setup

1. **Download TIGER/Line Shapefiles:**
   - Place `tl_2023_us_county.shp` (and associated files) in `data/shapefiles/`
   - Place `tl_2023_us_primaryroads.shp` (and associated files) in `data/shapefiles/`

2. **Prepare Masjid Data:**
   - CSV format with columns: `name`, `latitude`, `longitude`
   - Or modify the sample data in `src/main.py`

## Usage

### Basic Usage
```bash
python src/main.py
```

### Programmatic Usage
```python
from src.main import USMasjidMapGenerator

# Custom masjid data
masjid_data = [
    {"name": "Masjid Name", "latitude": 40.7128, "longitude": -74.0060},
    # ... more masjids
]

# Generate map
generator = USMasjidMapGenerator()
exported_files = generator.run(
    masjid_data=masjid_data,
    title="Custom Map Title",
    output_filename="custom_map"
)
```

## Output

The application generates three file formats:
- **PNG**: High-resolution raster (300 DPI)
- **PDF**: Vector format for professional printing
- **SVG**: Scalable vector graphics

Files are saved to the `output/` directory.

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black src/ tests/
```

### Linting
```bash
flake8 src/ tests/
```

## Project Structure

```
us_masjid_map/
├── src/
│   ├── data/           # Data loading utilities
│   ├── processing/     # Data processing modules
│   ├── rendering/      # Map rendering functionality
│   ├── export/         # Export utilities
│   ├── utils/          # Configuration and helpers
│   └── main.py         # Main application
├── tests/              # Test suite
├── data/               # Input data directory
├── output/             # Generated maps
└── context.md          # Detailed project documentation
```

## Configuration

Map styling and dimensions can be customized in `src/utils/config.py`:
- Colors and styling
- Map dimensions and DPI
- Font sizes and styling
- Export settings

## License

MIT License - See LICENSE file for details.
