# stock-data-pipeline Specification

## Purpose

Prepara a série histórica de fechamento de PETR4.SA em janelas temporais prontas para treino e avaliação do modelo, sem vazamento de informação futura.

## Requirements

### Requirement: Coleta da série histórica de PETR4.SA
O sistema SHALL obter preços diários de PETR4.SA com início em 2018-01-01 até a data de coleta, incluindo o preço de fechamento de cada pregão.

#### Scenario: Série diária disponível para processamento
- **WHEN** o pipeline de dados é executado com o símbolo PETR4.SA e data inicial 2018-01-01
- **THEN** o sistema produz uma série ordenada por data com o fechamento de cada pregão no intervalo solicitado

#### Scenario: Falha na fonte de dados
- **WHEN** a fonte histórica de preços está indisponível ou retorna erro
- **THEN** o sistema interrompe o pipeline e reporta a falha sem gerar janelas parciais silenciosas

### Requirement: Limpeza e ordenação temporal
O sistema SHALL remover registros sem fechamento válido e manter a série estritamente ordenada por data crescente.

#### Scenario: Pregões sem fechamento são descartados
- **WHEN** a série bruta contém dias sem preço de fechamento
- **THEN** esses dias são excluídos antes da criação das janelas

### Requirement: Split cronológico sem embaralhamento
O sistema SHALL separar treino, validação e teste por ordem temporal, de modo que todas as datas de treino precedam as de validação e todas as de validação precedam as de teste. O sistema MUST NOT embaralhar as janelas entre os conjuntos.

#### Scenario: Conjuntos respeitam a linha do tempo
- **WHEN** as janelas são geradas a partir da série limpa
- **THEN** a última data usada no treino é anterior à primeira data da validação, e a última data da validação é anterior à primeira data do teste

### Requirement: Normalização sem vazamento
O sistema SHALL ajustar a escala dos preços usando apenas estatísticas do conjunto de treino e aplicar a mesma transformação à validação e ao teste.

#### Scenario: Validação e teste usam escala do treino
- **WHEN** os preços de validação e teste são normalizados
- **THEN** os parâmetros de escala vêm exclusivamente do treino

### Requirement: Janelas de 60 pregões para prever o próximo fechamento
O sistema SHALL construir, para cada conjunto, janelas de exatamente 60 fechamentos consecutivos como entrada e o fechamento do pregão seguinte como alvo.

#### Scenario: Janela completa gera um alvo D+1
- **WHEN** existem pelo menos 61 pregões consecutivos em um conjunto
- **THEN** cada exemplo contém 60 fechamentos de entrada e um único alvo correspondente ao pregão imediatamente posterior

#### Scenario: Série curta demais
- **WHEN** um conjunto não possui 61 pregões consecutivos
- **THEN** o sistema não gera exemplos para esse conjunto e reporta que a série é insuficiente
