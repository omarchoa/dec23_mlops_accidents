# imports
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


# load model
model = joblib.load(paths.MODEL_TRAINED)


# define prediction function
def predict(features):
    input_df = pd.DataFrame([features])
    pred_time_start = time.time()
    prediction = model.predict(input_df)
    pred_time_end = time.time()
    return prediction, input_df, pred_time_start, pred_time_end


# define manual feature input function
def get_feature_values_manually(feature_names):
    features = {}
    for feature_name in feature_names:
        feature_value = float(input(f"Enter value for {feature_name}: "))
        features[feature_name] = feature_value
    return features


# main function
if __name__ == "__main__":
    # if input file is provided, read features from file
    if len(sys.argv) == 2:
        json_file = sys.argv[1]
        with open(json_file, "r") as file:
            features = json.load(file)
    # else, read features via manual input
    else:
        X_train = pd.read_csv(paths.X_TRAIN)
        feature_names = X_train.columns.tolist()
        features = get_feature_values_manually(feature_names)

    # perform prediction and save outputs
    result, input_df, pred_time_start, pred_time_end = predict(features)

    # get incident priority level
    priority = result[0]

    # prepare log data for export
    log_dict = {
        "request_id": "".join(random.choices(string.digits, k=16)),
        "time_stamp": str(datetime.datetime.now()),
        ## "user_name": user,
        "response_status_code": 200,
        "input_features": input_df.to_dict(orient="records")[0],
        "output_prediction": int(priority),
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

    # define response
    if priority == 1:
        response = "Incident priority level: high."
    else:
        response = "Incident priority level: low."

    # print response
    print(response)