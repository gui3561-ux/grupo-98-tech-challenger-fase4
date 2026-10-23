"""Contratos de Dados (Data Contracts) com Pandera para Credit Scoring (Etapa 1).

Garante que dados fora dos parâmetros de negócio (menores de idade, limites negativos,
categorias não homologadas ou nulos ilegítimos) sejam interceptados antes da
ingestão no pipeline de modelagem ("lixo não entra no modelo").
"""

from __future__ import annotations

import pandas as pd
import pandera.pandas as pa
from pandera.errors import SchemaError, SchemaErrors

# Categorias válidas homologadas pelo domínio
VALID_SEX = ["female", "male"]
VALID_JOB = [0, 1, 2, 3]
VALID_HOUSING = ["free", "own", "rent"]
VALID_SAVING_ACCOUNTS = ["little", "moderate", "no_account", "quite rich", "rich"]
VALID_CHECKING_ACCOUNT = ["little", "moderate", "no_account", "rich"]
VALID_PURPOSE = [
    "business",
    "car",
    "domestic appliances",
    "education",
    "furniture/equipment",
    "radio/TV",
    "repairs",
    "vacation/others",
]
VALID_RISK = ["bad", "good"]

# Esquema estrito Pandera para validação de crédito
CREDIT_DATA_SCHEMA = pa.DataFrameSchema(
    columns={
        "Age": pa.Column(
            int,
            pa.Check.in_range(18, 120),
            nullable=False,
            description="Idade do proponente em anos (mínimo legal 18)",
        ),
        "Credit amount": pa.Column(
            int,
            pa.Check.greater_than(0),
            nullable=False,
            description="Valor solicitado em crédito (deve ser positivo)",
        ),
        "Duration": pa.Column(
            int,
            pa.Check.greater_than(0),
            nullable=False,
            description="Prazo de pagamento em meses (deve ser positivo)",
        ),
        "Sex": pa.Column(
            str,
            pa.Check.isin(VALID_SEX),
            nullable=False,
            description="Sexo do cliente",
        ),
        "Job": pa.Column(
            int,
            pa.Check.isin(VALID_JOB),
            nullable=False,
            description="Nível de qualificação profissional (0 a 3)",
        ),
        "Housing": pa.Column(
            str,
            pa.Check.isin(VALID_HOUSING),
            nullable=False,
            description="Tipo de moradia (free, own, rent)",
        ),
        "Saving accounts": pa.Column(
            str,
            pa.Check.isin(VALID_SAVING_ACCOUNTS),
            nullable=False,
            description="Faixa de saldo em poupança ou 'no_account'",
        ),
        "Checking account": pa.Column(
            str,
            pa.Check.isin(VALID_CHECKING_ACCOUNT),
            nullable=False,
            description="Faixa de saldo em conta corrente ou 'no_account'",
        ),
        "Purpose": pa.Column(
            str,
            pa.Check.isin(VALID_PURPOSE),
            nullable=False,
            description="Finalidade do empréstimo",
        ),
        "Risk": pa.Column(
            str,
            pa.Check.isin(VALID_RISK),
            nullable=False,
            required=False,
            description="Rótulo de risco do cliente (good ou bad)",
        ),
    },
    coerce=True,
    strict=False,
)


class DataContractViolationError(Exception):
    """Exceção levantada quando um conjunto de dados viola o contrato de dados Pandera."""

    def __init__(self, message: str, failure_cases: pd.DataFrame | None = None) -> None:
        super().__init__(message)
        self.failure_cases = failure_cases


def validate_credit_data(
    df: pd.DataFrame,
    lazy: bool = True,
    schema: pa.DataFrameSchema = CREDIT_DATA_SCHEMA,
) -> pd.DataFrame:
    """Valida um dataframe de dados de crédito contra o contrato formal Pandera.

    Args:
        df: DataFrame contendo as features (e opcionalmente o target Risk).
        lazy: Se True, acumula todas as falhas antes de falhar.
        schema: Esquema Pandera a ser aplicado.

    Returns:
        DataFrame validado e com tipos devidamente conformados.

    Raises:
        DataContractViolationError: Se uma ou mais regras forem violadas.
    """
    try:
        return schema.validate(df, lazy=lazy)
    except SchemaErrors as err:
        failure_df = err.failure_cases
        summary_lines = []
        for _, row in failure_df.iterrows():
            col = row.get("column", "DataFrame")
            check = row.get("check", "unspecified")
            val = row.get("failure_case", "unknown")
            idx = row.get("index", "?")
            summary_lines.append(f"  - Coluna '{col}' (índice {idx}): valor '{val}' violou checagem '{check}'")
        summary_text = "\n".join(summary_lines[:15])
        if len(summary_lines) > 15:
            summary_text += f"\n  ... e mais {len(summary_lines) - 15} violações adicionais."
        msg = (
            f"Barreira de Ingestão: {len(failure_df)} violação(ões) do contrato de dados detectada(s):\n"
            f"{summary_text}"
        )
        raise DataContractViolationError(msg, failure_cases=failure_df) from err
    except SchemaError as err:
        msg = f"Barreira de Ingestão: violação única do contrato detectada na coluna '{err.schema.name}': {err}"
        raise DataContractViolationError(msg) from err


def build_corrupted_batch() -> pd.DataFrame:
    """Gera um lote de teste com anomalias intencionais para validar a barreira de ingestão.

    Violações incluídas propositalmente:
    1. Idade de menor (15 anos) -> viola Age >= 18.
    2. Valor de crédito negativo (-1000) -> viola Credit amount > 0.
    3. Prazo zero meses (0) -> viola Duration > 0.
    4. Categoria desconhecida de Purpose ('crypto_trading') -> viola categorias homologadas.
    5. Categoria inexistente de Sex ('unknown') -> viola categorias de sexo.
    6. Valor nulo em coluna obrigatória Housing (None) -> viola nullable=False.
    """
    return pd.DataFrame(
        {
            "Age": [15, 35, 42, 28, 50],
            "Credit amount": [1500, -1000, 3000, 2500, 4000],
            "Duration": [12, 24, 0, 18, 36],
            "Sex": ["female", "male", "unknown", "female", "male"],
            "Job": [2, 1, 3, 2, 2],
            "Housing": ["own", "rent", "own", None, "free"],
            "Saving accounts": ["little", "moderate", "no_account", "rich", "little"],
            "Checking account": ["little", "no_account", "moderate", "rich", "no_account"],
            "Purpose": ["radio/TV", "car", "crypto_trading", "education", "business"],
            "Risk": ["good", "bad", "good", "bad", "good"],
        }
    )

