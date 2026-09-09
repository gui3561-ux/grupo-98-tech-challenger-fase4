## 1. README da API na nuvem

- [x] 1.1 Substituir o placeholder de URL no README pela URL pública `https://grupo-98-tech-challenger-fase4.onrender.com` (Swagger `/docs`, health `/health`) e verificar que a tabela de entregáveis aponta esse hostname e ainda diz que o vídeo será gravado depois por um integrante
- [x] 1.2 Documentar o recorte Hobby (pode dormir; acordar com `GET /health`; fallback `docker compose` + `/docs`) e verificar que o README não pede upgrade para Standard/Pro

## 2. Render Hobby (CLI)

- [x] 2.1 Pedir `render login` se `render whoami` falhar, inspecionar `srv-dagm0e942hec73cu54t0` em JSON e verificar que o `plan` listado é Hobby-compatível (`free` ou `starter` / `0.5c-512mb`), sem alterar compute
- [x] 2.2 Só se a inspeção confirmar o `plan` atual: pinar esse valor no `render.yaml` e verificar que o arquivo não contém `standard`, `pro` nem `1c-2g`; se o login não ocorrer, deixar o yaml sem `plan` e registrar isso na verificação
- [x] 2.3 Só se logs CLI mostrarem OOM/restart: aplicar ajuste leve (env de threads TF) sem subir RAM e verificar `/ready` 200 na URL pública; senão, pular e verificar que `/ready` já responde 200

## 3. Checagem pública

- [x] 3.1 Chamar `/health`, `/ready` e `POST /predict` com `examples/predict_payload.json` na URL pública e verificar HTTP 200, `predicted_close` ~40.9999 e que nenhum hostname inventado (`petr4-lstm-api.onrender.com`) entrou no README
