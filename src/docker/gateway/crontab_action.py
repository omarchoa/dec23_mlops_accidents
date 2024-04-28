import datetime
import os
import requests

threshold = 0.75
now = str(datetime.datetime.now())
f1_score_file = "/logs/f1-score.csv"

if not os.path.exists(f1_score_file):
    comment = 'file "f1-score.csv" not existing'
else:
    try:
        with open(f1_score_file, "r") as f1_file:
            for line in f1_file:
                pass
        latest_score = float(line.split(";")[-1].strip())
        if latest_score >= threshold:
            comment = f"latest_score ({latest_score}) >= threshold ({threshold}): nothing to do"
        else:
            comment = f"latest_score ({latest_score}) < threshold ({threshold}): model shall be retrained !"
    except:
        comment = "latest f1-score can't be extracted from f1-score.csv"

end = str(datetime.datetime.now())
with open("/logs/crontab.csv", "a") as log_file:
    log_file.write(f"{now};{end};{comment}\n")
