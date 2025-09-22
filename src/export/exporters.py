"""Export functionality for saving maps in various formats."""

import os
from pathlib import Path
import matplotlib.pyplot as plt
from typing import List, Optional
from ..utils.config import OUTPUT_DIR, EXPORT_FORMATS, PNG_DPI, PDF_DPI


class MapExporter:
    """Export maps to various formats with high quality settings."""
    
    def __init__(self, output_dir: str = OUTPUT_DIR):
        """
        Initialize the exporter.
        
        Args:
            output_dir: Directory to save exported files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export_png(
        self, 
        fig: plt.Figure, 
        filename: str, 
        dpi: int = PNG_DPI
    ) -> str:
        """
        Export figure as high-resolution PNG.
        
        Args:
            fig: Matplotlib figure to export
            filename: Output filename (without extension)
            dpi: Dots per inch for PNG export
            
        Returns:
            Path to exported file
        """
        output_path = self.output_dir / f"{filename}.png"
        
        fig.savefig(
            output_path,
            format='png',
            dpi=dpi,
            bbox_inches='tight',
            pad_inches=0.1,
            facecolor='white',
            edgecolor='none'
        )
        
        return str(output_path)
    
    def export_pdf(
        self, 
        fig: plt.Figure, 
        filename: str
    ) -> str:
        """
        Export figure as vector PDF.
        
        Args:
            fig: Matplotlib figure to export
            filename: Output filename (without extension)
            
        Returns:
            Path to exported file
        """
        output_path = self.output_dir / f"{filename}.pdf"
        
        fig.savefig(
            output_path,
            format='pdf',
            bbox_inches='tight',
            pad_inches=0.1,
            facecolor='white',
            edgecolor='none'
        )
        
        return str(output_path)
    
    def export_svg(
        self, 
        fig: plt.Figure, 
        filename: str
    ) -> str:
        """
        Export figure as vector SVG.
        
        Args:
            fig: Matplotlib figure to export
            filename: Output filename (without extension)
            
        Returns:
            Path to exported file
        """
        output_path = self.output_dir / f"{filename}.svg"
        
        fig.savefig(
            output_path,
            format='svg',
            bbox_inches='tight',
            pad_inches=0.1,
            facecolor='white',
            edgecolor='none'
        )
        
        return str(output_path)
    
    def export_all_formats(
        self, 
        fig: plt.Figure, 
        base_filename: str,
        formats: Optional[List[str]] = None
    ) -> List[str]:
        """
        Export figure in all specified formats.
        
        Args:
            fig: Matplotlib figure to export
            base_filename: Base filename (without extension)
            formats: List of formats to export (default: all supported)
            
        Returns:
            List of paths to exported files
        """
        if formats is None:
            formats = EXPORT_FORMATS
        
        exported_files = []
        
        for fmt in formats:
            if fmt.lower() == 'png':
                path = self.export_png(fig, base_filename)
            elif fmt.lower() == 'pdf':
                path = self.export_pdf(fig, base_filename)
            elif fmt.lower() == 'svg':
                path = self.export_svg(fig, base_filename)
            else:
                print(f"Warning: Unsupported format '{fmt}' skipped")
                continue
            
            exported_files.append(path)
            print(f"Exported: {path}")
        
        return exported_files
    
    def get_file_info(self, filepath: str) -> dict:
        """
        Get information about an exported file.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Dictionary with file information
        """
        path = Path(filepath)
        
        if not path.exists():
            return {"error": "File not found"}
        
        stat = path.stat()
        
        return {
            "filename": path.name,
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "format": path.suffix.lower(),
            "exists": True
        }
