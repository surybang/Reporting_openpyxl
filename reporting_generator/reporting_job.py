from loguru import logger
import pandas as pd

from dal import S3Storage
from reporting_generator.insert_data import write_data_to_excel
from reporting_generator.fill_indicators import fill_indicators


class ReportingJob:
    def __init__(self, config):
        self.config = config
        self.storage = S3Storage(bucket=config.get("s3", "bucket"))
        self.paths = config.get("paths")

    def run(self):
        try:
            self.download_files()
            df = self.load_data()
            self.insert_data(df)
            self.fill_indicators()
            self.upload_report()
        except Exception as e:
            logger.exception(f"Erreur inattendue dans le job complet : {e}")

    def download_files(self):
        self.storage.download_file(
            self.paths["remote"]["data"], self.paths["local"]["data"]
        )
        logger.success("Fichier de données téléchargé")

        self.storage.download_file(
            self.paths["remote"]["template"], self.paths["local"]["template"]
        )
        logger.success("Template téléchargé")

    def load_data(self):
        try:
            df = pd.read_parquet(self.paths["local"]["data"])
            logger.success("Fichier de données chargé avec succès")
            return df
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données : {e}")
            raise

    def insert_data(self, df):
        try:
            write_data_to_excel(self.paths["local"]["template"], df=df)
            logger.success("Données insérées dans le fichier Excel")
        except Exception as e:
            logger.error(f"Erreur lors de l'insertion : {e}")
            raise

    def fill_indicators(self):
        try:
            fill_indicators(self.paths["local"]["template"])
            logger.success("Indicateurs remplis")
        except Exception as e:
            logger.error(f"Erreur lors du remplissage : {e}")
            raise

    def upload_report(self):
        try:
            self.storage.upload_file(
                self.paths["local"]["template"], self.paths["remote"]["reporting"]
            )
            logger.success("Fichier final uploadé")
        except Exception as e:
            logger.error(f"Erreur upload : {e}")
            raise
