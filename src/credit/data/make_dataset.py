"""Preparação do dataset base (Etapa 0).

O CSV do Kaggle (``data/raw/german_credit_data.csv``) é uma versão pré-processada
do *Statlog German Credit Data* (UCI, id=144) com colunas renomeadas, porém **sem
a coluna de target** (``Risk``). Este script recupera o target original (1=good,
2=bad) do UCI — que está na **mesma ordem de linhas** do CSV do Kaggle — e o anexa
por índice, gerando ``data/raw/german_credit_with_risk.csv``.

Fonte do target:
    - Preferencial: pacote ``ucimlrepo`` (``fetch_ucirepo(id=144)``).
    - Fallback: download direto de ``german.data`` do repositório UCI.

Uso (na máquina com acesso à internet):
    python -m src.credit.data.make_dataset

Requer acesso à rede na primeira execução. O arquivo gerado fica versionado
localmente e não precisa ser baixado novamente.
"""

from __future__ import annotations

import io
import urllib.request
from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")
SOURCE_CSV = RAW_DIR / "german_credit_data.csv"
OUTPUT_CSV = RAW_DIR / "german_credit_with_risk.csv"

UCI_DATA_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/"
    "statlog/german/german.data"
)
# Na german.data o target é a 21ª (última) coluna: 1 = good, 2 = bad.
TARGET_MAP = {1: "good", 2: "bad"}


def _target_via_ucimlrepo() -> pd.Series:
    from ucimlrepo import fetch_ucirepo  # type: ignore

    ds = fetch_ucirepo(id=144)
    y = ds.data.targets.iloc[:, 0].astype(int)
    return y.map(TARGET_MAP).reset_index(drop=True)


def _target_via_download() -> pd.Series:
    with urllib.request.urlopen(UCI_DATA_URL, timeout=30) as resp:  # noqa: S310
        raw = resp.read().decode("utf-8")
    df = pd.read_csv(io.StringIO(raw), sep=r"\s+", header=None)
    y = df.iloc[:, -1].astype(int)
    return y.map(TARGET_MAP).reset_index(drop=True)


def load_target() -> pd.Series:
    """Recupera o target original do UCI, tolerando ausência do ucimlrepo."""
    try:
        return _target_via_ucimlrepo()
    except Exception as exc:  # pragma: no cover - depende de rede/pacote
        print(f"[make_dataset] ucimlrepo indisponível ({exc}); usando download direto.")
        return _target_via_download()


def main() -> None:
    if not SOURCE_CSV.exists():
        raise FileNotFoundError(f"CSV base não encontrado: {SOURCE_CSV}")

    features = pd.read_csv(SOURCE_CSV, index_col=0)
    target = load_target()

    if len(features) != len(target):
        raise ValueError(
            f"Divergência de linhas: features={len(features)} vs target={len(target)}. "
            "A junção por ordem de linha não é segura."
        )

    features = features.reset_index(drop=True)
    features["Risk"] = target.values
    features.to_csv(OUTPUT_CSV, index=False)

    print(f"[make_dataset] Gerado {OUTPUT_CSV} com {len(features)} linhas.")
    print(features["Risk"].value_counts().to_string())


if __name__ == "__main__":
    main()
