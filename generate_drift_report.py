import pandas as pd
import joblib
from evidently import Report
from evidently.presets import DataDriftPreset

reference = pd.read_csv("model_artifacts/reference_data.csv")

# simulate "production" data with a slight shift, since we don't have real live traffic yet
current = reference.sample(n=200, random_state=1).copy()
current["credit_amount"] = (current["credit_amount"] * 1.15).astype(int)  # simulate drift
current["age"] = current["age"] + 5

report = Report([DataDriftPreset()])
result = report.run(reference_data=reference, current_data=current)
result.save_html("drift_report.html")
print("Saved drift_report.html")