from loguru import logger
from rich.logging import RichHandler


log_format = "{message}"
log_level = "DEBUG"

logger.configure(
    handlers=[{"sink": RichHandler(rich_tracebacks=True, markup=True), "format": log_format, "level": log_level}]
)
