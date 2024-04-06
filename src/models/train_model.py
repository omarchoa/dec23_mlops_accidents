import pandas as pd
from sklearn import ensemble
import joblib
import numpy as np
from config import paths


print(joblib.__version__)

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
rf_classifier.fit(X_train, y_train)

# --Save the trained model to a file
joblib.dump(rf_classifier, paths.MODEL_TRAINED)
print("Model trained and saved successfully.")
