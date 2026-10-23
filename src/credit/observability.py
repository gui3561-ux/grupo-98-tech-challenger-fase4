"""Módulo de Observabilidade, Logging Estruturado e Rastreamento com MLflow (Etapa 3).

Centraliza:
1. Configuração de logger estruturado operacional para todas as etapas.
2. Medição de latência e saúde operacional por estágio do pipeline.
3. Rastreamento de experimentos, hiperparâmetros, métricas e artefatos no MLflow.
"""

from __future__ import annotations

import logging
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

import mlflow
import pandas as pd

from src.credit import config as C

# Desabilita hints invasivos do agente MLflow
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"

EXPERIMENT_NAME = "credit-scoring-mlops"
DEFAULT_TRACKING_URI = "sqlite:///mlflow.db"
LOG_FILE = Path("reports") / "pipeline_execution.log"


def configure_logger(name: str = "credit.pipeline", level: int = logging.INFO) -> logging.Logger:
    """Configura logger estruturado com saída em console e arquivo de log operacional."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


logger = configure_logger()


def setup_mlflow(tracking_uri: str = DEFAULT_TRACKING_URI) -> None:
    """Inicializa o tracking local do MLflow e define o experimento oficial."""
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(EXPERIMENT_NAME)
    logger.info("MLflow configurado com Tracking URI: '%s' | Experimento: '%s'", tracking_uri, EXPERIMENT_NAME)


@contextmanager
def track_stage_latency(stage_name: str) -> Generator[dict[str, float], None, None]:
    """Context manager para cronometrar a duração de execução de um estágio do pipeline."""
    result: dict[str, float] = {"duration": 0.0}
    start = time.perf_counter()
    logger.info(">>> Iniciando estágio: [%s]", stage_name)
    try:
        yield result
    finally:
        elapsed = time.perf_counter() - start
        result["duration"] = round(elapsed, 4)
        logger.info("<<< Concluído estágio: [%s] em %.4f segundos", stage_name, elapsed)


def log_operational_metrics(
    latencies: dict[str, float],
    processed_rows: dict[str, int],
    drift_stats_df: Any | None = None,
    eval_metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Registra no MLflow métricas operacionais, parâmetros e contagem de alertas.

    Retorna o dicionário de métricas registradas.
    """
    logged_metrics: dict[str, float] = {}

    # 1. Latências por estágio
    for stage, duration in latencies.items():
        key = f"latency_{stage}_seconds"
        mlflow.log_metric(key, duration)
        logged_metrics[key] = duration

    # 2. Volume de registros processados
    for dataset_name, count in processed_rows.items():
        key = f"rows_{dataset_name}"
        mlflow.log_metric(key, count)
        logged_metrics[key] = count

    # 3. Métricas do modelo baseline
    if eval_metrics:
        for metric_name in ["roc_auc", "accuracy", "f1_bad"]:
            if metric_name in eval_metrics:
                key = f"model_{metric_name}"
                val = float(eval_metrics[metric_name])
                mlflow.log_metric(key, val)
                logged_metrics[key] = val

    # 4. Métricas estatísticas de drift e contagem de alertas
    critical_alerts = 0
    if drift_stats_df is not None:
        for _, row in drift_stats_df.iterrows():
            feat = row["feature"].replace(" ", "_")
            psi = float(row["psi"])
            mlflow.log_metric(f"psi_{feat}", psi)
            logged_metrics[f"psi_{feat}"] = psi
            if row.get("ks_pvalue") is not None and not pd.isna(row["ks_pvalue"]):
                mlflow.log_metric(f"ks_pvalue_{feat}", float(row["ks_pvalue"]))

            if row.get("psi_verdict") == "significativo":
                critical_alerts += 1

    mlflow.log_metric("drift_critical_alerts_count", critical_alerts)
    logged_metrics["drift_critical_alerts_count"] = critical_alerts

    # Tags de status
    mlflow.set_tag("pipeline.status", "success")
    mlflow.set_tag("pipeline.drift_alert", "CRITICAL" if critical_alerts > 0 else "OK")

    logger.info(
        "Métricas registradas no MLflow: latência total=%.4fs, alertas críticos de drift=%d",
        sum(latencies.values()),
        critical_alerts,
    )
    return logged_metrics


def log_pipeline_artifacts() -> None:
    """Registra relatórios e modelos gerados como artefatos rastreáveis na run do MLflow."""
    artifacts = [
        C.DRIFT_HTML,
        C.DRIFT_STATS_CSV,
        C.DRIFT_SUMMARY_MD,
        C.MODEL_PATH,
        C.MODEL_METRICS_PATH,
        LOG_FILE,
    ]
    for art in artifacts:
        if art.exists():
            mlflow.log_artifact(str(art))
            logger.info("Artefato registrado no MLflow: %s", art)
        else:
            logger.warning("Artefato esperado não encontrado para registro: %s", art)
