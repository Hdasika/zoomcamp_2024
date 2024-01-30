import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    data_df = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]

    # data_df = data_df.dropna(subset=['passenger_count', 'trip_distance'])
    
    data_df['lpep_pickup_date'] = pd.to_datetime(data_df['lpep_pickup_datetime'], unit='s').dt.date
    
    data = data_df.rename(columns={'VendorID': 'vendor_id','RatecodeID': 'ratecode_id',
        'PULocationID': 'pu_location_id', 'DOLocationID': 'do_location_id'})
    
    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['vendor_id'] is not None, 'vendor_id exists'
    assert ~(len(output[(output['passenger_count'] < 0)]) > 0), 'passenger_count is greater than Zero'
    assert ~(len(output[(output['trip_distance'] < 0)]) > 0), 'trip_distance is greater than Zero'