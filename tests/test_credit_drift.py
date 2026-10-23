from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.credit import config as C
from src.credit.data.simulate_drift import simulate_production_drift
from src.credit.drift.detect import (
    _psi_verdict,
    categorical_psi,
    compute_drift_stats,
    numeric_psi,
)


def test_psi_identical_distributions():
    s = pd.Series(np.random.normal(100, 15, size=500))
    psi = numeric_psi(s, s)
    assert psi < 0.05
    assert _psi_verdict(psi) == "estável"


def test_psi_shifted_distribution():
    ref = pd.Series(np.random.normal(100, 15, size=500))
    shifted = pd.Series(np.random.normal(150, 15, size=500))
    psi = numeric_psi(ref, shifted)
    assert psi > 0.25
    assert _psi_verdict(psi) == "significativo"


def test_categorical_psi():
    ref = pd.Series(["little"] * 80 + ["rich"] * 20)
    current_same = pd.Series(["little"] * 80 + ["rich"] * 20)
    current_shifted = pd.Series(["little"] * 20 + ["rich"] * 80)

    assert categorical_psi(ref, current_same) < 0.05
    assert categorical_psi(ref, current_shifted) > 0.25


def test_compute_drift_stats_dataframe():
    ref = pd.DataFrame(
        {
            "Age": [25, 30, 35, 40, 45, 50],
            "Credit amount": [1000, 2000, 3000, 4000, 5000, 6000],
            "Duration": [12, 18, 24, 30, 36, 42],
            "Sex": ["male", "female", "male", "female", "male", "female"],
            "Job": [1, 2, 2, 3, 1, 2],
            "Housing": ["own", "rent", "own", "own", "free", "rent"],
            "Saving accounts": ["little", "rich", "little", "no_account", "little", "moderate"],
            "Checking account": ["little", "moderate", "no_account", "rich", "little", "no_account"],
            "Purpose": ["car", "car", "radio/TV", "radio/TV", "education", "business"],
            "Risk": ["good", "good", "bad", "bad", "good", "bad"],
        }
    )
    # Drift numérico intencional em Age e Credit amount
    cur = ref.copy()
    cur["Age"] = cur["Age"] - 10
    cur["Credit amount"] = cur["Credit amount"] * 2

    stats = compute_drift_stats(ref, cur)
    assert len(stats) == len(C.FEATURES)
    assert "psi" in stats.columns
    assert "psi_verdict" in stats.columns
    assert "ks_drift" in stats.columns

    # Numéricas devem ter estatística KS
    num_stats = stats[stats["type"] == "numeric"]
    assert len(num_stats) == len(C.NUMERIC_FEATURES)
    assert num_stats["ks_statistic"].notna().all()


def test_simulate_production_drift(tmp_path, monkeypatch):
    raw_prod = tmp_path / "prod_raw.csv"
    out_prod = tmp_path / "prod.csv"

    df = pd.DataFrame(
        {
            "Age": [30, 40, 50],
            "Credit amount": [1000, 2000, 3000],
            "Duration": [12, 24, 36],
            "Sex": ["male", "female", "male"],
            "Job": [2, 2, 3],
            "Housing": ["own", "rent", "own"],
            "Saving accounts": [None, "little", "rich"],
            "Checking account": [None, "little", "moderate"],
            "Purpose": ["car", "radio/TV", "business"],
            "Risk": ["good", "bad", "good"],
        }
    )
    df.to_csv(raw_prod, index=False)

    monkeypatch.setattr(C, "PRODUCTION_RAW_CSV", raw_prod)
    monkeypatch.setattr(C, "PRODUCTION_CSV", out_prod)

    drifted = simulate_production_drift(random_state=42)

    assert out_prod.exists()
    assert (drifted["Age"] >= 18).all()
    # Credit amount inflacionado (~1.6x)
    assert drifted["Credit amount"].mean() > df["Credit amount"].mean()
    # NaN preenchido com no_account
    assert not drifted["Saving accounts"].isna().any()

