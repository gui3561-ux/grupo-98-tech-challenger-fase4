"""Carga e split Referência × Produção (base para a Etapa 1 e Etapa 2).

- `load_base_dataset`: lê o CSV com target e normaliza os NaN de conta.
- `make_reference_production_split`: separa de forma estratificada o dataset de
  Referência (treino/baseline) do dataset de Produção-base (semente do drift).
"""

from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split

from src.credit import config as C


def load_base_dataset() -> pd.DataFrame:
    """Lê o dataset com target e trata NaN de conta como categoria 'no_account'."""
    if not C.RAW_CSV.exists():
        raise FileNotFoundError(
            f"{C.RAW_CSV} não encontrado. Rode: python -m src.credit.data.make_dataset"
        )
    df = pd.read_csv(C.RAW_CSV)
    for col in ["Saving accounts", "Checking account"]:
        df[col] = df[col].fillna(C.NO_ACCOUNT_FILL)
    return df


def make_reference_production_split(
    production_size: float = 0.3,
    random_state: int = C.RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Divide o dataset base em Referência e Produção-base (estratificado por Risk).

    Grava `data/reference/reference.csv` e `data/production/production_raw.csv`.
    O dataset de produção ainda **não** tem drift — isso é feito em `simulate_drift`.
    """
    df = load_base_dataset()
    reference, production = train_test_split(
        df,
        test_size=production_size,
        random_state=random_state,
        stratify=df[C.TARGET],
    )
    reference = reference.reset_index(drop=True)
    production = production.reset_index(drop=True)

    C.REFERENCE_CSV.parent.mkdir(parents=True, exist_ok=True)
    C.PRODUCTION_RAW_CSV.parent.mkdir(parents=True, exist_ok=True)
    reference.to_csv(C.REFERENCE_CSV, index=False)
    production.to_csv(C.PRODUCTION_RAW_CSV, index=False)

    print(f"[preprocess] Referência: {len(reference)} linhas -> {C.REFERENCE_CSV}")
    print(f"[preprocess] Produção-base: {len(production)} linhas -> {C.PRODUCTION_RAW_CSV}")
    return reference, production


if __name__ == "__main__":
    make_reference_production_split()
