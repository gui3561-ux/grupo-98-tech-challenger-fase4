## 1. Exemplo reproduzível

- [x] 1.1 Criar `examples/predict_payload.json` com exatamente 60 fechamentos finitos (janela recente usada no último teste da API) e verificar que o JSON tem chave `prices` de length 60
- [x] 1.2 Rodar a previsão localmente com esse payload (API já no ar ou TestClient) e gravar o `predicted_close` real para o README, verificando ticker `PETR4.SA`, horizon `D+1` e número finito

## 2. README

- [x] 2.1 Reordenar o README (identidade/recorte → clone → Docker rápido → `/predict` + `/metrics` → treino/notebooks → nuvem/vídeo → testes/estrutura) e verificar que o topo cita Grupo 98, PETR4.SA, D+1 e que DIS no enunciado é exemplo
- [x] 2.2 Documentar o que o clone contém (`models/` versionado, `data/raw.parquet` fora do git) e verificar que treino/notebooks ficam descritos como download via yfinance se o cache não existir
- [x] 2.3 Trocar o `curl` quebrado por um comando que lê `examples/predict_payload.json`, incluir a resposta real do passo 1.2 e um `curl` de `/metrics` depois do predict, e verificar que o README não contém `/*` dentro do JSON e que cita contagem, latência, CPU e memória
- [x] 2.4 Declarar entregáveis da fase (docs, Docker, vídeo da API em `/docs`, ainda sem URL pública) e completar a árvore (`tests/`, `Dockerfile`, `compose.yaml`, `examples/`), verificando que não há URL de produção inventada e que a naive vs LSTM permanece
