from __future__ import annotations

from tensorflow import keras
from tensorflow.keras import layers

from src.settings import WINDOW_SIZE


def build_lstm(
    window_size: int = WINDOW_SIZE,
    first_units: int = 64,
    second_units: int = 32,
    dropout: float = 0.2,
) -> keras.Model:
    model = keras.Sequential(
        [
            keras.Input(shape=(window_size, 1)),
            layers.LSTM(first_units, return_sequences=True),
            layers.Dropout(dropout),
            layers.LSTM(second_units),
            layers.Dropout(dropout),
            layers.Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mse")
    return model
