from __future__ import annotations

import math
import time
from contextlib import asynccontextmanager
from pathlib import Path

import psutil
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field, field_validator

from src.model.artifacts import load_artifacts, predict_next_close
from src.settings import HORIZON, MODELS_DIR, TICKER, WINDOW_SIZE


class PredictRequest(BaseModel):
    prices: list[float] = Field(
        ...,
        min_length=WINDOW_SIZE,
        max_length=WINDOW_SIZE,
        description="60 fechamentos diários consecutivos, do mais antigo ao mais recente",
    )

    @field_validator("prices")
    @classmethod
    def finite_prices(cls, value: list[float]) -> list[float]:
        if any(item is None or not math.isfinite(item) for item in value):
            raise ValueError("todos os preços devem ser números finitos")
        return value


class PredictResponse(BaseModel):
    ticker: str = Field(description="Símbolo da ação prevista")
    horizon: str = Field(description="Horizonte da previsão (próximo pregão)")
    predicted_close: float = Field(description="Fechamento previsto para D+1")


class PredictMetrics:
    def __init__(self) -> None:
        self.predict_count = 0
        self.latency_sum = 0.0

    def observe(self, seconds: float) -> None:
        self.predict_count += 1
        self.latency_sum += seconds


class ArtifactPredictor:
    def __init__(self, model, scaler) -> None:
        self._model = model
        self._scaler = scaler

    def predict(self, prices: list[float]) -> float:
        return predict_next_close(self._model, self._scaler, prices)


def load_predictor(models_dir: Path) -> ArtifactPredictor | None:
    try:
        model, scaler = load_artifacts(models_dir)
    except Exception:
        return None
    return ArtifactPredictor(model, scaler)


def _prometheus_metrics(metrics: PredictMetrics) -> str:
    process = psutil.Process()
    cpu = process.cpu_times()
    rss = process.memory_info().rss
    lines = [
        "# HELP predict_requests_total Total de previsoes D+1 servidas",
        "# TYPE predict_requests_total counter",
        f"predict_requests_total {metrics.predict_count}",
        "# HELP predict_latency_seconds Latencia acumulada das previsoes",
        "# TYPE predict_latency_seconds summary",
        f"predict_latency_seconds_sum {metrics.latency_sum}",
        f"predict_latency_seconds_count {metrics.predict_count}",
        "# HELP process_cpu_seconds_total Tempo de CPU do processo",
        "# TYPE process_cpu_seconds_total counter",
        f"process_cpu_seconds_total {cpu.user + cpu.system}",
        "# HELP process_resident_memory_bytes Memoria RSS do processo",
        "# TYPE process_resident_memory_bytes gauge",
        f"process_resident_memory_bytes {rss}",
        "",
    ]
    return "\n".join(lines)


def create_app(models_dir: Path | None = None) -> FastAPI:
    directory = models_dir or MODELS_DIR

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.predictor = load_predictor(directory)
        app.state.metrics = PredictMetrics()
        yield

    app = FastAPI(
        title="PETR4 LSTM API",
        description="Recebe 60 fechamentos históricos e devolve o fechamento previsto de PETR4.SA no próximo pregão (D+1).",
        lifespan=lifespan,
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready")
    def ready() -> JSONResponse:
        predictor = getattr(app.state, "predictor", None)
        if predictor is None:
            return JSONResponse(status_code=503, content={"status": "not_ready"})
        return JSONResponse(status_code=200, content={"status": "ready"})

    @app.get("/metrics")
    def metrics() -> PlainTextResponse:
        current: PredictMetrics = getattr(app.state, "metrics", PredictMetrics())
        return PlainTextResponse(_prometheus_metrics(current), media_type="text/plain; version=0.0.4")

    @app.post("/predict", response_model=PredictResponse)
    def predict(body: PredictRequest) -> PredictResponse:
        predictor: ArtifactPredictor | None = getattr(app.state, "predictor", None)
        if predictor is None:
            raise HTTPException(status_code=503, detail="Modelo não está pronto")
        started = time.perf_counter()
        try:
            predicted = predictor.predict(body.prices)
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=500, detail="Erro interno ao gerar a previsão") from None
        elapsed = time.perf_counter() - started
        app.state.metrics.observe(elapsed)
        return PredictResponse(ticker=TICKER, horizon=HORIZON, predicted_close=predicted)

    return app


app = create_app()
