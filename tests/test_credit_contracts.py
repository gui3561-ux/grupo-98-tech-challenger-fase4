from __future__ import annotations

import pandas as pd
import pytest

from src.credit.data.contracts import (
    DataContractViolationError,
    build_corrupted_batch,
    validate_credit_data,
)


def _valid_record() -> dict:
    return {
        "Age": 30,
        "Credit amount": 2500,
        "Duration": 12,
        "Sex": "female",
        "Job": 2,
        "Housing": "own",
        "Saving accounts": "little",
        "Checking account": "moderate",
        "Purpose": "car",
        "Risk": "good",
    }


def test_validate_credit_data_valid_passes():
    df = pd.DataFrame([_valid_record()])
    validated = validate_credit_data(df)
    assert len(validated) == 1
    assert validated.loc[0, "Age"] == 30


def test_validate_credit_data_underage_blocked():
    record = _valid_record()
    record["Age"] = 17  # Menor de idade
    df = pd.DataFrame([record])

    with pytest.raises(DataContractViolationError) as exc_info:
        validate_credit_data(df)
    assert "Age" in str(exc_info.value)


def test_validate_credit_data_invalid_credit_amount():
    record = _valid_record()
    record["Credit amount"] = -50  # Valor negativo
    df = pd.DataFrame([record])

    with pytest.raises(DataContractViolationError) as exc_info:
        validate_credit_data(df)
    assert "Credit amount" in str(exc_info.value)


def test_validate_credit_data_invalid_duration():
    record = _valid_record()
    record["Duration"] = 0  # Prazo zerado
    df = pd.DataFrame([record])

    with pytest.raises(DataContractViolationError) as exc_info:
        validate_credit_data(df)
    assert "Duration" in str(exc_info.value)


def test_validate_credit_data_invalid_category():
    record = _valid_record()
    record["Purpose"] = "crypto_scam"  # Categoria desconhecida
    df = pd.DataFrame([record])

    with pytest.raises(DataContractViolationError) as exc_info:
        validate_credit_data(df)
    assert "Purpose" in str(exc_info.value)


def test_validate_credit_data_null_in_required_field():
    record = _valid_record()
    record["Housing"] = None  # Nulo não permitido
    df = pd.DataFrame([record])

    with pytest.raises(DataContractViolationError) as exc_info:
        validate_credit_data(df)
    assert "Housing" in str(exc_info.value)


def test_build_corrupted_batch_intercepted():
    corrupted = build_corrupted_batch()
    with pytest.raises(DataContractViolationError) as exc_info:
        validate_credit_data(corrupted)

    assert exc_info.value.failure_cases is not None
    assert len(exc_info.value.failure_cases) >= 5

