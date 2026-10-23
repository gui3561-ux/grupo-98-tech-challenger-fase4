"""Orquestrador demonstrativo da Etapa 1 (Validação de Dados e Contratos).

Executa:
1. Validação estrita do dataset de referência com o contrato Pandera.
2. Demonstração prática do Ingestion Gate: submissão de lote corrompido e bloqueio com logs.
3. Execução do split estratificado Referência × Produção.
4. Treinamento e avaliação do modelo baseline (XGBoost).

Uso:
    uv run python -m src.credit.run_etapa1
"""

from __future__ import annotations

import pandas as pd

from src.credit import config as C
from src.credit.data.contracts import (
    DataContractViolationError,
    build_corrupted_batch,
    validate_credit_data,
)
from src.credit.data.preprocess import load_base_dataset, make_reference_production_split
from src.credit.model.baseline import train_baseline


def main() -> None:
    print("=================================================================")
    print("   ETAPA 1: VALIDAÇÃO DE DADOS, DATA CONTRACTS E BASELINE       ")
    print("=================================================================")

    # 1. Carregamento e validação do dataset base
    print("\n[1/4] Carregando e validando dataset base com Pandera...")
    try:
        base_df = load_base_dataset(validate=True)
        print(f"✓ Sucesso: Dataset de entrada com {len(base_df)} registros atende a 100% das regras do contrato.")
    except Exception as exc:
        print(f"✗ Erro inesperado ao validar base limpa: {exc}")
        raise

    # 2. Demonstração de interceptação de lote anômalo (Ingestion Gate)
    print("\n[2/4] DEMONSTRAÇÃO DO INGESTION GATE: Submetendo lote com anomalias propositais...")
    corrupted_batch = build_corrupted_batch()
    print(f"-> Lote de teste gerado com {len(corrupted_batch)} amostras contendo violações deliberadas:")
    print("   (menores de 18 anos, limites negativos, prazos zerados, categorias não homologadas e nulos)")

    try:
        validate_credit_data(corrupted_batch)
        print("✗ FALHA DE SEGURANÇA: O lote corrompido passou sem ser interceptado!")
    except DataContractViolationError as exc:
        print("\n>>> SUCESSO: Contrato Pandera interceptou os dados inválidos e bloqueou a ingestão! <<<")
        print(f"{exc}\n")
        print("✓ Garantia de sustentação: Nenhum dado corrompido foi inserido no modelo.")

    # 3. Particionamento Referência × Produção
    print("\n[3/4] Particionamento estratificado Referência (70%) × Produção-base (30%)...")
    make_reference_production_split()

    # 4. Treinamento e avaliação do modelo baseline
    print("\n[4/4] Treinamento do modelo baseline XGBoost...")
    metrics = train_baseline()
    print("\n=================================================================")
    print("   ETAPA 1 CONCLUÍDA COM SUCESSO!                                ")
    print(f"   ROC-AUC (Holdout): {metrics['roc_auc']} | Acc: {metrics['accuracy']} | F1(bad): {metrics['f1_bad']}")
    print("=================================================================")


if __name__ == "__main__":
    main()

