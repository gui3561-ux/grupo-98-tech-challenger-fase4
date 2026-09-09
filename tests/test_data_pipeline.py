from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pytest

from src.data.collect import DataSourceError, collect_prices, normalize_ohlc
from src.data.preprocess import chronological_split, clean_series, fit_scaler, transform_close
from src.data.windows import InsufficientSeriesError, make_windows


def _ohlc_frame(closes: list[float], start: str = "2018-01-02") -> pd.DataFrame:
    dates = pd.bdate_range(start=start, periods=len(closes))
    return pd.DataFrame({"Close": closes}, index=dates)


def test_collect_prices_sorted_with_close(tmp_path):
    raw = _ohlc_frame([10.0, 11.0, 9.5])
    cache = tmp_path / "raw.parquet"
    series = collect_prices(downloader=lambda *_: raw, cache_path=cache, use_cache=False)
    assert list(series.columns) == ["date", "close"]
    assert series["date"].is_monotonic_increasing
    assert series["close"].tolist() == [10.0, 11.0, 9.5]
    assert cache.exists()


def test_collect_failure_does_not_build_windows(tmp_path):
    cache = tmp_path / "raw.parquet"

    def boom(*_args, **_kwargs):
        raise DataSourceError("fonte indisponível")

    with pytest.raises(DataSourceError):
        collect_prices(downloader=boom, cache_path=cache, use_cache=False)

    assert not cache.exists()


def test_normalize_empty_raises():
    with pytest.raises(DataSourceError):
        normalize_ohlc(pd.DataFrame())


def test_clean_drops_invalid_close():
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(["2018-01-03", "2018-01-02", "2018-01-04"]),
            "close": [10.0, np.nan, 12.0],
        }
    )
    cleaned = clean_series(frame)
    assert cleaned["close"].tolist() == [10.0, 12.0]
    assert cleaned["date"].is_monotonic_increasing


def test_chronological_split_order():
    dates = [datetime(2018, 1, 1) + timedelta(days=i) for i in range(100)]
    frame = pd.DataFrame({"date": dates, "close": np.linspace(10, 20, 100)})
    train, val, test = chronological_split(frame)
    assert train["date"].max() < val["date"].min()
    assert val["date"].max() < test["date"].min()
    assert len(train) == 70
    assert len(val) == 15
    assert len(test) == 15


def test_scaler_fits_only_on_train():
    train = pd.DataFrame({"close": [0.0, 10.0]})
    val = pd.DataFrame({"close": [100.0]})
    scaler = fit_scaler(train)
    scaled_val = transform_close(val, scaler)
    # min/max do treino são 0 e 10; 100 vira 10 na escala do treino
    assert scaled_val["close_scaled"].iloc[0] == pytest.approx(10.0)
    assert scaler.data_min_[0] == pytest.approx(0.0)
    assert scaler.data_max_[0] == pytest.approx(10.0)


def test_windows_shape_and_target():
    values = np.arange(65, dtype=float)
    frame = pd.DataFrame({"close_scaled": values})
    x, y, insufficient = make_windows(frame, window_size=60)
    assert insufficient is False
    assert x.shape == (5, 60, 1)
    assert y.shape == (5,)
    assert x[0, :, 0].tolist() == list(values[:60])
    assert y[0] == pytest.approx(values[60])


def test_windows_short_series_raises_and_empty():
    frame = pd.DataFrame({"close_scaled": np.arange(60, dtype=float)})
    with pytest.raises(InsufficientSeriesError):
        make_windows(frame, window_size=60, report_insufficient=True)
    x, y, insufficient = make_windows(frame, window_size=60, report_insufficient=False)
    assert insufficient is True
    assert x.shape == (0, 60, 1)
    assert y.shape == (0,)
