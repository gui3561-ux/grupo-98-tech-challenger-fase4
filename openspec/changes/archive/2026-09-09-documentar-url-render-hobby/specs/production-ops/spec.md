## MODIFIED Requirements

### Requirement: Caminho de deploy no Render
O README SHALL descrever o serviço Docker já publicado no Render Hobby, com health check em `/health` e a URL pública `https://grupo-98-tech-challenger-fase4.onrender.com`, de modo que um avaliador alcance a API sem adivinhar o hostname.

#### Scenario: Integrante publica no Render
- **WHEN** um integrante segue a seção Render do README com este repositório e a imagem Docker
- **THEN** encontra os passos de Web Service Docker, health `/health` e a URL pública já registrada no README

#### Scenario: Avaliador encontra a API na nuvem
- **WHEN** um avaliador segue a seção Render do README
- **THEN** encontra a URL pública, o Swagger em `/docs`, o health em `/health` e a indicação de que a imagem Docker é a mesma do repositório

## ADDED Requirements

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
