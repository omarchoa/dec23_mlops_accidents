import pandas as pd
from sklearn import ensemble
import joblib
import numpy as np
from config import paths
import time
import datetime
import random
import string
import json


# print(joblib.__version__)

X_train = pd.read_csv(paths.X_TRAIN)
X_test = pd.read_csv(paths.X_TEST)
y_train = pd.read_csv(paths.Y_TRAIN)
y_test = pd.read_csv(paths.Y_TEST)
y_train = np.ravel(y_train)
y_test = np.ravel(y_test)

X_train.rename(columns={"int": "inter"}, inplace=True)
X_test.rename(columns={"int": "inter"}, inplace=True)

rf_classifier = ensemble.RandomForestClassifier(n_jobs=-1)

# --Train the model
train_time_start = time.time()
rf_classifier.fit(X_train, y_train)
train_time_end = time.time()

# prepare log data for export
log_dict = {
    "request_id": "".join(random.choices(string.digits, k=16)),
    "time_stamp": str(datetime.datetime.now()),
    ## "user_name": user,
    "response_status_code": 200,
    "estimator_type": str(type(rf_classifier)),
    "estimator_parameters": rf_classifier.get_params(),
    "feature_importances": dict(
        zip(X_train.columns.to_list(), list(rf_classifier.feature_importances_))
    ),
    "train_time": train_time_end - train_time_start,
}
log_json = json.dumps(obj=log_dict)

# export log data to log file
with open(paths.LOGS_TRAIN, "a") as file:
    file.write(log_json + "\n")

# --Save the trained model to a file
joblib.dump(rf_classifier, paths.MODEL_TRAINED)
print("Model trained and saved successfully.")
