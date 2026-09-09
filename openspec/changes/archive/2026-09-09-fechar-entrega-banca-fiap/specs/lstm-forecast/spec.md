## ADDED Requirements

### Requirement: Hiperparâmetros escolhidos observáveis
A entrega SHALL tornar observáveis os hiperparâmetros do LSTM persistido (tamanho das camadas, dropout e early stopping na validação), sem exigir uma busca automática na hora da inferência.

#### Scenario: Banca vê o recorte de treino
- **WHEN** um avaliador consulta o notebook de avaliação ou o README
- **THEN** encontra os valores usados no artefato em `models/` e pelo menos duas alternativas que foram consideradas, com o critério de escolha ligado à perda de validação / early stopping
