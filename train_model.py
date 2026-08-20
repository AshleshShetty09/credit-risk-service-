import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report

cols = ["checking_status","duration","credit_history","purpose","credit_amount",
        "savings_status","employment","installment_rate","personal_status_sex",
        "other_parties","residence_since","property_magnitude","age",
        "other_payment_plans","housing","existing_credits","job",
        "num_dependents","own_telephone","foreign_worker","target"]

df = pd.read_csv("data/german_credit.csv", names=cols)
df["target"] = (df["target"] == 2).astype(int)  # 1 = bad credit risk, 0 = good

X = df.drop(columns=["target"])
y = df["target"]

categorical = X.select_dtypes(include="object").columns.tolist()
numeric = X.select_dtypes(include="number").columns.tolist()

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ("num", "passthrough", numeric),
])

model = Pipeline([
    ("preprocess", preprocessor),
    ("clf", RandomForestClassifier(n_estimators=200, random_state=42)),
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
model.fit(X_train, y_train)

preds = model.predict_proba(X_test)[:, 1]
print("Test ROC-AUC:", roc_auc_score(y_test, preds))
print(classification_report(y_test, model.predict(X_test)))

joblib.dump(model, "model_artifacts/credit_model.joblib")
X_train.to_csv("model_artifacts/reference_data.csv", index=False)  # needed later for drift report
print("Saved model + reference data.")