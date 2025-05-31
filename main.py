import sys
import os

from loguru import logger

from DAL import S3Storage

# Configuration du logger
logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}"
    )


def main():
    # Paramètres
    bucket = "fabienhos"
    endpoint_url = os.getenv("$AWS_S3_ENDPOINT")
    remote_path = "/Tuto_reporting/data.parquet"
    local_path = "data/data.parquet"

    logger.info("Initialisation du client S3Storage")
    storage = S3Storage(bucket=bucket, endpoint_url=endpoint_url)

    logger.info(f"Téléchargement du fichier {remote_path} depuis le bucket {bucket}")
    try:
        storage.download_file(remote_path, local_path)
        logger.success(f"Fichier téléchargé avec succès : {local_path}")
    except RuntimeError as e:
        logger.error(f"Erreur lors du téléchargement : {e}")


if __name__ == "__main__":
    main()
