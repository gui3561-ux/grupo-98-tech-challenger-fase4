## Purpose

Expõe uma API REST para que o usuário envie 60 fechamentos históricos e receba a previsão de fechamento do próximo pregão, sem depender da bolsa no momento da inferência.

## ADDED Requirements

### Requirement: Previsão D+1 a partir de preços históricos fornecidos
A API SHALL aceitar uma sequência de exatamente 60 preços de fechamento e devolver uma previsão numérica do fechamento do próximo pregão, usando o modelo e a escala persistidos.

#### Scenario: Janela válida retorna previsão
- **WHEN** um cliente envia 60 fechamentos numéricos válidos
- **THEN** a API responde com sucesso e um único valor de previsão de D+1 nas unidades de preço

#### Scenario: Resposta identifica horizonte e ticker
- **WHEN** a previsão é bem-sucedida
- **THEN** a resposta informa que o horizonte é o próximo pregão e que o ticker associado é PETR4.SA

### Requirement: Validação da janela de entrada
A API SHALL rejeitar requisições cuja sequência não tenha exatamente 60 valores numéricos finitos.

#### Scenario: Quantidade diferente de 60
- **WHEN** o cliente envia 59 ou 61 preços
- **THEN** a API rejeita a requisição com erro de validação e não executa inferência

#### Scenario: Valores não numéricos ou não finitos
- **WHEN** a sequência contém nulos, texto ou valores infinitos
- **THEN** a API rejeita a requisição com erro de validação

### Requirement: Inferência independente da fonte histórica ao vivo
A API MUST NOT consultar a fonte de preços de mercado para cumprir o pedido de previsão; a única entrada de preços SHALL ser a sequência enviada pelo cliente.

#### Scenario: Previsão sem acesso à bolsa
- **WHEN** a fonte histórica de mercado está indisponível
- **THEN** uma requisição com 60 fechamentos válidos ainda produz a previsão D+1

### Requirement: Documentação interativa da API
A API SHALL expor documentação OpenAPI que descreva o contrato de previsão, incluindo o formato da janela de entrada e da previsão de saída.

#### Scenario: Cliente descobre o contrato sem código-fonte
- **WHEN** um cliente acessa a documentação OpenAPI da API em execução
- **THEN** consegue identificar o endpoint de previsão, o tamanho da janela e o significado da saída D+1

### Requirement: Erros não expõem detalhes internos
Em falhas de inferência ou validação, a API MUST NOT incluir stack traces ou caminhos internos na resposta ao cliente.

#### Scenario: Falha de inferência
- **WHEN** o modelo não consegue produzir uma previsão por erro interno
- **THEN** o cliente recebe uma mensagem de erro genérica sem detalhes de implementação
