from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from tensorflow import keras

from src.data.collect import collect_prices
from src.data.preprocess import chronological_split, clean_series, fit_scaler, transform_close
from src.data.windows import make_windows
from src.model.artifacts import invert_scale, predict_next_close, save_artifacts
from src.model.lstm import build_lstm
from src.model.metrics import naive_from_windows, regression_metrics
from src.settings import METRICS_FILENAME, MODELS_DIR, WINDOW_SIZE


def train_lstm(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_val: np.ndarray,
    y_val: np.ndarray,
    epochs: int = 40,
    patience: int = 5,
    batch_size: int = 32,
) -> keras.Model:
    model = build_lstm()
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=patience,
            restore_best_weights=True,
        )
    ]
    model.fit(
        x_train,
        y_train,
        validation_data=(x_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=0,
        shuffle=False,
    )
    return model


def evaluate_in_price_space(
    model: keras.Model,
    scaler,
    x_test: np.ndarray,
    y_test: np.ndarray,
) -> dict[str, dict[str, float]]:
    lstm_scaled = model.predict(x_test, verbose=0).ravel()
    naive_scaled = naive_from_windows(x_test)
    y_true = invert_scale(scaler, y_test)
    lstm_price = invert_scale(scaler, lstm_scaled)
    naive_price = invert_scale(scaler, naive_scaled)
    return {
        "lstm": regression_metrics(y_true, lstm_price),
        "naive": regression_metrics(y_true, naive_price),
    }


def write_metrics(metrics: dict, models_dir: Path | None = None) -> Path:
    directory = models_dir or MODELS_DIR
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / METRICS_FILENAME
    path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return path


def run_training(
    models_dir: Path | None = None,
    cache_path: Path | None = None,
    epochs: int = 40,
) -> dict:
    raw = collect_prices(cache_path=cache_path)
    cleaned = clean_series(raw)
    train_df, val_df, test_df = chronological_split(cleaned)
    scaler = fit_scaler(train_df)
    train_s = transform_close(train_df, scaler)
    val_s = transform_close(val_df, scaler)
    test_s = transform_close(test_df, scaler)

    x_train, y_train, _ = make_windows(train_s)
    x_val, y_val, _ = make_windows(val_s)
    x_test, y_test, _ = make_windows(test_s)

    model = train_lstm(x_train, y_train, x_val, y_val, epochs=epochs)
    metrics = evaluate_in_price_space(model, scaler, x_test, y_test)
    save_artifacts(model, scaler, models_dir=models_dir)
    write_metrics(metrics, models_dir=models_dir)

    sample = cleaned["close"].iloc[-WINDOW_SIZE:].tolist()
    sample_pred = predict_next_close(model, scaler, sample)
    return {"metrics": metrics, "sample_prediction": sample_pred}


if __name__ == "__main__":
    result = run_training()
    print(json.dumps(result, indent=2))
