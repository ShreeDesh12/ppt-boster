"""
Storage module for managing presentation files
"""
from .factory import StorageFactory
from .file_storage import FileStorage

__all__ = [
    "StorageFactory",
    "FileStorage",
]
