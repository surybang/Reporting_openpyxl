import sys

from loguru import logger

from config import config
from reporting_generator import ReportingJob


# Configuration du logger
logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
)

if __name__ == "__main__":
    job = ReportingJob(config)
    job.run()
