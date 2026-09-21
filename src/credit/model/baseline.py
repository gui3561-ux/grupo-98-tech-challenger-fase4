"""Modelo baseline de risco de crédito (mínimo da Etapa 1).

Pipeline sklearn (OneHotEncoder nas categóricas + XGBoost) treinado no dataset
de Referência. Persiste o modelo e as métricas de classificação. Usado pela
Etapa 2 para gerar predições e evidenciar Concept Drift.
"""

from __future__ import annotations

import json

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier

from src.credit import config as C


def _to_binary(y: pd.Series) -> pd.Series:
    """good -> 0, bad -> 1 (bad = classe positiva / risco de inadimplência)."""
    return (y == C.POSITIVE_LABEL).astype(int)


def build_pipeline() -> Pipeline:
    pre = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                C.CATEGORICAL_FEATURES,
            ),
            ("num", "passthrough", C.NUMERIC_FEATURES),
        ]
    )
    clf = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=C.RANDOM_STATE,
    )
    return Pipeline([("pre", pre), ("clf", clf)])


def train_baseline() -> dict:
    """Treina no dataset de Referência, avalia em holdout e persiste modelo+métricas."""
    if not C.REFERENCE_CSV.exists():
        raise FileNotFoundError(
            f"{C.REFERENCE_CSV} não encontrado. Rode: python -m src.credit.data.preprocess"
        )
    ref = pd.read_csv(C.REFERENCE_CSV)
    X, y = ref[C.FEATURES], _to_binary(ref[C.TARGET])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=C.RANDOM_STATE, stratify=y
    )

    pipe = build_pipeline()
    pipe.fit(X_train, y_train)

    proba = pipe.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)
    metrics = {
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "roc_auc": round(float(roc_auc_score(y_test, proba)), 4),
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "f1_bad": round(float(f1_score(y_test, pred)), 4),
        "positive_label": C.POSITIVE_LABEL,
        "report": classification_report(
            y_test, pred, target_names=["good", "bad"], output_dict=True
        ),
    }

    # Reajusta no dataset de Referência inteiro para produção.
    pipe.fit(X, y)

    C.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, C.MODEL_PATH)
    C.MODEL_METRICS_PATH.write_text(json.dumps(metrics, indent=2, ensure_ascii=False))

    print(f"[baseline] Modelo salvo em {C.MODEL_PATH}")
    print(
        f"[baseline] holdout ROC-AUC={metrics['roc_auc']} "
        f"acc={metrics['accuracy']} f1(bad)={metrics['f1_bad']}"
    )
    return metrics


def load_model() -> Pipeline:
    if not C.MODEL_PATH.exists():
        raise FileNotFoundError(
            f"{C.MODEL_PATH} não encontrado. Rode: python -m src.credit.model.baseline"
        )
    return joblib.load(C.MODEL_PATH)


def predict_frame(pipe: Pipeline, df: pd.DataFrame) -> pd.DataFrame:
    """Anexa colunas de predição (rótulo good/bad e probabilidade de 'bad')."""
    proba = pipe.predict_proba(df[C.FEATURES])[:, 1]
    out = df.copy()
    out[C.PREDICTION_PROBA] = proba
    out[C.PREDICTION_LABEL] = pd.Series(proba >= 0.5, index=df.index).map(
        {True: "bad", False: "good"}
    )
    return out


if __name__ == "__main__":
    train_baseline()
