import joblib
import pandas as pd
import sys
import json
from config import paths
import time
import datetime
import random
import string
import os


# Load your saved model
model = joblib.load(paths.MODEL_TRAINED)


def predict_model(features):
    input_df = pd.DataFrame([features])
    ## print(input_df)
    pred_time_start = time.time()
    prediction = model.predict(input_df)
    pred_time_end = time.time()
    return prediction, input_df, pred_time_start, pred_time_end


def get_feature_values_manually(feature_names):
    features = {}
    for feature_name in feature_names:
        feature_value = float(input(f"Enter value for {feature_name}: "))
        features[feature_name] = feature_value
    return features


if __name__ == "__main__":
    if len(sys.argv) == 2:
        json_file = sys.argv[1]
        with open(json_file, "r") as file:
            features = json.load(file)
    else:
        X_train = pd.read_csv(paths.X_TRAIN)
        feature_names = X_train.columns.tolist()
        features = get_feature_values_manually(feature_names)

    result, input_df, pred_time_start, pred_time_end = predict_model(features)

    # prepare log data for export
    log_dict = {
        "request_id": "".join(random.choices(string.digits, k=16)),
        "time_stamp": str(datetime.datetime.now()),
        ## "user_name": user,
        "response_status_code": 200,
        "input_features": input_df.to_dict(orient="records")[0],
        "output_prediction": int(result[0]),
        "verified_prediction": None,
        "prediction_time": pred_time_end - pred_time_start,
    }
    log_json = json.dumps(obj=log_dict)

    # export log data to log file
    if os.environ.get("ENDPOINT") == "/predict_from_test":
        log_path = paths.LOGS_PREDS_TEST
    elif os.environ.get("ENDPOINT") == "/predict_from_call":
        log_path = paths.LOGS_PREDS_UNLABELED
    with open(log_path, "a") as file:
        file.write(log_json + "\n")

    result_dict = {"prediction": log_dict["output_prediction"]}
    print(result_dict)
