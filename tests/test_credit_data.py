from __future__ import annotations

import pandas as pd
import pytest

from src.credit import config as C
from src.credit.data.preprocess import load_base_dataset, make_reference_production_split


def test_load_base_dataset_replaces_na_with_no_account(tmp_path, monkeypatch):
    csv_file = tmp_path / "german_credit_with_risk.csv"
    sample_df = pd.DataFrame(
        {
            "Age": [25, 40],
            "Sex": ["female", "male"],
            "Job": [2, 3],
            "Housing": ["own", "rent"],
            "Saving accounts": [None, "little"],
            "Checking account": ["moderate", None],
            "Credit amount": [1000, 2500],
            "Duration": [12, 24],
            "Purpose": ["radio/TV", "car"],
            "Risk": ["good", "bad"],
        }
    )
    sample_df.to_csv(csv_file, index=False)
    monkeypatch.setattr(C, "RAW_CSV", csv_file)

    loaded = load_base_dataset()
    assert loaded["Saving accounts"].tolist() == [C.NO_ACCOUNT_FILL, "little"]
    assert loaded["Checking account"].tolist() == ["moderate", C.NO_ACCOUNT_FILL]
    assert len(loaded) == 2


def test_load_base_dataset_missing_file_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "RAW_CSV", tmp_path / "non_existent.csv")
    with pytest.raises(FileNotFoundError):
        load_base_dataset()


def test_make_reference_production_split_stratification(tmp_path, monkeypatch):
    csv_file = tmp_path / "raw.csv"
    ref_file = tmp_path / "ref.csv"
    prod_file = tmp_path / "prod.csv"

    # Criar 100 linhas: 70 good e 30 bad
    risks = ["good"] * 70 + ["bad"] * 30
    df = pd.DataFrame(
        {
            "Age": [30] * 100,
            "Sex": ["male"] * 100,
            "Job": [2] * 100,
            "Housing": ["own"] * 100,
            "Saving accounts": ["little"] * 100,
            "Checking account": ["little"] * 100,
            "Credit amount": [2000] * 100,
            "Duration": [12] * 100,
            "Purpose": ["radio/TV"] * 100,
            "Risk": risks,
        }
    )
    df.to_csv(csv_file, index=False)

    monkeypatch.setattr(C, "RAW_CSV", csv_file)
    monkeypatch.setattr(C, "REFERENCE_CSV", ref_file)
    monkeypatch.setattr(C, "PRODUCTION_RAW_CSV", prod_file)

    ref, prod = make_reference_production_split(production_size=0.3, random_state=42)

    assert len(ref) == 70
    assert len(prod) == 30
    assert ref["Risk"].value_counts()["good"] == 49
    assert ref["Risk"].value_counts()["bad"] == 21
    assert prod["Risk"].value_counts()["good"] == 21
    assert prod["Risk"].value_counts()["bad"] == 9
    assert ref_file.exists()
    assert prod_file.exists()

