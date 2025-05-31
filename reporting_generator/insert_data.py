import pandas as pd


def write_data_to_excel(path_file: str, df: pd.DataFrame, sheet_name: str = 'DATA') -> None:
    """
    Écrit un DataFrame dans une feuille Excel (ajout au fichier existant).

    Args:
        path_file (str): Chemin du fichier Excel à modifier.
        df (pd.DataFrame): Données à écrire.
        sheet_name (str): Nom de la feuille à créer ou remplacer.
    """
    with pd.ExcelWriter(
        path_file,
        mode='a',
        engine='openpyxl',
        if_sheet_exists='replace'
    ) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
