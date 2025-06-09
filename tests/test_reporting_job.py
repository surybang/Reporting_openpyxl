from unittest.mock import MagicMock, patch

import pytest

from reporting_generator import ReportingJob


@pytest.fixture
def mock_config():
    return {
        "s3": {"bucket": "my-bucket"},
        "paths": {
            "remote": {
                "data": "remote/data.parquet",
                "template": "remote/template.xlsx",
                "reporting": "remote/reporting.xlsx",
            },
            "local": {"data": "local/data.parquet", "template": "local/template.xlsx"},
        },
    }


@patch("reporting_generator.reporting_job.S3Storage")
@patch("reporting_generator.reporting_job.pd.read_parquet")
@patch("reporting_generator.reporting_job.write_data_to_excel")
@patch("reporting_generator.reporting_job.fill_indicators")
def test_reporting_job_run(
    mock_fill_indicators,
    mock_write_data_to_excel,
    mock_read_parquet,
    mock_s3storage,
    mock_config,
):
    # Simuler les retours
    mock_df = MagicMock(name="Mocked DataFrame")
    mock_read_parquet.return_value = mock_df
    mock_storage_instance = mock_s3storage.return_value

    # Instancier le job
    job = ReportingJob(config=mock_config)

    # Lancer le job
    job.run()

    # Vérifier les appels attendus
    mock_storage_instance.download_file.assert_any_call(
        "remote/data.parquet", "local/data.parquet"
    )
    mock_storage_instance.download_file.assert_any_call(
        "remote/template.xlsx", "local/template.xlsx"
    )
    mock_read_parquet.assert_called_once_with("local/data.parquet")
    mock_write_data_to_excel.assert_called_once_with("local/template.xlsx", df=mock_df)
    mock_fill_indicators.assert_called_once_with("local/template.xlsx")
    mock_storage_instance.upload_file.assert_called_once_with(
        "local/template.xlsx", "remote/reporting.xlsx"
    )
