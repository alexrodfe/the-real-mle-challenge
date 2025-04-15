import asyncio
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

from kaisdk.sdk.kai_sdk import KaiSDK
from kaisdk.runner.runner import Runner
from google.protobuf.any_pb2 import Any
from google.protobuf.struct_pb2 import Value

async def initializer(sdk: KaiSDK):
    sdk.logger.info("Initializing inference trainer..")


async def handler(sdk: KaiSDK, message: Any):
    sdk.logger.info(f"Received message example: {message}")
    response = Value()

    # Load preprocessed data
    FILEPATH_PROCESSED = Path.cwd() / "data" / "preprocessed_listings.csv"
    df = pd.read_csv(FILEPATH_PROCESSED, index_col=0)
    df = df.dropna(axis=0)

    # Categorical variable mapping dictionaries
    MAP_ROOM_TYPE = {"Shared room": 1, "Private room": 2, "Entire home/apt": 3, "Hotel room": 4}
    MAP_NEIGHB = {"Bronx": 1, "Queens": 2, "Staten Island": 3, "Brooklyn": 4, "Manhattan": 5}

    # Map categorical features
    df["neighbourhood"] = df["neighbourhood"].map(MAP_NEIGHB)
    df["room_type"] = df["room_type"].map(MAP_ROOM_TYPE)

    # Split data for cross-validation
    FEATURE_NAMES = ["neighbourhood", "room_type", "accommodates", "bathrooms", "bedrooms"]

    X = df[FEATURE_NAMES]
    y = df["category"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=1)

    # Train the model
    clf = RandomForestClassifier(n_estimators=500, random_state=0, class_weight="balanced", n_jobs=4)
    clf.fit(X_train, y_train)

    # Save the model
    pickle.dump(clf, open(Path.cwd() / "simple_classifier.pkl", "wb"))

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
