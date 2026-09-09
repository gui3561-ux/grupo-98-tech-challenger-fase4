## ADDED Requirements

### Requirement: Porta HTTP da plataforma de nuvem
Quando a imagem sobe em um provedor que define a variável de ambiente `PORT`, o processo HTTP SHALL escutar essa porta. Na ausência da variável, SHALL escutar 8000.

#### Scenario: Render define PORT
- **WHEN** o contêiner inicia com `PORT` definido
- **THEN** a API fica acessível nessa porta, sem exigir rebuild só para mudar o número

#### Scenario: Execução local sem PORT
- **WHEN** o contêiner inicia sem `PORT`
- **THEN** a API permanece na porta 8000, como no `compose.yaml`

### Requirement: Caminho de deploy no Render
O README SHALL descrever o deploy da imagem Docker no Render (serviço web, health check em `/health`) de modo que um integrante consiga publicar o serviço e, depois, registrar a URL no README.

#### Scenario: Integrante publica no Render
- **WHEN** um integrante segue a seção Render do README com este repositório e a imagem Docker
- **THEN** encontra os passos de Web Service Docker, health `/health` e a instrução de colar a URL pública no README após o primeiro deploy bem-sucedido
