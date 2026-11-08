"""Aumento de dados sintéticos (cópula gaussiana condicional por classe) para o German Credit.

Motivação: o edital pede dataset com >= 5.000 amostras e o German Credit tem 1.000.
Este módulo acrescenta **4.000 linhas sintéticas** ao CSV bruto
(``data/raw/german_credit_with_risk.csv``), mantendo **exatamente as mesmas colunas**
(Age, Sex, Job, Housing, Saving accounts, Checking account, Credit amount, Duration,
Purpose, Risk). Não há coluna de marcação: por convenção as 1.000 primeiras linhas são
reais (``config.N_REAL_ROWS``) e as 4.000 seguintes são sintéticas.

Como as linhas são geradas:
- Uma cópula gaussiana é ajustada **separadamente para cada classe** (``Risk`` good/bad),
  preservando P(X | Risk) e, portanto, a relação entre as variáveis e o alvo.
- A proporção das classes segue a das linhas reais de cada partição.

Garantias contra *data leakage*:
- As linhas sintéticas de **Referência** (primeiras ``N_SYNTH_REFERENCE`` sintéticas) são geradas
  SOMENTE a partir das linhas reais da partição de referência.
- As de **Produção** (restantes) são geradas SOMENTE a partir das linhas reais da partição de
  produção. A partição real usa o mesmo split estratificado de ``preprocess``.
- ``preprocess.make_reference_production_split`` respeita essa ordem ao separar os datasets.
- O drift continua sendo injetado depois, em ``simulate_drift``.

Idempotente: só as 1.000 primeiras linhas do CSV são lidas como base real.

Uso:
    uv run python -m src.credit.data.make_dataset      # 1.000 linhas reais (com Risk)
    uv run python -m src.credit.data.augment_dataset   # acrescenta 4.000 sintéticas
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm
from sklearn.model_selection import train_test_split

from src.credit import config as C
from src.credit.data.contracts import validate_credit_data

# Ordem de colunas idêntica à do dataset original.
OUTPUT_COLUMNS = [
    "Age",
    "Sex",
    "Job",
    "Housing",
    "Saving accounts",
    "Checking account",
    "Credit amount",
    "Duration",
    "Purpose",
    "Risk",
]
MODEL_COLUMNS = [c for c in OUTPUT_COLUMNS if c != C.TARGET]
CATEGORICAL_COLS = set(C.CATEGORICAL_FEATURES)
NUMERIC_INT = C.NUMERIC_FEATURES


def _to_normal_scores(col: pd.Series, rng: np.random.Generator, categorical: bool) -> np.ndarray:
    """Transforma uma coluna em scores normais via CDF empírica (com jitter nos empates)."""
    n = len(col)
    if categorical:
        codes, _ = pd.factorize(col, sort=True)
        counts = np.bincount(codes)
        upper = np.cumsum(counts) / n
        lower = upper - counts / n
        u = rng.uniform(lower[codes], upper[codes])
    else:
        ranks = col.rank(method="average").to_numpy()
        u = (ranks - rng.uniform(0.0, 1.0, size=n)) / n
    return norm.ppf(np.clip(u, 1e-6, 1 - 1e-6))


def _from_normal_scores(z: np.ndarray, original: pd.Series, categorical: bool) -> np.ndarray:
    """Mapeia scores normais de volta para o domínio original via quantis empíricos."""
    u = norm.cdf(z)
    if categorical:
        cats = sorted(original.unique(), key=lambda v: str(v))
        probs = original.value_counts(normalize=True).reindex(cats).to_numpy()
        edges = np.cumsum(probs)
        edges[-1] = 1.0
        idx = np.searchsorted(edges, u, side="right").clip(0, len(cats) - 1)
        return np.asarray(cats, dtype=object)[idx]
    return np.quantile(original.to_numpy(), u)


def _sample_copula(real: pd.DataFrame, n_samples: int, rng: np.random.Generator) -> pd.DataFrame:
    """Amostra ``n_samples`` linhas (sem Risk) de uma cópula gaussiana ajustada em ``real``."""
    cols = MODEL_COLUMNS
    scores = np.column_stack(
        [_to_normal_scores(real[c], rng, c in CATEGORICAL_COLS) for c in cols]
    )
    corr = np.corrcoef(scores, rowvar=False)
    corr = (corr + corr.T) / 2 + 1e-6 * np.eye(len(cols))  # estabiliza (positiva definida)
    z = rng.multivariate_normal(np.zeros(len(cols)), corr, size=n_samples)

    synth = pd.DataFrame(
        {c: _from_normal_scores(z[:, i], real[c], c in CATEGORICAL_COLS) for i, c in enumerate(cols)}
    )
    for c in NUMERIC_INT:
        lo, hi = real[c].min(), real[c].max()
        synth[c] = np.clip(np.round(synth[c].astype(float)), lo, hi).astype(int)
    synth["Job"] = synth["Job"].astype(int)
    return synth


def fit_sample_class_conditional(real: pd.DataFrame, n_samples: int, seed: int) -> pd.DataFrame:
    """Gera ``n_samples`` linhas sintéticas, uma cópula por classe de ``Risk``."""
    rng = np.random.default_rng(seed)
    props = real[C.TARGET].value_counts(normalize=True)
    labels = sorted(props.index)
    counts = {lab: int(round(props[lab] * n_samples)) for lab in labels}
    counts[labels[-1]] += n_samples - sum(counts.values())  # ajusta arredondamento

    parts = []
    for lab in labels:
        part = _sample_copula(real[real[C.TARGET] == lab].reset_index(drop=True), counts[lab], rng)
        part[C.TARGET] = lab
        parts.append(part)
    out = pd.concat(parts, ignore_index=True)
    # Embaralha para não deixar blocos ordenados por classe.
    return out.sample(frac=1.0, random_state=seed).reset_index(drop=True)[OUTPUT_COLUMNS]


def load_real_rows() -> pd.DataFrame:
    """Lê as ``N_REAL_ROWS`` primeiras linhas (reais) do CSV bruto e normaliza contas ausentes."""
    if not C.RAW_CSV.exists():
        raise FileNotFoundError(
            f"{C.RAW_CSV} não encontrado. Rode: uv run python -m src.credit.data.make_dataset"
        )
    df = pd.read_csv(C.RAW_CSV, nrows=C.N_REAL_ROWS)
    for col in ["Saving accounts", "Checking account"]:
        df[col] = df[col].fillna(C.NO_ACCOUNT_FILL)
    return df[OUTPUT_COLUMNS]


def augment_dataset(random_state: int = C.RANDOM_STATE) -> pd.DataFrame:
    real = load_real_rows()
    if len(real) < C.N_REAL_ROWS:
        raise ValueError(f"Esperadas {C.N_REAL_ROWS} linhas reais, encontradas {len(real)}.")
    real = validate_credit_data(real, lazy=True)

    # Mesma partição real usada no pipeline (preprocess) -> sem vazamento ref/prod.
    ref_real, prod_real = train_test_split(
        real, test_size=0.3, random_state=random_state, stratify=real[C.TARGET]
    )
    ref_synth = fit_sample_class_conditional(ref_real, C.N_SYNTH_REFERENCE, random_state)
    prod_synth = fit_sample_class_conditional(prod_real, C.N_SYNTH_PRODUCTION, random_state + 1)
    synth = pd.concat([ref_synth, prod_synth], ignore_index=True)

    # Os sintéticos também passam pela barreira de ingestão (contrato Pandera).
    validate_credit_data(synth, lazy=True)

    # Contas sem conta voltam ao formato original do CSV (NaN -> "NA").
    full = pd.concat([real, synth], ignore_index=True)
    for col in ["Saving accounts", "Checking account"]:
        full[col] = full[col].replace(C.NO_ACCOUNT_FILL, np.nan)
    full[OUTPUT_COLUMNS].to_csv(C.RAW_CSV, index=False, na_rep="NA")

    # Mantém também data/raw/german_credit_data.csv sincronizado com 5.000 linhas
    # e exatamente o mesmo cabeçalho original (,Age,Sex,...,Purpose).
    raw_no_target = C.DATA_DIR / "raw" / "german_credit_data.csv"
    full[MODEL_COLUMNS].to_csv(raw_no_target, index=True, na_rep="NA")

    print(f"[augment] Reais: {len(real)} | Sintéticas: {len(synth)} | Total: {len(full)} -> {C.RAW_CSV}")
    for name, a, b in [("ref", ref_real, ref_synth), ("prod", prod_real, prod_synth)]:
        print(
            f"[augment] % 'bad' {name}: real={(a[C.TARGET] == 'bad').mean():.3f} "
            f"sintético={(b[C.TARGET] == 'bad').mean():.3f}"
        )
    return full


if __name__ == "__main__":
    augment_dataset()
