import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from datetime import datetime
import json


METADATA_GLOBAL = {
    b"dataset_version": b"1.0.0",
    b"creation_date": datetime.utcnow().isoformat().encode("utf-8") + b"Z",
    b"owner": b"data_team",
    b"sensitivity_level": b"confidential",
    b"update_frequency": b"daily",
    b"description": b"Client risk assessment with historical scores",
}

schema = pa.schema([
    pa.field(
        "client_id", pa.int64(), nullable=False,
        metadata={
            b"description": b"Unique client identifier",
            b"pii": b"true",
            b"validation": b"positive_values_only"
        }),

    pa.field(
        "type_client", pa.string(), nullable=False,
        metadata={
            b"description": b"Client type (PP=Personne Physique, PM=Personne Morale)",
            b"domain_values": json.dumps(["PP", "PM"]).encode("utf-8"),
        }
    ),

    pa.field(
        "date_adhesion", pa.timestamp('ms'), nullable=False,
        metadata={
            b"description": b"Client registration timestamp",
            b"timezone": b"UTC",
            b"validation": b"date_range(1980-01-01, now)"
        }),

    pa.field(
        "score", pa.string(), nullable=True,
        metadata={
            b"description": b"Current risk score (V=Vert, O=Orange, R=Rouge), Z if new client",
            b"domain_values": json.dumps(["V", "O", "R", "Z"]).encode("utf-8"),
        }),

    pa.field(
        "score_prev", pa.string(), nullable=True,
        metadata={
            b"description": b"Previous risk score, Z if new client",
            b"domain_values": json.dumps(["O", "V", "R", "Z"]).encode("utf-8"),
        }),

    pa.field(
        "id_agent", pa.string(),
        metadata={
            b"description": b"Agent ID responsible for client",
            b"pii": b"false",
            b"reference_table": b"dim_agents"
        }),

    pa.field(
        "drc_complet", pa.bool_(), nullable=False,
        metadata={
            b"description": b"Documentation completeness flag",
            b"critical_alert": b"true"
        })
], metadata=METADATA_GLOBAL)


def validate_schema(df: pd.DataFrame, schema: pa.Schema):
    """Vérifie les violations de schéma"""
    errors = []

    null_counts = df.isnull().sum()
    for field in schema:
        if not field.nullable and null_counts[field.name] > 0:
            errors.append(f"VIOLATION: {field.name} has {null_counts[field.name]} nulls")

    domain_checks = {
        "type_client": set(df["type_client"].dropna().unique()) - {"PP", "PM"},
        "score": set(df["score"].dropna().unique()) - {"V", "O", "R", "Z"},
        "score_prev": set(df["score_prev"].dropna().unique()) - {"V", "O", "R", "Z"}
    }

    for col, violations in domain_checks.items():
        if violations:
            errors.append(f"DOMAIN VIOLATION: {col} contains invalid values {violations}")

    min_date = df["date_adhesion"].min()
    if pd.Timestamp(min_date) < pd.Timestamp("1980-01-01"):
        errors.append(f"DATE VIOLATION: date_adhesion has pre-1980 value ({min_date})")

    if errors:
        raise ValueError("\n".join(["CRITICAL SCHEMA ISSUES:"] + errors))


def prepare_data_for_parquet(df: pd.DataFrame) -> pa.Table:
    """Transforme le DataFrame Pandas en Table Arrow avec contrôles"""
    # Nettoyage
    df["date_adhesion"] = pd.to_datetime(df["date_adhesion"], errors="coerce")

    # Types explicites
    df["client_id"] = df["client_id"].astype("Int64")
    df["type_client"] = df["type_client"].astype(str)
    df["score"] = df["score"].astype(str)
    df["score_prev"] = df["score_prev"].astype(str)
    df["id_agent"] = df["id_agent"].astype(str)
    df["drc_complet"] = df["drc_complet"].astype(bool)
    
    # Validation
    validate_schema(df, schema)

    # Conversion Arrow
    table = pa.Table.from_pandas(df, schema=schema, preserve_index=False)

    return table


if __name__ == "__main__":
    from pathlib import Path

    path_data_csv = Path("create_data/csv/data.csv")
    path_data_pq = Path("create_data/pq/data.parquet")
    df = pd.read_csv(path_data_csv)
    table = prepare_data_for_parquet(df)

    pq.write_table(
        table,
        path_data_pq,
        compression='ZSTD',
        write_statistics=True,
        data_page_version='2.0',
        store_schema=True
    )
