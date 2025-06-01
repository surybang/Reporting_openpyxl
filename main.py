import sys
import os

from loguru import logger
import pandas as pd

from DAL import S3Storage
from reporting_generator import fill_indicators, write_data_to_excel

# Configuration du logger
logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
)


def main():
    bucket = "fabienhos"
    data_remote_path = "/Tuto_reporting/data.parquet"
    reporting_remote_path = "/Tuto_reporting/reporting.xlsx"
    file_remote_path = "/Tuto_reporting/fichier_a_remplir.xlsx"
    data_local_path = "data/data.parquet"
    reporting_local_path = "example/fichier_a_remplir.xlsx"

    os.makedirs("example", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    logger.info("Initialisation du client S3Storage")
    storage = S3Storage(bucket=bucket)

    logger.info(
        f"Téléchargement du fichier {data_remote_path} depuis le bucket {bucket}"
    )
    try:
        storage.download_file(data_remote_path, data_local_path)
        logger.success(f"Fichier téléchargé avec succès : {data_local_path}")
    except RuntimeError as e:
        logger.error(f"Erreur lors du téléchargement : {e}")

    logger.info(f"Création du DataFrame à partir du fichier {data_local_path}")
    try:
        df = pd.read_parquet(data_local_path)
        logger.success(f"DataFrame généré avec succès : {df.columns.tolist()}")
    except FileNotFoundError as e:
        logger.error(f"Erreur lors de la création du DataFrame: {e}")

    try:
        storage.download_file(file_remote_path, reporting_local_path)
        logger.success(f"Template téléchargé avec succès : {file_remote_path}")
    except RuntimeError as e:
        logger.error(f"Erreur lors du téléchargement : {e}")
    try:
        write_data_to_excel(reporting_local_path, df=df)
        logger.success("Les données ont été insérées avec succès")
    except Exception as e:
        logger.error(f"Erreur innatendue : {e}")

    try:
        fill_indicators(reporting_local_path)
        logger.success("Les indicateurs ont été remplis avec succès")
    except Exception as e:
        logger.error(f"Erreur innatendue: {e}")

    try:
        storage.upload_file(reporting_local_path, reporting_remote_path)
        logger.success(
            f"Le fichier {reporting_local_path} a été uploadé vers {reporting_remote_path}"
        )
    except Exception as e:
        logger.error(f"Erreur innatendue: {e}")


if __name__ == "__main__":
    main()
