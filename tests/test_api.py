from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sklearn.preprocessing import MinMaxScaler

from src.api.main import ArtifactPredictor, PredictRequest, create_app
from src.model.artifacts import save_artifacts
from src.model.lstm import build_lstm
from src.settings import WINDOW_SIZE


@pytest.fixture
def artifact_dir(tmp_path):
    scaler = MinMaxScaler()
    prices = np.linspace(20.0, 40.0, WINDOW_SIZE).reshape(-1, 1)
    scaler.fit(prices)
    rng = np.random.default_rng(1)
    x = rng.random((8, WINDOW_SIZE, 1))
    y = rng.random((8,))
    model = build_lstm()
    model.fit(x, y, epochs=1, verbose=0, batch_size=4)
    save_artifacts(model, scaler, models_dir=tmp_path)
    return tmp_path, prices.ravel().tolist()


@pytest.fixture
def client(artifact_dir):
    directory, prices = artifact_dir
    app = create_app(models_dir=directory)
    with TestClient(app) as test_client:
        yield test_client, prices, app


def test_predict_success(client):
    test_client, prices, _app = client
    response = test_client.post("/predict", json={"prices": prices})
    assert response.status_code == 200
    body = response.json()
    assert body["ticker"] == "PETR4.SA"
    assert body["horizon"] == "D+1"
    assert isinstance(body["predicted_close"], float)
    assert np.isfinite(body["predicted_close"])


def test_wrong_window_size_does_not_call_predict(client):
    test_client, prices, app = client
    calls: list[list[float]] = []
    original = app.state.predictor.predict

    def wrapped(values: list[float]) -> float:
        calls.append(values)
        return original(values)

    app.state.predictor.predict = wrapped  # type: ignore[method-assign]
    too_short = test_client.post("/predict", json={"prices": prices[:59]})
    too_long = test_client.post("/predict", json={"prices": prices + [1.0]})
    assert too_short.status_code == 422
    assert too_long.status_code == 422
    assert calls == []


def test_non_finite_rejected_without_inference(client):
    test_client, prices, app = client
    calls: list[list[float]] = []
    original = app.state.predictor.predict

    def wrapped(values: list[float]) -> float:
        calls.append(values)
        return original(values)

    app.state.predictor.predict = wrapped  # type: ignore[method-assign]
    payload = list(prices)
    payload[0] = None
    response = test_client.post("/predict", json={"prices": payload})
    assert response.status_code == 422
    assert calls == []

    infinite = list(prices)
    infinite[0] = float("inf")
    with pytest.raises(ValidationError):
        PredictRequest(prices=infinite)


def test_inference_error_is_generic_500(client):
    test_client, prices, app = client

    def boom(_values: list[float]) -> float:
        raise RuntimeError("/secret/models/lstm_petr4.keras traceback")

    app.state.predictor.predict = boom  # type: ignore[method-assign]
    response = test_client.post("/predict", json={"prices": prices})
    assert response.status_code == 500
    payload = response.text
    assert "traceback" not in payload.lower()
    assert "/secret/models" not in payload
    assert "Erro interno ao gerar a previsão" in payload


def test_openapi_describes_predict_contract(client):
    test_client, _prices, _app = client
    docs = test_client.get("/docs")
    spec = test_client.get("/openapi.json")
    assert docs.status_code == 200
    assert spec.status_code == 200
    schema = spec.json()
    predict = schema["paths"]["/predict"]["post"]
    assert predict is not None
    request_schema = schema["components"]["schemas"]["PredictRequest"]
    prices_schema = request_schema["properties"]["prices"]
    assert prices_schema["minItems"] == 60
    assert prices_schema["maxItems"] == 60
    response_schema = schema["components"]["schemas"]["PredictResponse"]
    assert "predicted_close" in response_schema["properties"]
    assert "horizon" in response_schema["properties"]
    description = schema.get("info", {}).get("description", "") + str(predict)
    assert "D+1" in description or "próximo pregão" in description.lower() or "horizon" in str(response_schema)


def test_health_and_ready_ok(client):
    test_client, _prices, _app = client
    assert test_client.get("/health").status_code == 200
    ready = test_client.get("/ready")
    assert ready.status_code == 200
    assert ready.json()["status"] == "ready"


def test_ready_fails_without_model(tmp_path):
    app = create_app(models_dir=tmp_path)
    with TestClient(app) as test_client:
        assert test_client.get("/health").status_code == 200
        ready = test_client.get("/ready")
        assert ready.status_code == 503


def test_metrics_after_predict(client):
    test_client, prices, _app = client
    before = test_client.get("/metrics")
    assert before.status_code == 200
    assert "process_cpu_seconds_total" in before.text
    assert "process_resident_memory_bytes" in before.text
    test_client.post("/predict", json={"prices": prices})
    after = test_client.get("/metrics")
    assert "predict_requests_total 1" in after.text
    assert "predict_latency_seconds_sum" in after.text
    assert "predict_latency_seconds_count 1" in after.text


def test_api_sources_do_not_depend_on_yfinance():
    api_dir = Path("src/api")
    for path in api_dir.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "yfinance" not in text
        assert "src.data" not in text
        assert "yf.download" not in text


def test_predictor_type_exists():
    assert ArtifactPredictor is not None
