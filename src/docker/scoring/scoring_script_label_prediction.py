# imports
import json
import sys

from config import paths

# load prediction label from input file
input = sys.argv[1]
with open(input, "r") as file:
    pred_label = json.load(file)

# load unlabeled predictions from logs
with open(paths.LOGS_PREDS_UNLABELED, "r") as file:
    preds_unlabeled = [json.loads(line) for line in file]

# label corresponding prediction
record_exists = "no"
record_to_update = {}
for record in preds_unlabeled:
    ## pull up record corresponding to input request_id
    if int(record["request_id"]) == pred_label["request_id"]:
        record_exists = "yes"
        record_to_update = record

        ## update verified_prediction field with input y_true
        record_to_update["verified_prediction"] = pred_label["y_true"]

        ## save updated record to labeled prediction logs
        record_updated_json = json.dumps(obj=record_to_update)
        with open(paths.LOGS_PREDS_LABELED, "a") as file:
            file.write(record_updated_json + "\n")

# print response
if record_exists == "yes":
    print("Prédiction mise à jour. Merci pour votre retour.")
else:
    print("Prédiction non trouvée. Veuillez fournir une référence valable.")
