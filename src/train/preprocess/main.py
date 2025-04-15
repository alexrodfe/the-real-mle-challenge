import asyncio
from pathlib import Path
import numpy as np
import pandas as pd
from pandas import DataFrame

from kaisdk.sdk.kai_sdk import KaiSDK
from kaisdk.runner.runner import Runner
from google.protobuf.any_pb2 import Any
from google.protobuf.struct_pb2 import Value

async def initializer(sdk: KaiSDK):
    sdk.logger.info("Initializing preprocess..")


# Get number of bathrooms from `bathrooms_text`
def num_bathroom_from_text(text):
    try:
        if isinstance(text, str):
            bath_num = text.split(" ")[0]
            return float(bath_num)
        else:
            return np.NaN
    except ValueError:
        return np.NaN

def preprocess_amenities_column(df: DataFrame) -> DataFrame:
    df['TV'] = df['amenities'].str.contains('TV')
    df['TV'] = df['TV'].astype(int)
    df['Internet'] = df['amenities'].str.contains('Internet')
    df['Internet'] = df['Internet'].astype(int)
    df['Air_conditioning'] = df['amenities'].str.contains('Air conditioning')
    df['Air_conditioning'] = df['Air_conditioning'].astype(int)
    df['Kitchen'] = df['amenities'].str.contains('Kitchen')
    df['Kitchen'] = df['Kitchen'].astype(int)
    df['Heating'] = df['amenities'].str.contains('Heating')
    df['Heating'] = df['Heating'].astype(int)
    df['Wifi'] = df['amenities'].str.contains('Wifi')
    df['Wifi'] = df['Wifi'].astype(int)
    df['Elevator'] = df['amenities'].str.contains('Elevator')
    df['Elevator'] = df['Elevator'].astype(int)
    df['Breakfast'] = df['amenities'].str.contains('Breakfast')
    df['Breakfast'] = df['Breakfast'].astype(int)

    df.drop('amenities', axis=1, inplace=True)
    
    return df

async def handler(sdk: KaiSDK, message: Any):
    sdk.logger.info(f"Received message example: {message}")
    response = Value()

    # Load raw data
    FILEPATH_RAW_DATA = Path.cwd() / "data" / "listings.csv"
    df_raw = pd.read_csv(FILEPATH_RAW_DATA)

    df_raw.drop(columns=['bathrooms'], inplace=True)
    df_raw['bathrooms'] = df_raw['bathrooms_text'].apply(num_bathroom_from_text)
    
    # For an initial model, we are only going to use a small subset of the columns.
    COLUMNS = ['id', 'neighbourhood_group_cleansed', 'property_type', 'room_type', 'latitude', 'longitude', 'accommodates', 'bathrooms', 'bedrooms', 'beds','amenities', 'price']

    df = df_raw[COLUMNS].copy()
    df.rename(columns={'neighbourhood_group_cleansed': 'neighbourhood'}, inplace=True)

    # Remove rows with missing values
    df.dropna(inplace=True, axis=0)

    # Convert price string to numeric
    df['price'] = df['price'].str.extract(r"(\d+).")
    df['price'] = df['price'].astype(int)
    # Remove rows with price < 10
    df = df[df['price'] >= 10]

    # Create a categorical price column corresponding to Low ($0-$90), Mid ($90-$180), High ($180-$400) and Luxury ($400+) properties
    df['category'] = pd.cut(df['price'], bins=[10, 90, 180, 400, np.inf], labels=[0, 1, 2, 3])

    # extract amenities
    df = preprocess_amenities_column(df)

    FILEPATH_PREPROCESSED_DATA = Path.cwd() / "data" / "preprocessed_listings.csv"
    df.to_csv(FILEPATH_PREPROCESSED_DATA)

    await sdk.messaging.send_output(response=response)



async def finalizer(sdk: KaiSDK):
    sdk.logger.info("Finalizing example..")


async def init():
    runner = await Runner().initialize()
    await (
        runner.task_runner()
        .with_initializer(initializer)
        .with_handler(handler)
        .with_finalizer(finalizer)
        .run()
    )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(init())
    loop.run_forever()
    loop.close()
