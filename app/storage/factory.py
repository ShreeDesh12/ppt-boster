"""
Storage factory for creating storage instances
"""
import logging
from typing import Optional
from .base import BaseStorage
from .file_storage import FileStorage

logger = logging.getLogger(__name__)


class StorageFactory:
    """Factory class for creating storage instances"""

    # Registry of available storage backends
    _storage_backends = {
        'file_storage': FileStorage,
        # Future storage backends can be added here
        # 's3': S3Storage,
        # 'azure_blob': AzureBlobStorage,
        # 'gcs': GoogleCloudStorage,
    }

    # Default storage backend
    _default_backend = 'file_storage'

    @classmethod
    def create(cls, backend: Optional[str] = None, **kwargs) -> BaseStorage:
        """
        Create a storage instance

        Args:
            backend: Storage backend name (e.g., 'file_storage', 's3').
                    Defaults to 'file_storage'
            **kwargs: Additional arguments to pass to storage constructor

        Returns:
            Storage instance

        Raises:
            ValueError: If backend is not supported
        """
        backend = backend or cls._default_backend

        if backend not in cls._storage_backends:
            available = ', '.join(cls._storage_backends.keys())
            raise ValueError(
                f"Unsupported storage backend: '{backend}'. "
                f"Available backends: {available}"
            )

        storage_class = cls._storage_backends[backend]
        logger.info(f"Creating storage instance: {backend}")

        try:
            storage_instance = storage_class(**kwargs)
            logger.info(f"Successfully created {backend} storage instance")
            return storage_instance
        except Exception as e:
            logger.error(f"Error creating storage instance: {str(e)}", exc_info=True)
            raise

    @classmethod
    def register_backend(cls, name: str, storage_class: type):
        """
        Register a new storage backend

        Args:
            name: Name of the storage backend
            storage_class: Storage class that extends BaseStorage

        Raises:
            TypeError: If storage_class doesn't extend BaseStorage
        """
        if not issubclass(storage_class, BaseStorage):
            raise TypeError(
                f"Storage class must extend BaseStorage. "
                f"Got: {storage_class.__name__}"
            )

        cls._storage_backends[name] = storage_class
        logger.info(f"Registered storage backend: {name}")

    @classmethod
    def get_available_backends(cls) -> list:
        """
        Get list of available storage backends

        Returns:
            List of backend names
        """
        return list(cls._storage_backends.keys())

    @classmethod
    def set_default_backend(cls, backend: str):
        """
        Set the default storage backend

        Args:
            backend: Name of the storage backend

        Raises:
            ValueError: If backend is not registered
        """
        if backend not in cls._storage_backends:
            available = ', '.join(cls._storage_backends.keys())
            raise ValueError(
                f"Cannot set default to unregistered backend: '{backend}'. "
                f"Available backends: {available}"
            )

        cls._default_backend = backend
        logger.info(f"Set default storage backend to: {backend}")
