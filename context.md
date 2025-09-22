# US County/Highway/Masjid Map Project - Context & Plan

## Project Goals & Requirements

### Primary Goal
Create a large-format infographic-style map (4 ft × 4 ft banner) showing:
- US Counties with soft pastel warm colors and subtle boundaries
- US Primary Roads (Highways) with clear labeling and no overlap
- Masjid locations with star/masjid icons and labels
- High-resolution output suitable for professional printing

### Specific Requirements

#### Counties
- Use `tl_2023_us_county.shp` shapefile
- Soft pastel warm color palette
- Subtle but visible boundaries
- Clean, readable appearance

#### Highways
- Use `tl_2023_us_primaryroads.shp` shapefile
- Clear highway labels without clutter
- Intelligent label placement to avoid overlap
- Major highways prominently displayed

#### Masjid Markers
- Star or masjid icon symbols
- Individual labels for each masjid
- Clear visibility against county background
- Coordinate-based placement from CSV/list

#### Output Specifications
- 4 ft × 4 ft (48" × 48") print dimensions
- High DPI for crisp printing (300+ DPI)
- Multiple formats: PDF (vector), SVG (vector), PNG (raster)
- Professional print quality

## Tech Stack & Dependencies

### Core Technologies
- **Python 3.8+**: Primary development language
- **geopandas**: Geospatial data manipulation and analysis
- **matplotlib**: Primary plotting and visualization
- **shapely**: Geometric operations and spatial analysis
- **contextily**: Optional basemap integration
- **pandas**: Data manipulation for masjid coordinates

### Development Tools
- **pytest**: Unit testing framework
- **black**: Code formatting
- **flake8**: Code linting and style checking
- **mypy**: Type checking (optional)

### Additional Libraries
- **numpy**: Numerical operations
- **pillow**: Image processing for custom icons
- **descartes**: Matplotlib polygon plotting (if needed)

## System Architecture

### Data Flow
```
Input Data → Data Loaders → Processors → Map Renderer → Export Engine → Output Files
```

### Component Architecture
1. **Data Layer**: Load and validate shapefiles and masjid coordinates
2. **Processing Layer**: Clean, filter, and prepare geospatial data
3. **Rendering Layer**: Create map visualization with proper styling
4. **Export Layer**: Generate high-resolution outputs in multiple formats

### Module Structure
```
us_masjid_map/
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loaders.py      # Load shapefiles and masjid data
│   │   └── validators.py   # Data validation and cleaning
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── counties.py     # County data processing
│   │   ├── highways.py     # Highway data processing
│   │   └── masjids.py      # Masjid data processing
│   ├── rendering/
│   │   ├── __init__.py
│   │   ├── map_renderer.py # Main map creation
│   │   ├── styling.py      # Colors, fonts, styling
│   │   └── labels.py       # Label placement algorithms
│   ├── export/
│   │   ├── __init__.py
│   │   └── exporters.py    # PDF, SVG, PNG export
│   └── utils/
│       ├── __init__.py
│       ├── config.py       # Configuration constants
│       └── helpers.py      # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_data/
│   ├── test_processing/
│   ├── test_rendering/
│   └── test_export/
├── data/                   # Input data directory
│   ├── shapefiles/
│   └── masjids/
├── output/                 # Generated maps
├── requirements.txt
├── requirements-dev.txt
├── setup.py
├── pyproject.toml
├── .gitignore
├── README.md
└── context.md
```

## File Structure Outline

### Source Code Organization
- **Modular design**: Each component has single responsibility
- **Clear separation**: Data, processing, rendering, export layers
- **Testable units**: Each module can be tested independently
- **Configuration-driven**: Colors, sizes, DPI settings in config

### Data Organization
- **Input data**: Organized by type (shapefiles, coordinates)
- **Processed data**: Intermediate results cached if needed
- **Output data**: Multiple formats in organized structure

## Coding Standards

### Python Style
- **PEP 8 compliance**: Enforced by flake8
- **Black formatting**: Consistent code style
- **Type hints**: For all function signatures
- **Docstrings**: Google-style documentation
- **Maximum line length**: 88 characters

### Code Quality
- **Single responsibility**: Each function has one clear purpose
- **Error handling**: Comprehensive exception handling
- **Input validation**: All inputs validated and sanitized
- **No hardcoded values**: Configuration-driven approach
- **Logging**: Proper logging for debugging and monitoring

### Security Practices
- **No secrets in code**: All sensitive data externalized
- **Input sanitization**: Validate all file paths and data
- **Safe file operations**: Proper error handling for I/O
- **Dependency management**: Pin versions, security scanning

## Testing Strategy

### Unit Testing
- **100% function coverage**: Every function tested
- **Edge case testing**: Boundary conditions and error cases
- **Mock external dependencies**: File I/O, network calls
- **Fast execution**: Tests run quickly for continuous feedback

### Integration Testing
- **End-to-end workflows**: Complete data pipeline testing
- **Output validation**: Verify generated files are correct
- **Performance testing**: Ensure reasonable execution times
- **Visual regression**: Compare output images when possible

### Test Data
- **Sample shapefiles**: Small test datasets
- **Mock masjid data**: Synthetic coordinates for testing
- **Expected outputs**: Reference images for comparison

## Implementation Phases

### Phase 1: Foundation (MVP)
1. Project setup and basic structure
2. Data loading for counties and highways
3. Basic map rendering with matplotlib
4. Simple export to PNG

### Phase 2: Core Features
1. Masjid data integration
2. Styling system (colors, fonts)
3. Label placement algorithms
4. PDF and SVG export

### Phase 3: Polish & Optimization
1. Advanced label collision detection
2. Performance optimization
3. High-DPI output optimization
4. Comprehensive testing

### Phase 4: Production Ready
1. Error handling and validation
2. Configuration management
3. Documentation completion
4. Final testing and QA

## Color Palette & Styling

### County Colors (Pastel Warm Palette)
- Light peach (#FFE5CC)
- Soft coral (#FFD1DC)
- Pale yellow (#FFF8DC)
- Light salmon (#FFA07A)
- Warm beige (#F5F5DC)

### Highway Styling
- Color: Dark gray (#404040)
- Width: Proportional to highway importance
- Labels: Black text with white outline

### Masjid Styling
- Icon: Green star or crescent symbol
- Size: Clearly visible but not overwhelming
- Labels: Dark text with light background

## Technical Specifications

### Map Dimensions
- **Print size**: 48" × 48" (4 ft × 4 ft)
- **DPI**: 300 for print quality
- **Pixel dimensions**: 14,400 × 14,400 pixels
- **Aspect ratio**: 1:1 (square)

### Performance Targets
- **Processing time**: < 5 minutes for full map generation
- **Memory usage**: < 4GB RAM
- **File sizes**: PDF < 50MB, PNG < 100MB

## Success Metrics
- All tests passing (100%)
- Clean linting results (0 errors)
- High-quality print output
- Readable labels at print size
- Professional appearance
- Efficient processing time
