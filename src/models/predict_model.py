import joblib
import pandas as pd
import sys
import json
from config import paths


# Load your saved model
loaded_model = joblib.load(paths.MODEL_TRAINED)


def predict_model(features):
    input_df = pd.DataFrame([features])
    # print(input_df)
    prediction = loaded_model.predict(input_df)
    return prediction


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

    result = predict_model(features)
    result_dict = {"prediction": result[0]}
    print(result_dict)
