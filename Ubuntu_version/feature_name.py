# save as check_features.py, then: python check_features.py
import joblib, json
scaler = joblib.load("./scaler_pipeline.joblib")     # your file
# Try to read feature names from the pipeline; fall back to your own list if needed
names = getattr(scaler, "feature_names_in_", None)
if names is None:
    # If your scaler is inside a Pipeline, expose your list here instead:
    # names = [...]
    raise SystemExit("Put your ordered 77 feature names list here and re-run.")
print("Feature count:", len(names))
open("expected_features.json","w").write(json.dumps(list(names), indent=2))
print("Wrote expected_features.json")

