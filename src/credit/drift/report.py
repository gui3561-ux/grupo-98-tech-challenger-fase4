"""Relatório de Drift com Evidently AI (Etapa 2).

Compara Referência × Produção e gera:
- `reports/drift_report.html`  — Data Drift + qualidade de classificação (Evidently).
- `reports/drift_stats.csv`    — PSI/KS por feature.
- `reports/drift_summary.md`   — resumo executivo (features degradadas + Concept Drift).
"""

from __future__ import annotations

import json

import pandas as pd
from evidently import BinaryClassification, DataDefinition, Dataset, Report
from evidently.presets import ClassificationPreset, DataDriftPreset
from sklearn.metrics import accuracy_score, roc_auc_score

from src.credit import config as C
from src.credit.drift.detect import PSI_MAJOR, compute_drift_stats
from src.credit.model.baseline import load_model, predict_frame


def _data_definition() -> DataDefinition:
    return DataDefinition(
        numerical_columns=C.NUMERIC_FEATURES,
        categorical_columns=C.CATEGORICAL_FEATURES,
        classification=[
            BinaryClassification(
                target=C.TARGET,
                prediction_labels=C.PREDICTION_LABEL,
                prediction_probas=C.PREDICTION_PROBA,
                pos_label=C.POSITIVE_LABEL,
            )
        ],
    )


def _performance(df: pd.DataFrame) -> dict:
    y_true = (df[C.TARGET] == C.POSITIVE_LABEL).astype(int)
    y_pred = (df[C.PREDICTION_LABEL] == C.POSITIVE_LABEL).astype(int)
    return {
        "roc_auc": round(float(roc_auc_score(y_true, df[C.PREDICTION_PROBA])), 4),
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
    }


def build_drift_report() -> dict:
    if not C.PRODUCTION_CSV.exists():
        raise FileNotFoundError(
            f"{C.PRODUCTION_CSV} não encontrado. Rode: python -m src.credit.data.simulate_drift"
        )
    model = load_model()
    reference = predict_frame(model, pd.read_csv(C.REFERENCE_CSV))
    production = predict_frame(model, pd.read_csv(C.PRODUCTION_CSV))

    # --- Evidently: Data Drift + qualidade de classificação (Concept Drift) ---
    definition = _data_definition()
    ref_ds = Dataset.from_pandas(reference, data_definition=definition)
    cur_ds = Dataset.from_pandas(production, data_definition=definition)

    report = Report([DataDriftPreset(), ClassificationPreset()])
    snapshot = report.run(current_data=cur_ds, reference_data=ref_ds)
    C.DRIFT_HTML.parent.mkdir(parents=True, exist_ok=True)
    snapshot.save_html(str(C.DRIFT_HTML))

    # --- Estatística explícita (PSI/KS) ---
    stats = compute_drift_stats(reference, production)
    stats.to_csv(C.DRIFT_STATS_CSV, index=False)

    # --- Concept Drift: performance esperada (holdout) × produção ---
    # A referência usa a métrica de HOLDOUT (out-of-sample) salva no treino; a
    # performance in-sample da referência é otimista e não serve de baseline justo.
    holdout = json.loads(C.MODEL_METRICS_PATH.read_text())
    perf_ref = {"roc_auc": holdout["roc_auc"], "accuracy": holdout["accuracy"]}
    perf_prod = _performance(production)

    _write_summary(stats, perf_ref, perf_prod)

    print(f"[drift_report] HTML  -> {C.DRIFT_HTML}")
    print(f"[drift_report] Stats -> {C.DRIFT_STATS_CSV}")
    print(f"[drift_report] Resumo-> {C.DRIFT_SUMMARY_MD}")
    print(
        f"[drift_report] Concept Drift: ROC-AUC {perf_ref['roc_auc']} (holdout) -> "
        f"{perf_prod['roc_auc']} | acc {perf_ref['accuracy']} -> {perf_prod['accuracy']}"
    )
    return {"stats": stats, "perf_reference": perf_ref, "perf_production": perf_prod}


def _df_to_markdown(df: pd.DataFrame) -> str:
    header = "| " + " | ".join(df.columns) + " |"
    sep = "|" + "|".join(["---"] * len(df.columns)) + "|"
    rows = [
        "| " + " | ".join("" if pd.isna(v) else str(v) for v in row) + " |"
        for row in df.itertuples(index=False)
    ]
    return "\n".join([header, sep, *rows])


def _write_summary(stats: pd.DataFrame, perf_ref: dict, perf_prod: dict) -> None:
    drifted = stats[stats["psi"] >= PSI_MAJOR]["feature"].tolist()
    auc_drop = round(perf_ref["roc_auc"] - perf_prod["roc_auc"], 4)
    acc_drop = round(perf_ref["accuracy"] - perf_prod["accuracy"], 4)

    lines = [
        "# Relatório de Drift — Etapa 2",
        "",
        "Comparação entre o **Dataset de Referência** (treino do baseline) e o ",
        "**Dataset de Produção** (com degradação injetada simulando a passagem do tempo).",
        "",
        "## Data Drift (mudança de distribuição das features)",
        "",
        f"Features com drift **significativo** (PSI ≥ {PSI_MAJOR}): "
        + (", ".join(f"`{f}`" for f in drifted) if drifted else "nenhuma"),
        "",
        "PSI/KS por feature (detalhe em `drift_stats.csv`):",
        "",
        _df_to_markdown(stats),
        "",
        "## Concept Drift (degradação do modelo)",
        "",
        "Referência = performance de **holdout** (out-of-sample) do treino; "
        "Produção = mesmo modelo sobre o dataset com drift (labels reais preservados).",
        "",
        "| Métrica | Referência (holdout) | Produção | Queda |",
        "|---|---|---|---|",
        f"| ROC-AUC | {perf_ref['roc_auc']} | {perf_prod['roc_auc']} | {auc_drop} |",
        f"| Accuracy | {perf_ref['accuracy']} | {perf_prod['accuracy']} | {acc_drop} |",
        "",
        "> O relatório visual completo do Evidently está em `drift_report.html`.",
        "",
    ]
    C.DRIFT_SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    build_drift_report()
