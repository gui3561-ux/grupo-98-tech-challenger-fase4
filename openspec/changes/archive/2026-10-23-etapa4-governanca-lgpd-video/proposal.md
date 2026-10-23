## Why

A Etapa 4 do Tech Challenge, somada aos critérios do Vídeo STAR, compõe 30% da nota final (15% Governança e LGPD + 15% Vídeo). O edital exige expressamente a inclusão no `README.md` de um plano consolidado de proteção de dados (PII, bases legais da LGPD para crédito e retenção), uma análise causal profunda sobre o motivo da degradação do modelo, e o roteiro do vídeo demonstrativo de 5 minutos seguindo a metodologia STAR. Atualmente, o README.md ainda reflete a Fase 3 e carece dessa documentação formal exigida para a banca.

## What Changes

- Reestruturação completa do `README.md` colocando a Fase 4 (Credit Scoring MLOps) como o tema principal do repositório, com instruções claras de execução de cada etapa e preservação da Fase 3 em seção demarcada de legado.
- Redação da seção formal de **Governança de Dados e Conformidade com a LGPD**:
  - Bases legais aplicadas: Proteção ao Crédito (Art. 7º, X) e Legítimo Interesse (Art. 7º, IX).
  - Mapeamento e mitigação de viés em dados sensíveis e PII (`Sex` e `Age`).
  - Plano de ciclo de vida, segurança e retenção de dados transacionais.
- Elaboração da **Análise Causal da Degradação Silenciosa**:
  - Explicação técnica e econômica detalhada do mecanismo que causou o Data Drift (inflação em `Credit amount`, clientes mais jovens em `Age`, liquidez reduzida em `Checking account`) e a deterioração do ROC-AUC (Concept Drift).
- Estruturação do **Roteiro Oficial do Vídeo (Método STAR - ≤ 5 min)**:
  - Divisão minuto a minuto por integrante nos pilares Situation, Task, Action e Result, orientando a demonstração prática do pipeline, barreira de dados e relatórios.

## Capabilities

### New Capabilities
- `credit-governance-compliance`: Governança de dados, conformidade regulatória (LGPD), mitigação de viés algorítmico e análise causal da degradação.

### Modified Capabilities
- `academic-notebooks`: Requisitos de documentação do README para evidenciar a entrega da Fase 4, link de vídeo e conformidade acadêmica.

## Impact

- README.md consolidado atendendo a 30% da pontuação do Tech Challenge.
- Roteiro pronto para gravação imediata do vídeo pelos alunos do Grupo 98.
- Sem impactos destrutivos em código de produção ou testes existentes.

