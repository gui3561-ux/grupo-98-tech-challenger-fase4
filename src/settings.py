from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TICKER = "PETR4.SA"
START_DATE = "2018-01-01"
WINDOW_SIZE = 60
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
HORIZON = "D+1"

MODELS_DIR = ROOT / "models"
DATA_DIR = ROOT / "data"
RAW_CACHE = DATA_DIR / "raw.parquet"
MODEL_FILENAME = "lstm_petr4.keras"
SCALER_FILENAME = "scaler.pkl"
METRICS_FILENAME = "metrics.json"
