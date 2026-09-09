# lstm-forecast Specification

## Purpose

Treina, avalia e persiste um modelo LSTM univariado que prevê o fechamento de PETR4.SA no próximo pregão a partir de 60 fechamentos anteriores.

## Requirements

### Requirement: Modelo LSTM univariado para fechamento D+1
O sistema SHALL treinar um modelo de redes neurais LSTM que recebe 60 fechamentos normalizados e produz uma previsão do fechamento do pregão seguinte.

#### Scenario: Treino conclui com artefato utilizável
- **WHEN** as janelas de treino e validação estão disponíveis
- **THEN** o sistema produz um modelo treinado capaz de emitir uma previsão numérica de D+1 para uma janela válida

### Requirement: Avaliação com MAE, RMSE e MAPE
O sistema SHALL avaliar as previsões no conjunto de teste nas unidades originais de preço usando MAE, RMSE e MAPE, e registrar esses valores de forma reproduzível.

#### Scenario: Métricas no teste após inversão de escala
- **WHEN** o modelo gera previsões para o conjunto de teste
- **THEN** as previsões são convertidas de volta para preço e o sistema reporta MAE, RMSE e MAPE nesse espaço

### Requirement: Comparação com baseline naive
O sistema SHALL comparar as métricas do LSTM com a baseline naive em que a previsão de D+1 é o último fechamento da janela.

#### Scenario: Baseline naive reportada junto do LSTM
- **WHEN** a avaliação de teste é executada
- **THEN** o sistema reporta MAE, RMSE e MAPE do LSTM e da baseline naive sobre o mesmo conjunto de teste

### Requirement: Persistência do modelo e da escala
Após o treino, o sistema SHALL salvar o modelo e os parâmetros de escala em artefatos que permitam reproduzir a mesma transformação e a mesma inferência sem retreinar.

#### Scenario: Artefatos carregáveis para inferência
- **WHEN** o treino termina com sucesso
- **THEN** existem artefatos persistidos de modelo e escala que, recarregados, reproduzem a previsão para a mesma janela de entrada

### Requirement: Hiperparâmetros escolhidos observáveis
A entrega SHALL tornar observáveis os hiperparâmetros do LSTM persistido (tamanho das camadas, dropout e early stopping na validação), sem exigir uma busca automática na hora da inferência.

#### Scenario: Banca vê o recorte de treino
- **WHEN** um avaliador consulta o notebook de avaliação ou o README
- **THEN** encontra os valores usados no artefato em `models/` e pelo menos duas alternativas que foram consideradas, com o critério de escolha ligado à perda de validação / early stopping
