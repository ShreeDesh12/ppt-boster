"""
Logging configuration for the application
"""
import logging
import sys

def setup_logging():
    """Configure logging for the application"""
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Remove all existing handlers from root logger
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Create file handler
    file_handler = logging.FileHandler('app.log', mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Configure root logger
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Also configure app.main logger specifically
    app_logger = logging.getLogger("app.main")
    app_logger.setLevel(logging.DEBUG)
    app_logger.propagate = True

    # Also configure service loggers
    logging.getLogger("app.services.content_generator").setLevel(logging.DEBUG)
    logging.getLogger("app.services.presentation_generator").setLevel(logging.DEBUG)

    # Set logging levels for external libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)

    return root_logger
