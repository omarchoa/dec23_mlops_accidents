from pathlib import Path
import os


# root path
if os.environ.get("CONTAINERIZED") == "yes":
    ROOT = "."
else:
    ROOT = [
        p for p in Path(__file__).parents if p.parts[-1] == "dec23_mlops_accidents"
    ][0]

# data paths
DATA_PREPROCESSED = Path(ROOT, "data", "preprocessed")
X_TRAIN = Path(DATA_PREPROCESSED, "X_train.csv")
X_TEST = Path(DATA_PREPROCESSED, "X_test.csv")
Y_TRAIN = Path(DATA_PREPROCESSED, "y_train.csv")
Y_TEST = Path(DATA_PREPROCESSED, "y_test.csv")

# log paths
LOGS = Path(ROOT, "logs")
PREDS_UNLABELED = Path(LOGS, "preds_call.jsonl")
PREDS_LABELED = Path(LOGS, "preds_labeled.jsonl")

# model paths
MODEL_SAVES = Path(ROOT, "models")
MODEL_TRAINED = Path(MODEL_SAVES, "trained_model.joblib")
MODEL_TRAINED_NEW = Path(MODEL_SAVES, "new_trained_model.joblib")

# other paths
USERS = Path(ROOT, "src", "features", "api", "users_db_bis.json")
