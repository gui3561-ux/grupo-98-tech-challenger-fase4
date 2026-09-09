## Context

See `proposal.md` (Why). O README já existe e descreve treino, notebooks, API, Docker e métricas LSTM vs naive. O gap é reprodução pós-clone e alinhamento com os entregáveis do PDF. A API, o modelo e o `/metrics` não mudam.

## Goals / Non-Goals

**Goals:**

- README como roteiro único da banca: clonar → subir → prever → ver métricas.
- Payload de `/predict` copiável sem edição.

**Non-Goals:**

- Deploy real em Render/Railway nesta change.
- Alterar API, treino, Docker ou notebooks.
- Inventar URL pública ou lista de integrantes.

## Decisions

- **Payload em `examples/predict_payload.json`**, não 60 números inline no README. Alternativa considerada: comentário no JSON (quebra o `curl`) ou script Python que lê o parquet (o parquet não está no git). O JSON versionado deixa o exemplo estável mesmo sem cache.
- **Resposta de exemplo com o valor real do artefato atual** (~41), não um placeholder. Alternativa: omitir o body; a banca precisa ver o contrato.
- **Nuvem como receita + estado honesto** (“ainda sem URL pública”). Alternativa: silenciar Render/Railway; o PDF pede o caminho de deploy, então a receita permanece.
- **Ordem do README:** identidade/recorte → o que vem no clone → caminho rápido Docker → `/predict` + `/metrics` → treino/notebooks → nuvem/vídeo → testes/estrutura. Alternativa: só remendar seções atuais; o avaliador ainda começaria pelo treino, que não é o caminho do clone.

## Risks / Trade-offs

- [Payload envelhece se o modelo for retreinado] → o README avisa que o JSON é um exemplo da janela recente no último treino; retreino pode atualizar o arquivo.
- [Avaliador espera DIS] → uma frase no topo resolve; não mudamos o ticker.
- [Sem URL de nuvem na nota] → o README deixa o plano B (compose local + `/docs`) explícito para o vídeo.

## Migration Plan

Só documentação. Publicar o README atualizado no mesmo repositório; rollback é o commit anterior.

## Open Questions

Nenhuma. Integrantes não entram até existirem no repo.
