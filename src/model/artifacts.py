from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras

from src.settings import MODEL_FILENAME, MODELS_DIR, SCALER_FILENAME, WINDOW_SIZE


def save_artifacts(
    model: keras.Model,
    scaler: MinMaxScaler,
    models_dir: Path | None = None,
) -> tuple[Path, Path]:
    directory = models_dir or MODELS_DIR
    directory.mkdir(parents=True, exist_ok=True)
    model_path = directory / MODEL_FILENAME
    scaler_path = directory / SCALER_FILENAME
    model.save(model_path)
    with scaler_path.open("wb") as handle:
        pickle.dump(scaler, handle)
    return model_path, scaler_path


def load_artifacts(models_dir: Path | None = None) -> tuple[keras.Model, MinMaxScaler]:
    directory = models_dir or MODELS_DIR
    model = keras.models.load_model(directory / MODEL_FILENAME)
    with (directory / SCALER_FILENAME).open("rb") as handle:
        scaler = pickle.load(handle)
    return model, scaler


def invert_scale(scaler: MinMaxScaler, values: np.ndarray) -> np.ndarray:
    return scaler.inverse_transform(np.asarray(values, dtype=np.float64).reshape(-1, 1)).ravel()


def predict_next_close(
    model: keras.Model,
    scaler: MinMaxScaler,
    prices: list[float] | np.ndarray,
    window_size: int = WINDOW_SIZE,
) -> float:
    array = np.asarray(prices, dtype=np.float64).reshape(-1, 1)
    if array.shape[0] != window_size:
        raise ValueError(f"janela deve ter {window_size} preços")
    scaled = scaler.transform(array).reshape(1, window_size, 1)
    pred_scaled = model.predict(scaled, verbose=0)
    return float(invert_scale(scaler, pred_scaled.ravel())[0])
