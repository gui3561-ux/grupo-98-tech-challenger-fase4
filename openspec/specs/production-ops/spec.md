# production-ops Specification

## Purpose

Permite executar a API de previsão em contêiner e observar saúde, prontidão, latência e uso de recursos em operação.

## Requirements

### Requirement: Empacotamento em contêiner
O sistema SHALL fornecer uma imagem de contêiner que sobe a API de previsão com o modelo e a escala já incluídos ou montados, sem exigir retreino no arranque.

#### Scenario: API sobe via contêiner
- **WHEN** a imagem é executada com a configuração documentada
- **THEN** a API de previsão fica acessível em HTTP sem passos manuais de treino

### Requirement: Verificação de saúde
A API SHALL expor um endpoint de saúde que responde com sucesso quando o processo HTTP está no ar, independentemente do modelo.

#### Scenario: Processo no ar
- **WHEN** o servidor HTTP está escutando
- **THEN** o endpoint de saúde responde com sucesso

### Requirement: Verificação de prontidão do modelo
A API SHALL expor um endpoint de prontidão que só responde com sucesso quando o modelo e a escala estão carregados e aptos para inferência.

#### Scenario: Modelo carregado
- **WHEN** modelo e escala foram carregados com sucesso
- **THEN** o endpoint de prontidão responde com sucesso

#### Scenario: Modelo ausente
- **WHEN** o modelo ou a escala não puderam ser carregados
- **THEN** o endpoint de prontidão responde com falha e o endpoint de previsão não deve ser considerado pronto

### Requirement: Métricas de latência e recursos
A API SHALL expor métricas observáveis de contagem de requisições, latência das previsões e utilização de CPU e memória do processo.

#### Scenario: Métricas após uma previsão
- **WHEN** pelo menos uma previsão bem-sucedida foi servida
- **THEN** as métricas incluem aumento na contagem de requisições e um registro de latência dessa previsão

#### Scenario: Uso de recursos visível
- **WHEN** a API está em execução
- **THEN** as métricas incluem indicadores atuais de CPU e memória do processo

### Requirement: Porta HTTP da plataforma de nuvem
Quando a imagem sobe em um provedor que define a variável de ambiente `PORT`, o processo HTTP SHALL escutar essa porta. Na ausência da variável, SHALL escutar 8000.

#### Scenario: Render define PORT
- **WHEN** o contêiner inicia com `PORT` definido
- **THEN** a API fica acessível nessa porta, sem exigir rebuild só para mudar o número

#### Scenario: Execução local sem PORT
- **WHEN** o contêiner inicia sem `PORT`
- **THEN** a API permanece na porta 8000, como no `compose.yaml`

### Requirement: Caminho de deploy no Render
O README SHALL descrever o serviço Docker já publicado no Render Hobby, com health check em `/health` e a URL pública `https://grupo-98-tech-challenger-fase4.onrender.com`, de modo que um avaliador alcance a API sem adivinhar o hostname.

#### Scenario: Integrante publica no Render
- **WHEN** um integrante segue a seção Render do README com este repositório e a imagem Docker
- **THEN** encontra os passos de Web Service Docker, health `/health` e a URL pública já registrada no README

#### Scenario: Avaliador encontra a API na nuvem
- **WHEN** um avaliador segue a seção Render do README
- **THEN** encontra a URL pública, o Swagger em `/docs`, o health em `/health` e a indicação de que a imagem Docker é a mesma do repositório

### Requirement: Permanecer no compute Hobby
Ajustes no Render (painel, Blueprint ou CLI) MUST NOT promover o serviço para Standard, Pro ou planos com 2 GB de RAM ou mais (`1c-2g` e acima). O compute SHALL permanecer no recorte Hobby já em uso (`free` ou `starter` / `0.5c-512mb`).

#### Scenario: Blueprint ou CLI não sobe o plano
- **WHEN** o `render.yaml` é sincronizado ou o serviço é atualizado via CLI
- **THEN** o plano de compute não passa a `standard`, `pro` nem `1c-2g` ou maior

### Requirement: Spin-down do Hobby visível
O README SHALL avisar que o serviço Hobby pode dormir após ociosidade, que um `GET /health` acorda a instância antes da demo, e que o fallback da apresentação é `docker compose` local em `/docs`.

#### Scenario: Demo após idle
- **WHEN** um integrante prepara a demonstração da API em nuvem
- **THEN** o README indica acordar o serviço com `/health` e, se a instância gratuita estiver suspensa, usar a API local com Docker
