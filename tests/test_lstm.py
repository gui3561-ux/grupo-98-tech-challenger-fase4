from __future__ import annotations

import json

import numpy as np
import pytest
from sklearn.preprocessing import MinMaxScaler

from src.model.artifacts import invert_scale, predict_next_close, save_artifacts, load_artifacts
from src.model.lstm import build_lstm
from src.model.metrics import naive_from_windows, regression_metrics
from src.model.train import evaluate_in_price_space, train_lstm, write_metrics


def _synthetic_windows(n_samples: int = 80, window: int = 60, seed: int = 0):
    rng = np.random.default_rng(seed)
    walk = np.cumsum(rng.normal(0, 0.01, size=n_samples + window)) + 1.0
    xs, ys = [], []
    for i in range(window, len(walk)):
        xs.append(walk[i - window : i])
        ys.append(walk[i])
        if len(xs) >= n_samples:
            break
    x = np.asarray(xs, dtype=np.float64).reshape(-1, window, 1)
    y = np.asarray(ys, dtype=np.float64)
    return x, y


def test_train_lstm_emits_numeric_prediction():
    x, y = _synthetic_windows()
    split = 60
    model = train_lstm(x[:split], y[:split], x[split:], y[split:], epochs=2, patience=2, batch_size=16)
    pred = model.predict(x[:1], verbose=0)
    assert pred.shape[0] == 1
    assert np.isfinite(pred).all()


def test_metrics_written_with_lstm_and_naive(tmp_path):
    x, y = _synthetic_windows(n_samples=40)
    scaler = MinMaxScaler()
    scaler.fit(np.array([[0.5], [1.5]]))
    model = train_lstm(x[:30], y[:30], x[30:], y[30:], epochs=1, patience=1, batch_size=8)
    metrics = evaluate_in_price_space(model, scaler, x[30:], y[30:])
    path = write_metrics(metrics, models_dir=tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    for key in ("mae", "rmse", "mape"):
        assert key in payload["lstm"]
        assert key in payload["naive"]
        assert np.isfinite(payload["lstm"][key])
        assert np.isfinite(payload["naive"][key])


def test_naive_is_last_window_value():
    x = np.array([[[0.1], [0.2], [0.9]]], dtype=np.float64)
    assert naive_from_windows(x)[0] == pytest.approx(0.9)


def test_save_and_reload_reproduces_prediction(tmp_path):
    x, y = _synthetic_windows(n_samples=20)
    scaler = MinMaxScaler()
    prices = np.linspace(20.0, 40.0, 60).reshape(-1, 1)
    scaler.fit(prices)
    model = build_lstm()
    model.fit(x[:15], y[:15], epochs=1, verbose=0, batch_size=5)
    save_artifacts(model, scaler, models_dir=tmp_path)
    loaded_model, loaded_scaler = load_artifacts(tmp_path)
    raw_prices = prices.ravel().tolist()
    first = predict_next_close(model, scaler, raw_prices)
    second = predict_next_close(loaded_model, loaded_scaler, raw_prices)
    assert first == pytest.approx(second)
    assert np.isfinite(first)


def test_invert_scale_roundtrip():
    scaler = MinMaxScaler()
    scaler.fit(np.array([[10.0], [20.0]]))
    restored = invert_scale(scaler, np.array([0.0, 1.0]))
    assert restored[0] == pytest.approx(10.0)
    assert restored[1] == pytest.approx(20.0)


def test_regression_metrics_zero_error():
    y = np.array([10.0, 20.0])
    metrics = regression_metrics(y, y)
    assert metrics["mae"] == 0.0
    assert metrics["rmse"] == 0.0
    assert metrics["mape"] == 0.0
