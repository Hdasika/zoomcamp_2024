from mage_ai.settings.repo import get_repo_path
from azure.storage.blob import BlobServiceClient
from pandas import DataFrame
from os import path
from io import BytesIO
import yaml
import pyarrow as pa
import pyarrow.parquet as pq


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_azure_blob_storage(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Azure Blob Storage.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading
    """

    with open(path.join(get_repo_path(), 'io_config.yaml'), 'r') as file:
        data = yaml.safe_load(file)

    connection_string = data['dev']['AZURE_BLOB_CONNECTION_STRING']

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    for date_value in list(df['lpep_pickup_date'].unique()):
        parquet_file = BytesIO()
        df_filter = df[df['lpep_pickup_date'] == date_value]
        df_filter.to_parquet(parquet_file, engine='pyarrow')
        parquet_file.seek(0)
        partition_path = f"/green_taxi/lpep_pickup_date={date_value}"
        blob_client = blob_service_client.get_blob_client('synapse', partition_path + "/data.parquet")
        blob_client.upload_blob(data=parquet_file, overwrite=True)