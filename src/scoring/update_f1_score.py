# imports
import json

import joblib
import pandas as pd
from sklearn.metrics import f1_score

from config import paths


# load model
model = joblib.load(paths.MODEL_TRAINED)

# load test data from data files
X_test_old = pd.read_csv(paths.X_TEST)
y_test_old = pd.read_csv(paths.Y_TEST)

# load labeled predictions from logs
with open(paths.LOGS_PREDS_LABELED, "r") as file:
    preds_labeled = [json.loads(line) for line in file]

X_test_new = pd.DataFrame()
y_test_new = pd.Series()
# convert labeled predictions to test data format
for record in preds_labeled:
    ## append input features to X_test_new
    X_record = record["input_features"]
    X_record = {key: [value] for key, value in X_record.items()}
    X_record = pd.DataFrame(X_record)
    X_test_new = pd.concat([X_test_new, X_record])

    ## append verified prediction to y_test_new
    y_record = record["verified_prediction"]
    y_record = pd.Series(y_record)
    if (
        y_test_new.empty is True
    ):  ### to avoid "FutureWarning: The behavior of array concatenation with empty entries is deprecated."
        y_test_new = y_record
    else:
        y_test_new = pd.concat([y_test_new, y_record])
y_test_new = pd.Series(y_test_new, name="grav")

# rename column "int" to "inter" to avoid conflicts with reserved keyword
X_test_old.rename(columns={"int": "inter"}, inplace=True)
X_test_new.rename(columns={"int": "inter"}, inplace=True)

# append labeled predictions to test data
X_test_combined = pd.concat([X_test_old, X_test_new]).reset_index(drop=True)
y_test_combined = pd.concat([y_test_old, y_test_new]).reset_index(drop=True)

# define y values for f1 score computation
y_pred = model.predict(X_test_combined)
y_true = y_test_combined

# compute new f1 score macro average
f1_score_macro_average = f1_score(y_true=y_true, y_pred=y_pred, average="macro")

# prepare log data for export
log_dict = {
    "request_id": preds_labeled[-1]["request_id"],
    "f1_score_macro_average": f1_score_macro_average,
}
log_json = json.dumps(obj=log_dict)

# export log data to log file
with open(paths.LOGS_F1_SCORES, "a") as file:
    file.write(log_json + "\n")

# print response
print("F1 score successfully updated.")
