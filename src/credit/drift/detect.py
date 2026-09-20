"""Testes estatísticos de drift: PSI (Population Stability Index) e KS.

Complementa o relatório do Evidently com uma tabela objetiva por feature,
atendendo ao requisito "relatório estatístico (PSI ou Kolmogorov-Smirnov)".
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

from src.credit import config as C

# Interpretação usual do PSI.
PSI_MINOR = 0.10   # < 0.10: estável
PSI_MAJOR = 0.25   # 0.10–0.25: mudança moderada; > 0.25: mudança significativa


def _psi_from_counts(expected_pct: np.ndarray, actual_pct: np.ndarray) -> float:
    eps = 1e-6
    expected_pct = np.clip(expected_pct, eps, None)
    actual_pct = np.clip(actual_pct, eps, None)
    return float(np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct)))


def numeric_psi(reference: pd.Series, current: pd.Series, bins: int = 10) -> float:
    """PSI com binning por quantis da referência."""
    quantiles = np.linspace(0, 1, bins + 1)
    edges = np.unique(np.quantile(reference, quantiles))
    edges[0], edges[-1] = -np.inf, np.inf
    exp = np.histogram(reference, bins=edges)[0] / len(reference)
    act = np.histogram(current, bins=edges)[0] / len(current)
    return _psi_from_counts(exp, act)


def categorical_psi(reference: pd.Series, current: pd.Series) -> float:
    cats = sorted(set(reference.dropna()) | set(current.dropna()))
    exp = reference.value_counts(normalize=True).reindex(cats, fill_value=0).to_numpy()
    act = current.value_counts(normalize=True).reindex(cats, fill_value=0).to_numpy()
    return _psi_from_counts(exp, act)


def _psi_verdict(psi: float) -> str:
    if psi < PSI_MINOR:
        return "estável"
    if psi < PSI_MAJOR:
        return "moderado"
    return "significativo"


def compute_drift_stats(reference: pd.DataFrame, current: pd.DataFrame) -> pd.DataFrame:
    """Tabela por feature com PSI, veredito e KS (numéricas)."""
    rows = []
    for col in C.NUMERIC_FEATURES:
        psi = numeric_psi(reference[col], current[col])
        ks = ks_2samp(reference[col], current[col])
        rows.append(
            {
                "feature": col,
                "type": "numeric",
                "psi": round(psi, 4),
                "psi_verdict": _psi_verdict(psi),
                "ks_statistic": round(float(ks.statistic), 4),
                "ks_pvalue": round(float(ks.pvalue), 6),
                "ks_drift": bool(ks.pvalue < 0.05),
            }
        )
    for col in C.CATEGORICAL_FEATURES:
        psi = categorical_psi(reference[col], current[col])
        rows.append(
            {
                "feature": col,
                "type": "categorical",
                "psi": round(psi, 4),
                "psi_verdict": _psi_verdict(psi),
                "ks_statistic": None,
                "ks_pvalue": None,
                "ks_drift": None,
            }
        )
    return pd.DataFrame(rows).sort_values("psi", ascending=False).reset_index(drop=True)
