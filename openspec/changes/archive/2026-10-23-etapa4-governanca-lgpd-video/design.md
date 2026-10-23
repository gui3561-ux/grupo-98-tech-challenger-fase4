## Context

Ver `proposal.md` para motivação.
A Etapa 4 do edital exige a formalização teórica e prática da governança em produção: compliance com LGPD, mitigação de vieses, análise causal da degradação silenciosa e preparação do roteiro do vídeo de apresentação em formato STAR (≤ 5 min).

## Goals / Non-Goals

**Goals:**
- Reorganizar o `README.md` estabelecendo a Fase 4 como documento de entrada do repositório.
- Redigir a seção de conformidade jurídica com a LGPD (Bases legais, tratamento de PII, direitos do titular e política de descarte).
- Documentar a análise causal fundamentada nas variações estatísticas observadas nos relatórios da Etapa 2 (PSI e ROC-AUC).
- Fornecer roteiro completo e minutado para gravação do vídeo pelo método STAR.

**Non-Goals:**
- Gravar o vídeo físico (responsabilidade dos alunos integrantes do Grupo 98).
- Apagar documentação ou código da Fase 3 (será mantido preservado em seção de legado ao final).

## Decisions

### 1. Hierarquia do README.md
- **Decisão:** Posicionar o Tech Challenge Fase 4 no topo do `README.md`, contendo introdução, arquitetura das 4 etapas, guia rápido de execução, Governança/LGPD, Análise Causal e Roteiro STAR. O conteúdo da Fase 3 (PETR4) será encapsulado ao final na seção `# Apêndice: Fase 3 (Legado)`.
- **Justificativa:** Garante que os avaliadores encontrem imediatamente todos os entregáveis pontuados no edital da Fase 4.

### 2. Fundamentação da LGPD
- **Decisão:** Mapear a base legal primária no Artigo 7º, X da Lei nº 13.709/2018 ("proteção do crédito"), complementada pelas diretrizes de transparência e direito à explicação de decisões automatizadas (Artigo 20).
- **Justificativa:** Concessão de crédito possui fundamentação jurídica explícita na LGPD, mitigando riscos regulatórios quando associada a auditorias periódicas de fairness em `Sex` e `Age`.

### 3. Roteiro STAR em 4 blocos (5 minutos)
- **Decisão:** Estruturar o roteiro em:
  - **S (Situation)**: 0:00 - 1:00 (Contexto fintech, inflação e risco de degradação silenciosa).
  - **T (Task)**: 1:00 - 2:00 (Requisitos de sustentação: contratos rígidos, observabilidade e governança).
  - **A (Action)**: 2:00 - 3:30 (Demonstração prática: `run_etapa1.py` bloqueando lote inválido, `run_etapa2.py` gerando Evidently HTML e tracking no MLflow).
  - **R (Result)**: 3:30 - 5:00 (Análise dos relatórios de drift, impacto na acurácia, lições aprendidas e conformidade).

## Risks / Trade-offs

- **[Tamanho do README]** → A consolidação dos capítulos de governança e causalidade aumenta a extensão do arquivo. Utilizaremos tabelas, alertas GitHub e formatação modular para preservar a legibilidade e facilidade de navegação.

