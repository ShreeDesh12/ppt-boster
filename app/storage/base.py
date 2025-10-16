"""
Base storage interface
"""
from abc import ABC, abstractmethod
from typing import Optional


class BaseStorage(ABC):
    """Abstract base class for storage backends"""

    @abstractmethod
    def save(self, file_path: str, presentation_id: str, content: bytes = None) -> str:
        """
        Save a file to storage

        Args:
            file_path: Path to the file to save
            presentation_id: Unique identifier for the presentation
            content: Optional file content as bytes (if file_path is a temp file)

        Returns:
            Storage path or URL where file was saved
        """
        pass

    @abstractmethod
    def get(self, presentation_id: str) -> Optional[str]:
        """
        Get the file path for a presentation

        Args:
            presentation_id: Unique identifier for the presentation

        Returns:
            File path if exists, None otherwise
        """
        pass

    @abstractmethod
    def delete(self, presentation_id: str) -> bool:
        """
        Delete a file from storage

        Args:
            presentation_id: Unique identifier for the presentation

        Returns:
            True if deleted successfully, False otherwise
        """
        pass

    @abstractmethod
    def exists(self, presentation_id: str) -> bool:
        """
        Check if a file exists in storage

        Args:
            presentation_id: Unique identifier for the presentation

        Returns:
            True if exists, False otherwise
        """
        pass
