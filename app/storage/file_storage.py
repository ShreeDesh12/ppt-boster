"""
Local file system storage implementation
"""
import os
import shutil
import logging
from typing import Optional
from .base import BaseStorage
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class FileStorage(BaseStorage):
    """Local file system storage backend"""

    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize file storage

        Args:
            base_dir: Base directory for storing files.
                     Defaults to settings.output_dir
        """
        self.base_dir = base_dir or settings.output_dir
        os.makedirs(self.base_dir, exist_ok=True)
        logger.info(f"FileStorage initialized with base_dir: {self.base_dir}")

    def save(self, file_path: str, presentation_id: str, content: bytes = None) -> str:
        """
        Save a file to local storage

        Args:
            file_path: Path to the file to save
            presentation_id: Unique identifier for the presentation
            content: Optional file content as bytes

        Returns:
            Absolute path where file was saved
        """
        filename = f"{presentation_id}.pptx"
        destination = os.path.join(self.base_dir, filename)

        try:
            if content:
                # Save from bytes content
                with open(destination, 'wb') as f:
                    f.write(content)
                logger.info(f"Saved presentation from bytes to: {destination}")
            elif os.path.exists(file_path):
                # Copy from existing file
                shutil.copy2(file_path, destination)
                logger.info(f"Copied presentation from {file_path} to: {destination}")
            else:
                # File path is already the destination
                if os.path.abspath(file_path) != os.path.abspath(destination):
                    shutil.move(file_path, destination)
                    logger.info(f"Moved presentation from {file_path} to: {destination}")
                else:
                    logger.info(f"Presentation already at destination: {destination}")

            return os.path.abspath(destination)

        except Exception as e:
            logger.error(f"Error saving file: {str(e)}", exc_info=True)
            raise

    def get(self, presentation_id: str) -> Optional[str]:
        """
        Get the file path for a presentation

        Args:
            presentation_id: Unique identifier for the presentation

        Returns:
            Absolute file path if exists, None otherwise
        """
        filename = f"{presentation_id}.pptx"
        file_path = os.path.join(self.base_dir, filename)

        if os.path.exists(file_path):
            logger.debug(f"Found presentation: {file_path}")
            return os.path.abspath(file_path)
        else:
            logger.debug(f"Presentation not found: {file_path}")
            return None

    def delete(self, presentation_id: str) -> bool:
        """
        Delete a file from storage

        Args:
            presentation_id: Unique identifier for the presentation

        Returns:
            True if deleted successfully, False otherwise
        """
        file_path = self.get(presentation_id)

        if not file_path:
            logger.warning(f"Cannot delete non-existent presentation: {presentation_id}")
            return False

        try:
            os.remove(file_path)
            logger.info(f"Deleted presentation: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {str(e)}", exc_info=True)
            return False

    def exists(self, presentation_id: str) -> bool:
        """
        Check if a file exists in storage

        Args:
            presentation_id: Unique identifier for the presentation

        Returns:
            True if exists, False otherwise
        """
        return self.get(presentation_id) is not None
