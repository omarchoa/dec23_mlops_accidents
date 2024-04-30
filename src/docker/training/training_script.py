# imports
import datetime
import json
import random
import string
import time

import joblib
import numpy as np
import pandas as pd
from sklearn import ensemble

from config import paths

# load data
X_train = pd.read_csv(paths.X_TRAIN)
X_test = pd.read_csv(paths.X_TEST)
y_train = pd.read_csv(paths.Y_TRAIN)
y_test = pd.read_csv(paths.Y_TEST)
y_train = np.ravel(y_train)
y_test = np.ravel(y_test)

# rename column "int" to "inter" to avoid conflicts with reserved keyword
X_train.rename(columns={"int": "inter"}, inplace=True)
X_test.rename(columns={"int": "inter"}, inplace=True)

# define model
model = ensemble.RandomForestClassifier(n_jobs=-1)

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
print("Modèle entraîné et sauvegardé.")
