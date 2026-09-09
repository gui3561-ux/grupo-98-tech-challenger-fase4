from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.settings import TRAIN_RATIO, VAL_RATIO


def clean_series(frame: pd.DataFrame) -> pd.DataFrame:
    """Remove fechamentos inválidos e ordena por data crescente."""
    cleaned = frame.copy()
    cleaned["close"] = pd.to_numeric(cleaned["close"], errors="coerce")
    cleaned = cleaned.dropna(subset=["close"])
    cleaned = cleaned[np.isfinite(cleaned["close"])]
    return cleaned.sort_values("date").reset_index(drop=True)


def chronological_split(
    frame: pd.DataFrame,
    train_ratio: float = TRAIN_RATIO,
    val_ratio: float = VAL_RATIO,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Separa treino/validação/teste por ordem temporal, sem embaralhar."""
    n = len(frame)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))
    train = frame.iloc[:train_end].copy()
    validation = frame.iloc[train_end:val_end].copy()
    test = frame.iloc[val_end:].copy()
    return train, validation, test


def fit_scaler(train: pd.DataFrame) -> MinMaxScaler:
    scaler = MinMaxScaler()
    scaler.fit(train[["close"]].to_numpy())
    return scaler


def transform_close(frame: pd.DataFrame, scaler: MinMaxScaler) -> pd.DataFrame:
    out = frame.copy()
    out["close_scaled"] = scaler.transform(frame[["close"]].to_numpy()).ravel()
    return out
