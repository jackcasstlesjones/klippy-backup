"""
Klippy - Kindle Clippings to Markdown Converter
"""

__version__ = '0.1.0'

# Make the main function available at the package level
try:
    from .klippy import main
except ImportError:
    # Fallback for direct imports
    from klippy import main
