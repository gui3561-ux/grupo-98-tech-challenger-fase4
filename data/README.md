# Dataset — German Credit Data (Fase 4)

## Origem
- **Nome:** Statlog (German Credit Data)
- **Fonte primária:** UCI Machine Learning Repository — dataset id **144**
  (https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data)
- **Versão utilizada:** CSV pré-processado (colunas renomeadas / subconjunto) publicado
  no Kaggle — *German Credit Risk* — arquivo `raw/german_credit_data.csv`.
- **Licença:** uso acadêmico/pesquisa (UCI).
- **Volume:** 1.000 amostras. É um dos datasets **explicitamente listados como aceitos**
  no enunciado (MELT.pdf), apesar de a sugestão genérica citar ≥ 5.000 amostras.

## Problema
Classificação **binária** de risco de crédito: prever se um cliente é **bom** (`good`)
ou **mau** (`bad`) pagador.

## ⚠️ Target ausente no CSV do Kaggle
A versão baixada (`raw/german_credit_data.csv`) contém apenas as 9 features, **sem a
coluna `Risk`**. O target original (1=good, 2=bad) é recuperado do UCI, que mantém a
**mesma ordem de linhas**, e anexado por índice pelo script:

```bash
python -m src.credit.data.make_dataset
```

Isso gera `raw/german_credit_with_risk.csv` (features + coluna `Risk`), que é o
dataset base efetivo do projeto.

## Dicionário de dados

| Coluna | Tipo | Descrição | Sensibilidade (LGPD) |
|---|---|---|---|
| `Age` | int | Idade do cliente (anos) | PII / dado pessoal |
| `Sex` | cat | Sexo (`male`/`female`) | PII / dado sensível (risco de viés) |
| `Job` | int (0–3) | Nível de qualificação/emprego | — |
| `Housing` | cat | Moradia (`own`/`rent`/`free`) | dado pessoal |
| `Saving accounts` | cat | Saldo em poupança (`little`…`rich`, `NA`) | financeiro |
| `Checking account` | cat | Saldo em conta corrente (`little`/`moderate`/`rich`, `NA`) | financeiro |
| `Credit amount` | int | Valor do crédito solicitado (DM) | financeiro |
| `Duration` | int | Prazo do crédito (meses) | — |
| `Purpose` | cat | Finalidade do crédito | — |
| `Risk` | cat | **Target**: `good` / `bad` (anexado via UCI) | rótulo de decisão |

> Valores `NA` em `Saving accounts` e `Checking account` são categoria legítima
> ("sem conta"), não ausência de dado — tratar na Etapa 1 do contrato de dados.

## Estratégia de separação: Referência × Produção
Requisito obrigatório do desafio (separação clara entre treino e o cenário onde o
drift ocorre).

- **Dataset de Referência** (`data/reference/`): recorte "limpo" usado para treinar o
  modelo baseline e servir de baseline estatístico para o Evidently.
- **Dataset de Produção** (`data/production/`): cópia com **degradação injetada**
  (Data/Concept Drift) em ≥ 2 variáveis importantes — construído na **Etapa 2**.

Split proposto (a materializar na Etapa 1):
1. Ler `raw/german_credit_with_risk.csv`.
2. `train_test_split` estratificado por `Risk` (ex.: 70% referência / 30% produção-base).
3. Salvar referência em `data/reference/reference.csv`.
4. A partição de produção-base será a semente para a injeção de drift na Etapa 2.

## Arquivos
- `raw/german_credit_data.csv` — original do Kaggle (sem target).
- `raw/german_credit_with_risk.csv` — gerado por `make_dataset.py` (com target). *(não versionar até validar)*
- `raw/archive.zip` — zip original do Kaggle.
- `reference/`, `production/` — populados nas Etapas 1 e 2.
