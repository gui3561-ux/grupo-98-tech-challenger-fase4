from __future__ import annotations

import pandas as pd
import pytest

from src.credit import config as C
from src.credit.model.baseline import (
    _to_binary,
    build_pipeline,
    load_model,
    predict_frame,
)


def test_to_binary_mapping():
    series = pd.Series(["good", "bad", "good", "bad"])
    binary = _to_binary(series)
    assert binary.tolist() == [0, 1, 0, 1]


def test_build_pipeline_fits_and_predicts():
    df = pd.DataFrame(
        {
            "Age": [25, 45, 30, 50, 22, 60],
            "Credit amount": [1000, 5000, 2000, 7000, 1500, 3000],
            "Duration": [12, 36, 18, 48, 12, 24],
            "Sex": ["female", "male", "female", "male", "female", "male"],
            "Job": [2, 3, 1, 2, 0, 3],
            "Housing": ["own", "rent", "own", "free", "rent", "own"],
            "Saving accounts": ["little", "rich", "little", "no_account", "little", "moderate"],
            "Checking account": ["little", "moderate", "no_account", "rich", "little", "no_account"],
            "Purpose": ["radio/TV", "car", "furniture/equipment", "radio/TV", "education", "business"],
            "Risk": ["good", "bad", "good", "bad", "good", "bad"],
        }
    )
    X = df[C.FEATURES]
    y = _to_binary(df[C.TARGET])

    pipe = build_pipeline()
    pipe.fit(X, y)

    # Testar com categoria nunca vista para validar handle_unknown="ignore"
    test_df = X.copy()
    test_df.loc[0, "Purpose"] = "unknown_category"

    proba = pipe.predict_proba(test_df)
    assert proba.shape == (6, 2)
    assert (proba >= 0.0).all() and (proba <= 1.0).all()


def test_predict_frame_appends_columns():
    df = pd.DataFrame(
        {
            "Age": [25, 45],
            "Credit amount": [1000, 5000],
            "Duration": [12, 36],
            "Sex": ["female", "male"],
            "Job": [2, 3],
            "Housing": ["own", "rent"],
            "Saving accounts": ["little", "rich"],
            "Checking account": ["little", "moderate"],
            "Purpose": ["radio/TV", "car"],
            "Risk": ["good", "bad"],
        }
    )
    pipe = build_pipeline()
    pipe.fit(df[C.FEATURES], _to_binary(df[C.TARGET]))

    result = predict_frame(pipe, df)
    assert C.PREDICTION_PROBA in result.columns
    assert C.PREDICTION_LABEL in result.columns
    assert set(result[C.PREDICTION_LABEL].unique()).issubset({"good", "bad"})
    assert (result[C.PREDICTION_PROBA] >= 0.0).all() and (result[C.PREDICTION_PROBA] <= 1.0).all()


def test_load_model_missing_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "MODEL_PATH", tmp_path / "missing.joblib")
    with pytest.raises(FileNotFoundError):
        load_model()

