"""Configuração central da Fase 4 (Credit Scoring).

Caminhos e definição de colunas usados pelo baseline (Etapa 1) e pela
simulação/detecção de drift (Etapa 2).
"""

from __future__ import annotations

from pathlib import Path

# --- Caminhos ---------------------------------------------------------------
DATA_DIR = Path("data")
RAW_CSV = DATA_DIR / "raw" / "german_credit_with_risk.csv"
REFERENCE_CSV = DATA_DIR / "reference" / "reference.csv"
PRODUCTION_RAW_CSV = DATA_DIR / "production" / "production_raw.csv"  # split, antes do drift
PRODUCTION_CSV = DATA_DIR / "production" / "production.csv"          # com drift injetado

MODELS_DIR = Path("models")
MODEL_PATH = MODELS_DIR / "credit_baseline.joblib"
MODEL_METRICS_PATH = MODELS_DIR / "credit_baseline_metrics.json"

REPORTS_DIR = Path("reports")
DRIFT_HTML = REPORTS_DIR / "drift_report.html"
DRIFT_STATS_CSV = REPORTS_DIR / "drift_stats.csv"
DRIFT_SUMMARY_MD = REPORTS_DIR / "drift_summary.md"

# --- Colunas ----------------------------------------------------------------
NUMERIC_FEATURES = ["Age", "Credit amount", "Duration"]
CATEGORICAL_FEATURES = [
    "Sex",
    "Job",
    "Housing",
    "Saving accounts",
    "Checking account",
    "Purpose",
]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

TARGET = "Risk"                 # 'good' / 'bad'
POSITIVE_LABEL = "bad"          # classe de interesse (risco de inadimplência)
PREDICTION_LABEL = "prediction"     # rótulo previsto (good/bad)
PREDICTION_PROBA = "prediction_proba"  # probabilidade da classe 'bad'

# NaN em Saving/Checking account = "sem conta" (categoria legítima), não ausência.
NO_ACCOUNT_FILL = "no_account"

RANDOM_STATE = 42
