import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
    taxi_dtypes = {
        'VendorID': pd.Int64Dtype(),
        'passenger_count': pd.Int64Dtype(),
        'trip_distance': float,
        'RatecodeID': pd.Int64Dtype(),
        'store_and_fw_flag': str,
        'PULocationID': pd.Int64Dtype(),
        'DOLocationID': pd.Int64Dtype(),
        'payment_type': pd.Int64Dtype(),
        'fare_amount': float,
        'extra': float,
        'mta_tax': float,
        'tip_amount': float,
        'tolls_amount':float,
        'improvement_surcharge': float,
        'total_amount': float,
        'congestion_surcharge': float
    }

    dataframes = []
    for month in range(10, 13):
        # Load the data for the current month into a DataFrame
        file_url = url + f'green/green_tripdata_2020-{month}.csv.gz'

        parse_dates = ['lpep_pickup_datetime','lpep_dropoff_datetime']

        df = pd.read_csv(file_url, compression='gzip',dtype=taxi_dtypes, parse_dates=parse_dates)

        # Append the DataFrame to the list
        dataframes.append(df)

    # Concatenate the DataFrames for the three months into a single DataFrame
    final_quarter_data = pd.concat(dataframes, ignore_index=True)
    
    return final_quarter_data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
