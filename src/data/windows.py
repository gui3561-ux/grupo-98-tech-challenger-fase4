from __future__ import annotations

import numpy as np
import pandas as pd

from src.settings import WINDOW_SIZE


class InsufficientSeriesError(Exception):
    """A série não tem pregões suficientes para montar janelas 60 → 1."""


def make_windows(
    frame: pd.DataFrame,
    window_size: int = WINDOW_SIZE,
    value_col: str = "close_scaled",
    report_insufficient: bool = True,
) -> tuple[np.ndarray, np.ndarray, bool]:
    """Monta janelas de `window_size` fechamentos e o alvo D+1.

    Retorna `(X, y, insufficient)`. Se a série for curta demais, `X` e `y`
    vêm vazios e `insufficient` é True. Quando `report_insufficient` é True
    e a série é curta, também dispara `InsufficientSeriesError`.
    """
    values = frame[value_col].to_numpy(dtype=np.float64)
    if len(values) < window_size + 1:
        if report_insufficient:
            raise InsufficientSeriesError(
                f"série insuficiente: {len(values)} pontos, mínimo {window_size + 1}"
            )
        empty_x = np.empty((0, window_size, 1), dtype=np.float64)
        empty_y = np.empty((0,), dtype=np.float64)
        return empty_x, empty_y, True

    xs: list[np.ndarray] = []
    ys: list[float] = []
    for end in range(window_size, len(values)):
        xs.append(values[end - window_size : end])
        ys.append(float(values[end]))

    x_arr = np.asarray(xs, dtype=np.float64).reshape(-1, window_size, 1)
    y_arr = np.asarray(ys, dtype=np.float64)
    return x_arr, y_arr, False
