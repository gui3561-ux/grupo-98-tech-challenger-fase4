"""Orquestrador Unificado do Pipeline de Credit Scoring MLOps (Etapa 3).

Executa todo o ciclo de vida operacional dentro de uma run do MLflow:
1. Validação de contratos de dados (Pandera).
2. Particionamento e preparação de dataset (Referência × Produção).
3. Treinamento e avaliação do modelo baseline (XGBoost).
4. Simulação de drift de mercado.
5. Detecção de Data Drift e Concept Drift com relatórios Evidently AI e PSI/KS.
6. Centralização de métricas de saúde operacional e rastreabilidade de artefatos.

Uso:
    uv run python -m src.credit.pipeline
"""

from __future__ import annotations

import json
from pathlib import Path

import mlflow
import pandas as pd

from src.credit import config as C
from src.credit.data.preprocess import load_base_dataset, make_reference_production_split
from src.credit.data.simulate_drift import simulate_production_drift
from src.credit.drift.report import build_drift_report
from src.credit.model.baseline import train_baseline
from src.credit.observability import (
    logger,
    log_operational_metrics,
    log_pipeline_artifacts,
    setup_mlflow,
    track_stage_latency,
)


def run_pipeline() -> dict[str, str | float]:
    """Executa o pipeline completo de ponta a ponta e registra na run do MLflow."""
    setup_mlflow()

    logger.info("=================================================================")
    logger.info("   INICIANDO PIPELINE UNIFICADO DE CRÉDITO COM MLFLOW TRACKING   ")
    logger.info("=================================================================")

    latencies: dict[str, float] = {}
    processed_rows: dict[str, int] = {}

    with mlflow.start_run(run_name="credit_scoring_mlops_pipeline") as run:
        run_id = run.info.run_id
        logger.info("MLflow Run iniciada com ID: %s", run_id)

        # Log de parâmetros de governança e configuração
        mlflow.log_params(
            {
                "random_state": C.RANDOM_STATE,
                "production_size": 0.3,
                "target_column": C.TARGET,
                "positive_label": C.POSITIVE_LABEL,
                "model_algorithm": "XGBClassifier",
                "validation_framework": "Pandera",
                "drift_framework": "Evidently AI + SciPy (PSI/KS)",
            }
        )

        # --- Estágio 1: Validação de Contrato e Carga ---
        with track_stage_latency("data_validation") as s1:
            base_df = load_base_dataset(validate=True)
            processed_rows["raw_base"] = len(base_df)
        latencies["validation"] = s1["duration"]

        # --- Estágio 2: Split Referência × Produção ---
        with track_stage_latency("data_split") as s2:
            ref_df, prod_raw_df = make_reference_production_split()
            processed_rows["reference"] = len(ref_df)
            processed_rows["production_raw"] = len(prod_raw_df)
        latencies["split"] = s2["duration"]

        # --- Estágio 3: Treinamento do Modelo Baseline ---
        with track_stage_latency("model_training") as s3:
            train_metrics = train_baseline()
        latencies["training"] = s3["duration"]

        # --- Estágio 4: Simulação de Drift ---
        with track_stage_latency("drift_simulation") as s4:
            prod_drifted = simulate_production_drift()
            processed_rows["production_drifted"] = len(prod_drifted)
        latencies["simulation"] = s4["duration"]

        # --- Estágio 5: Detecção de Drift e Relatórios ---
        with track_stage_latency("drift_detection") as s5:
            drift_results = build_drift_report()
            drift_stats_df = drift_results["stats"]
        latencies["drift_detection"] = s5["duration"]

        # --- Registro de Métricas Operacionais e Artefatos ---
        logger.info("Registrando métricas de saúde operacional e artefatos no MLflow...")
        logged_metrics = log_operational_metrics(
            latencies=latencies,
            processed_rows=processed_rows,
            drift_stats_df=drift_stats_df,
            eval_metrics=train_metrics,
        )
        log_pipeline_artifacts()

        logger.info("=================================================================")
        logger.info("   PIPELINE UNIFICADO CONCLUÍDO COM SUCESSO!                    ")
        logger.info("   Run ID: %s", run_id)
        logger.info("   Visualize o dashboard executando: uv run mlflow ui          ")
        logger.info("=================================================================")

        return {
            "run_id": run_id,
            "total_latency_seconds": round(sum(latencies.values()), 4),
            "roc_auc_holdout": train_metrics["roc_auc"],
            "drift_critical_alerts": logged_metrics["drift_critical_alerts_count"],
        }


def main() -> None:
    run_pipeline()


if __name__ == "__main__":
    main()

