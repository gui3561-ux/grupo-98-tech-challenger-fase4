"""Orquestrador da Etapa 2 (inclui o baseline mínimo da Etapa 1).

Executa, em ordem:
1. Split Referência × Produção-base.
2. Treino do modelo baseline de crédito.
3. Simulação de drift no dataset de produção.
4. Detecção de drift + relatórios (Evidently + PSI/KS).

Uso:
    python -m src.credit.run_etapa2
"""

from __future__ import annotations

from src.credit.data.preprocess import make_reference_production_split
from src.credit.data.simulate_drift import simulate_production_drift
from src.credit.drift.report import build_drift_report
from src.credit.model.baseline import train_baseline


def main() -> None:
    print("== [1/4] Split Referência × Produção ==")
    make_reference_production_split()
    print("\n== [2/4] Treino do baseline (Etapa 1 mínima) ==")
    train_baseline()
    print("\n== [3/4] Simulação de drift ==")
    simulate_production_drift()
    print("\n== [4/4] Detecção e relatório de drift ==")
    build_drift_report()
    print("\n== Etapa 2 concluída ==")


if __name__ == "__main__":
    main()
