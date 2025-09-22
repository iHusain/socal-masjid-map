"""Data loading utilities for shapefiles and masjid coordinates."""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
import geopandas as gpd
import pandas as pd
from ..utils.config import SHAPEFILES_DIR, COUNTIES_SHAPEFILE, HIGHWAYS_SHAPEFILE


class ShapefileLoader:
    """Load and validate shapefile data."""
    
    @staticmethod
    def load_counties(shapefile_path: Optional[str] = None) -> gpd.GeoDataFrame:
        """
        Load US counties shapefile.
        
        Args:
            shapefile_path: Optional custom path to counties shapefile
            
        Returns:
            GeoDataFrame containing county geometries and attributes
            
        Raises:
            FileNotFoundError: If shapefile doesn't exist
            ValueError: If shapefile is invalid or empty
        """
        if shapefile_path is None:
            shapefile_path = os.path.join(SHAPEFILES_DIR, COUNTIES_SHAPEFILE)
        
        if not os.path.exists(shapefile_path):
            raise FileNotFoundError(f"Counties shapefile not found: {shapefile_path}")
        
        try:
            gdf = gpd.read_file(shapefile_path)
            
            if gdf.empty:
                raise ValueError("Counties shapefile is empty")
            
            # Ensure we have geometry column
            if gdf.geometry.isna().all():
                raise ValueError("Counties shapefile contains no valid geometries")
            
            return gdf
            
        except Exception as e:
            raise ValueError(f"Failed to load counties shapefile: {str(e)}")
    
    @staticmethod
    def load_highways(shapefile_path: Optional[str] = None) -> gpd.GeoDataFrame:
        """
        Load US primary roads/highways shapefile.
        
        Args:
            shapefile_path: Optional custom path to highways shapefile
            
        Returns:
            GeoDataFrame containing highway geometries and attributes
            
        Raises:
            FileNotFoundError: If shapefile doesn't exist
            ValueError: If shapefile is invalid or empty
        """
        if shapefile_path is None:
            shapefile_path = os.path.join(SHAPEFILES_DIR, HIGHWAYS_SHAPEFILE)
        
        if not os.path.exists(shapefile_path):
            raise FileNotFoundError(f"Highways shapefile not found: {shapefile_path}")
        
        try:
            gdf = gpd.read_file(shapefile_path)
            
            if gdf.empty:
                raise ValueError("Highways shapefile is empty")
            
            if gdf.geometry.isna().all():
                raise ValueError("Highways shapefile contains no valid geometries")
            
            return gdf
            
        except Exception as e:
            raise ValueError(f"Failed to load highways shapefile: {str(e)}")


class MasjidLoader:
    """Load and process masjid location data."""
    
    @staticmethod
    def load_from_csv(csv_path: str) -> gpd.GeoDataFrame:
        """
        Load masjid locations from CSV file.
        
        Args:
            csv_path: Path to CSV file with masjid coordinates
            
        Returns:
            GeoDataFrame with masjid points
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV format is invalid
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Masjid CSV file not found: {csv_path}")
        
        try:
            df = pd.read_csv(csv_path)
            
            # Check required columns
            required_cols = ['name', 'latitude', 'longitude']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            # Create GeoDataFrame from coordinates
            gdf = gpd.GeoDataFrame(
                df,
                geometry=gpd.points_from_xy(df.longitude, df.latitude),
                crs='EPSG:4326'
            )
            
            return gdf
            
        except Exception as e:
            raise ValueError(f"Failed to load masjid CSV: {str(e)}")
    
    @staticmethod
    def load_from_list(masjid_data: List[Dict[str, Any]]) -> gpd.GeoDataFrame:
        """
        Load masjid locations from list of dictionaries.
        
        Args:
            masjid_data: List of dicts with 'name', 'latitude', 'longitude'
            
        Returns:
            GeoDataFrame with masjid points
            
        Raises:
            ValueError: If data format is invalid
        """
        if not masjid_data:
            raise ValueError("Masjid data list is empty")
        
        try:
            df = pd.DataFrame(masjid_data)
            
            # Check required columns
            required_cols = ['name', 'latitude', 'longitude']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            # Create GeoDataFrame from coordinates
            gdf = gpd.GeoDataFrame(
                df,
                geometry=gpd.points_from_xy(df.longitude, df.latitude),
                crs='EPSG:4326'
            )
            
            return gdf
            
        except Exception as e:
            raise ValueError(f"Failed to load masjid data: {str(e)}")


def validate_crs_consistency(*gdfs: gpd.GeoDataFrame) -> bool:
    """
    Check if all GeoDataFrames have consistent CRS.
    
    Args:
        *gdfs: Variable number of GeoDataFrames to check
        
    Returns:
        True if all have same CRS, False otherwise
    """
    if not gdfs:
        return True
    
    first_crs = gdfs[0].crs
    return all(gdf.crs == first_crs for gdf in gdfs)


def ensure_crs(gdf: gpd.GeoDataFrame, target_crs: str = 'EPSG:4326') -> gpd.GeoDataFrame:
    """
    Ensure GeoDataFrame has the specified CRS.
    
    Args:
        gdf: Input GeoDataFrame
        target_crs: Target coordinate reference system
        
    Returns:
        GeoDataFrame with specified CRS
    """
    if gdf.crs is None:
        return gdf.set_crs(target_crs)
    elif gdf.crs != target_crs:
        return gdf.to_crs(target_crs)
    else:
        return gdf
