## ADDED Requirements

### Requirement: Identidade e recorte da entrega
O README SHALL identificar o grupo da entrega, a ação escolhida e o horizonte da previsão, deixando explícito que o ticker do enunciado é apenas exemplo.

#### Scenario: Avaliador reconhece o recorte
- **WHEN** um avaliador abre o README
- **THEN** encontra o grupo da entrega, PETR4.SA como ação escolhida, horizonte de um pregão à frente, e a indicação de que DIS no enunciado é exemplo, não obrigação

### Requirement: Fluxo após clone
O README SHALL descrever o que o clone contém e o que não contém, de modo que treino, notebooks e API local não dependam de um cache de dados que não está no Git.

#### Scenario: Clone sem cache de mercado
- **WHEN** um leitor clona o repositório sem o arquivo de cache histórico
- **THEN** o README deixa claro que os artefatos do modelo já estão no repositório para servir a API, e que treino ou notebooks baixam a série histórica se o cache não existir

### Requirement: Chamada reproduzível de previsão
O README SHALL incluir um exemplo de chamada à API de previsão que um leitor consegue copiar e executar, com janela de tamanho correto e resposta de exemplo coerente com o modelo persistido.

#### Scenario: Copiar e prever
- **WHEN** a API local está no ar e o leitor segue o exemplo de previsão do README
- **THEN** o comando usa JSON válido com exatamente 60 fechamentos e a resposta de exemplo contém ticker PETR4.SA, horizonte D+1 e um fechamento previsto numérico alinhado ao artefato atual

### Requirement: Entregáveis da fase visíveis
O README SHALL declarar o estado dos entregáveis do enunciado: documentação, contêiner, vídeo e API em nuvem, sem apresentar uma URL pública que não exista.

#### Scenario: Nuvem e vídeo sem ambiguidade
- **WHEN** um avaliador procura o link da API em produção e o vídeo
- **THEN** o README diz que ainda não há URL pública, que a demo oficial é local via contêiner e documentação interativa, e que o vídeo deve mostrar a API em funcionamento

### Requirement: Monitoramento demonstrável no README
O README SHALL mostrar como observar latência e uso de recursos após uma previsão, usando o endpoint de métricas já existente.

#### Scenario: Métricas depois do predict
- **WHEN** o leitor segue a seção de monitoramento do README após uma previsão bem-sucedida
- **THEN** consegue chamar o endpoint de métricas e reconhecer contagem, latência, CPU e memória
