## Why

O serviço já está Live no Render Hobby e a API pública responde (`/health`, `/ready`, `/predict`, `/docs`). O README ainda trata a URL como pendente, o que deixa a banca sem o link de nuvem. Ajustes de instância, se existirem, precisam caber no Hobby — sem upgrade de compute e sem gravar o vídeo nesta change.

## What Changes

- Registrar no README a URL pública verificada `https://grupo-98-tech-challenger-fase4.onrender.com` (Swagger em `/docs`, health em `/health`), no lugar do placeholder “colar depois do deploy”.
- Documentar o recorte Hobby: o serviço permanece nesse plano; instância pode dormir; acordar com `/health` antes da demo; fallback local `docker compose` + `/docs`.
- Na aplicação: autenticar o Render CLI se necessário, inspecionar o serviço `srv-dagm0e942hec73cu54t0` e só então aplicar ajustes compatíveis com Hobby (env, health, documentação). **Não** subir compute para Standard/Pro (`1c-2g` ou acima).
- O vídeo continua fora: gravado depois por um integrante.

## Capabilities

### New Capabilities

- Nenhuma.

### Modified Capabilities

- `academic-notebooks`: entregáveis da fase passam a exigir a URL pública real no README; o vídeo permanece “depois”, sem hostname inventado.
- `production-ops`: README documenta o serviço Hobby já publicado (URL, health, spin-down) e proíbe upgrade de plano de compute nesta entrega.

## Impact

- Principalmente `README.md`. `render.yaml` só se a inspeção CLI mostrar um pin de `plan` já Hobby (ex.: `free` ou `starter` / `0.5c-512mb`) — nunca `standard`/`pro`.
- Sem retreino, sem mudança de contrato da API, sem gravação de vídeo.
- CLI Render (`render login` + `render services`) só para inspecionar/ajustar no Hobby; o CLI local ainda não está autenticado.
