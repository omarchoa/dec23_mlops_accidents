# imports
import datetime
import json
import os
import random
import string
import time

import joblib
import numpy as np
import pandas as pd

from config import paths

# load model
model = joblib.load(
    paths.MODEL_TRAINED
)  ## paths.MODEL_TRAINED = "/home/shield/models/trained_model.joblib"

# # add time stamp to current model's file name
# time_stamp_string = datetime.datetime.now().strftime(
#     "%Y%m%d_%H%M%S"
# )  ## "YYYYMMDD_HHMMSS"
# model_file_name_current = paths.MODEL_TRAINED.stem  ## "trained_model"
# model_file_name_time_stamped = (
#     model_file_name_current + "_" + time_stamp_string
# )  ## "trained_model_YYYYMMDD_HHMMSS"
# model_path_time_stamped = paths.MODEL_TRAINED.with_stem(
#     model_file_name_time_stamped
# )  ## "/home/shield/models/trained_model_YYYYMMDD_HHMMSS.joblib"
# joblib.dump(model, model_path_time_stamped)

# load training data from data files
X_train_old = pd.read_csv(paths.X_TRAIN)
y_train_old = pd.read_csv(paths.Y_TRAIN)

# rename column "int" to "inter" to avoid conflicts with reserved keyword
X_train_old.rename(columns={"int": "inter"}, inplace=True)

# flatten y_train_old
y_train_old = np.ravel(y_train_old)

# if labeled predictions are available
if os.path.exists(paths.LOGS_PREDS_LABELED):

    # load labeled predictions from logs
    with open(paths.LOGS_PREDS_LABELED, "r") as file:
        preds_labeled = [json.loads(line) for line in file]

    X_train_new = pd.DataFrame()
    y_train_new = pd.Series()
    # convert labeled predictions to training data format
    for record in preds_labeled:
        ## append input features to X_train_new
        X_record = record["input_features"]
        X_record = {key: [value] for key, value in X_record.items()}
        X_record = pd.DataFrame(X_record)
        X_train_new = pd.concat([X_train_new, X_record])

        ## append verified prediction to y_train_new
        y_record = record["verified_prediction"]
        y_record = pd.Series(y_record)
        if (
            y_train_new.empty is True
        ):  ### to avoid "FutureWarning: The behavior of array concatenation with empty entries is deprecated."
            y_train_new = y_record
        else:
            y_train_new = pd.concat([y_train_new, y_record])
    y_train_old = pd.Series(y_train_old, name="grav")
    y_train_new = pd.Series(y_train_new, name="grav")

    # rename column "int" to "inter" to avoid conflicts with reserved keyword
    X_train_new.rename(columns={"int": "inter"}, inplace=True)

    # append labeled predictions to training data
    X_train_combined = pd.concat([X_train_old, X_train_new]).reset_index(drop=True)
    y_train_combined = pd.concat([y_train_old, y_train_new]).reset_index(drop=True)

    # define X_train and y_train
    X_train = X_train_combined
    y_train = y_train_combined

else:

    # define X_train and y_train
    X_train = X_train_old
    y_train = y_train_old

# train model
train_time_start = time.time()
model.fit(X_train, y_train)
train_time_end = time.time()

# prepare log data for export
log_dict = {
    "request_id": "".join(random.choices(string.digits, k=16)),
    "time_stamp": str(datetime.datetime.now()),
    ## "user_name": user,
    "response_status_code": 200,
    "estimator_type": str(type(model)),
    "estimator_parameters": model.get_params(),
    "feature_importances": dict(
        zip(X_train.columns.to_list(), list(model.feature_importances_))
    ),
    "train_time": train_time_end - train_time_start,
}
log_json = json.dumps(obj=log_dict)

# export log data to log file
with open(paths.LOGS_TRAIN, "a") as file:
    file.write(log_json + "\n")

# save model
joblib.dump(model, paths.MODEL_TRAINED)
print("Modèle ré-entraîné et re-sauvegardé.")
