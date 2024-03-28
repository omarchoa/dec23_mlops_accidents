from pathlib import Path
import os


# bucket
BUCKET = "dec23-mlops-accidents"

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
MODEL_SAVES_LOCAL = Path(ROOT, "models")
MODEL_SAVES_CLOUD = "https://{bucket}.s3.eu-west-3.amazonaws.com/models".format(
    bucket=BUCKET
)
MODEL_TRAINED_LOCAL = Path(MODEL_SAVES_LOCAL, "trained_model.joblib")
MODEL_TRAINED_NEW_LOCAL = Path(MODEL_SAVES_LOCAL, "new_trained_model.joblib")
MODEL_TRAINED_CLOUD = Path("models", "trained_model.joblib")
MODEL_TRAINED_NEW_CLOUD = Path("models", "new_trained_model.joblib")

# other paths
USERS = Path(ROOT, "src", "features", "api", "users_db_bis.json")
