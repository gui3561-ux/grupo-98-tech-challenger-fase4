from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pandas as pd

from src.settings import RAW_CACHE, START_DATE, TICKER


class DataSourceError(Exception):
    """A fonte histórica de preços falhou ou devolveu dados inválidos."""


Downloader = Callable[[str, str], pd.DataFrame]


def _default_downloader(ticker: str, start: str) -> pd.DataFrame:
    import yfinance as yf

    try:
        frame = yf.download(
            ticker,
            start=start,
            progress=False,
            auto_adjust=True,
            threads=False,
            multi_level_index=False,
        )
    except TypeError:
        frame = yf.download(
            ticker,
            start=start,
            progress=False,
            auto_adjust=True,
            threads=False,
        )
    except Exception as exc:
        raise DataSourceError(f"falha ao baixar {ticker}: {exc}") from exc

    if frame is None or frame.empty:
        raise DataSourceError(f"fonte histórica não retornou dados para {ticker}")
    return frame


def _flatten_columns(frame: pd.DataFrame) -> pd.DataFrame:
    if isinstance(frame.columns, pd.MultiIndex):
        flattened = frame.copy()
        flattened.columns = [
            str(col[0]) if isinstance(col, tuple) else str(col) for col in flattened.columns
        ]
        return flattened
    return frame


def _close_column(frame: pd.DataFrame) -> str:
    for column in frame.columns:
        if str(column).lower() == "close":
            return str(column)
    raise DataSourceError("coluna Close ausente na resposta da fonte histórica")


def normalize_ohlc(frame: pd.DataFrame) -> pd.DataFrame:
    """Converte o DataFrame do yfinance em série `date` + `close` ordenada."""
    if frame is None or frame.empty:
        raise DataSourceError("fonte histórica retornou série vazia")

    flat = _flatten_columns(frame)
    close_col = _close_column(flat)
    dates = pd.to_datetime(flat.index)
    series = pd.DataFrame(
        {
            "date": dates,
            "close": pd.to_numeric(flat[close_col], errors="coerce"),
        }
    )
    return series.sort_values("date").reset_index(drop=True)


def collect_prices(
    ticker: str = TICKER,
    start: str = START_DATE,
    cache_path: Path | None = None,
    downloader: Downloader | None = None,
    use_cache: bool = True,
) -> pd.DataFrame:
    """Obtém a série diária de fechamento, com cache opcional em parquet."""
    path = cache_path or RAW_CACHE
    if use_cache and path.exists():
        cached = pd.read_parquet(path)
        return cached.sort_values("date").reset_index(drop=True)

    fetch = downloader or _default_downloader
    raw = fetch(ticker, start)
    series = normalize_ohlc(raw)
    path.parent.mkdir(parents=True, exist_ok=True)
    series.to_parquet(path, index=False)
    return series
