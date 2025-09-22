"""Tests for data loading functionality."""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

from src.data.loaders import (
    ShapefileLoader,
    MasjidLoader,
    validate_crs_consistency,
    ensure_crs,
)


class TestShapefileLoader:
    """Test cases for ShapefileLoader."""

    def test_load_counties_file_not_found(self):
        """Test loading counties when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            ShapefileLoader.load_counties("nonexistent.shp")

    @patch("geopandas.read_file")
    @patch("os.path.exists")
    def test_load_counties_empty_file(self, mock_exists, mock_read_file):
        """Test loading empty counties shapefile."""
        mock_exists.return_value = True
        mock_read_file.return_value = gpd.GeoDataFrame()

        with pytest.raises(ValueError, match="Counties shapefile is empty"):
            ShapefileLoader.load_counties("test.shp")

    @patch("geopandas.read_file")
    @patch("os.path.exists")
    def test_load_counties_success(self, mock_exists, mock_read_file):
        """Test successful counties loading."""
        mock_exists.return_value = True

        # Create mock GeoDataFrame
        mock_gdf = gpd.GeoDataFrame(
            {
                "NAME": ["County1", "County2"],
                "geometry": [
                    Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
                    Polygon([(1, 0), (2, 0), (2, 1), (1, 1)]),
                ],
            }
        )
        mock_read_file.return_value = mock_gdf

        result = ShapefileLoader.load_counties("test.shp")

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 2
        assert "NAME" in result.columns

    def test_load_highways_file_not_found(self):
        """Test loading highways when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            ShapefileLoader.load_highways("nonexistent.shp")


class TestMasjidLoader:
    """Test cases for MasjidLoader."""

    def test_load_from_csv_file_not_found(self):
        """Test loading from non-existent CSV."""
        with pytest.raises(FileNotFoundError):
            MasjidLoader.load_from_csv("nonexistent.csv")

    def test_load_from_csv_success(self):
        """Test successful CSV loading."""
        # Create temporary CSV file
        csv_data = """name,latitude,longitude
Masjid 1,40.7128,-74.0060
Masjid 2,34.0522,-118.2437"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_data)
            f.flush()

            try:
                result = MasjidLoader.load_from_csv(f.name)

                assert isinstance(result, gpd.GeoDataFrame)
                assert len(result) == 2
                assert "name" in result.columns
                assert result.crs == "EPSG:4326"

                # Check geometry
                assert all(isinstance(geom, Point) for geom in result.geometry)

            finally:
                os.unlink(f.name)

    def test_load_from_csv_missing_columns(self):
        """Test CSV with missing required columns."""
        csv_data = """name,lat,lng
Masjid 1,40.7128,-74.0060"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_data)
            f.flush()

            try:
                with pytest.raises(ValueError, match="Missing required columns"):
                    MasjidLoader.load_from_csv(f.name)
            finally:
                os.unlink(f.name)

    def test_load_from_list_success(self):
        """Test successful loading from list."""
        masjid_data = [
            {"name": "Masjid 1", "latitude": 40.7128, "longitude": -74.0060},
            {"name": "Masjid 2", "latitude": 34.0522, "longitude": -118.2437},
        ]

        result = MasjidLoader.load_from_list(masjid_data)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 2
        assert result.crs == "EPSG:4326"

    def test_load_from_list_empty(self):
        """Test loading from empty list."""
        with pytest.raises(ValueError, match="Masjid data list is empty"):
            MasjidLoader.load_from_list([])

    def test_load_from_list_missing_columns(self):
        """Test loading from list with missing columns."""
        masjid_data = [{"name": "Masjid 1", "lat": 40.7128}]

        with pytest.raises(ValueError, match="Missing required columns"):
            MasjidLoader.load_from_list(masjid_data)


class TestUtilityFunctions:
    """Test utility functions."""

    def test_validate_crs_consistency_empty(self):
        """Test CRS validation with no GeoDataFrames."""
        assert validate_crs_consistency() is True

    def test_validate_crs_consistency_same(self):
        """Test CRS validation with same CRS."""
        gdf1 = gpd.GeoDataFrame({"geometry": [Point(0, 0)]}, crs="EPSG:4326")
        gdf2 = gpd.GeoDataFrame({"geometry": [Point(1, 1)]}, crs="EPSG:4326")

        assert validate_crs_consistency(gdf1, gdf2) is True

    def test_validate_crs_consistency_different(self):
        """Test CRS validation with different CRS."""
        gdf1 = gpd.GeoDataFrame({"geometry": [Point(0, 0)]}, crs="EPSG:4326")
        gdf2 = gpd.GeoDataFrame({"geometry": [Point(1, 1)]}, crs="EPSG:3857")

        assert validate_crs_consistency(gdf1, gdf2) is False

    def test_ensure_crs_no_crs(self):
        """Test ensuring CRS when none exists."""
        gdf = gpd.GeoDataFrame({"geometry": [Point(0, 0)]})
        result = ensure_crs(gdf, "EPSG:4326")

        assert result.crs == "EPSG:4326"

    def test_ensure_crs_same_crs(self):
        """Test ensuring CRS when already correct."""
        gdf = gpd.GeoDataFrame({"geometry": [Point(0, 0)]}, crs="EPSG:4326")
        result = ensure_crs(gdf, "EPSG:4326")

        assert result.crs == "EPSG:4326"
        assert result.equals(gdf)
