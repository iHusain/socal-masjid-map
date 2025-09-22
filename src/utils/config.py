"""Configuration constants for the US Masjid Map project."""

# Map dimensions and DPI settings
MAP_WIDTH_INCHES = 48  # 4 feet
MAP_HEIGHT_INCHES = 48  # 4 feet
PRINT_DPI = 300
DISPLAY_DPI = 100

# Color palette - Pastel warm colors for counties
COUNTY_COLORS = [
    "#FFE5CC",  # Light peach
    "#FFD1DC",  # Soft coral
    "#FFF8DC",  # Pale yellow
    "#FFA07A",  # Light salmon
    "#F5F5DC",  # Warm beige
    "#FFEFD5",  # Papaya whip
    "#FFE4E1",  # Misty rose
    "#FAFAD2",  # Light goldenrod yellow
]

# Highway styling
HIGHWAY_COLOR = "#404040"  # Dark gray
HIGHWAY_WIDTH = 1.5
HIGHWAY_LABEL_COLOR = "#000000"  # Black
HIGHWAY_LABEL_OUTLINE = "#FFFFFF"  # White outline

# Masjid styling
MASJID_COLOR = "#228B22"  # Forest green
MASJID_SIZE = 100  # Marker size
MASJID_SYMBOL = "*"  # Star symbol
MASJID_LABEL_COLOR = "#000000"
MASJID_LABEL_SIZE = 8

# County styling
COUNTY_EDGE_COLOR = "#CCCCCC"  # Light gray
COUNTY_EDGE_WIDTH = 0.5
COUNTY_ALPHA = 0.8

# Font settings
TITLE_FONT_SIZE = 24
LABEL_FONT_SIZE = 10
HIGHWAY_LABEL_SIZE = 8

# File paths
DATA_DIR = "data"
SHAPEFILES_DIR = f"{DATA_DIR}/shapefiles"
MASJIDS_DIR = f"{DATA_DIR}/masjids"
OUTPUT_DIR = "output"

# Shapefile names
COUNTIES_SHAPEFILE = "tl_2023_us_county.shp"
HIGHWAYS_SHAPEFILE = "tl_2023_us_primaryroads.shp"

# Export settings
EXPORT_FORMATS = ["png", "pdf", "svg"]
PNG_DPI = PRINT_DPI
PDF_DPI = PRINT_DPI
