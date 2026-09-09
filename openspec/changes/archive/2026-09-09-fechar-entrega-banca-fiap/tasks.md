## 1. Identidade e entregáveis

- [x] 1.1 Incluir no README a tabela dos cinco integrantes (RM + nome iguais ao LICENSE) e verificar que os cinco RMs aparecem no topo junto de Grupo 98
- [x] 1.2 Atualizar a tabela de entregáveis: vídeo = gravado depois por um integrante via `/docs`; nuvem = Render, URL só depois do deploy, e verificar que não há hostname `onrender.com` inventado

## 2. Render

- [x] 2.1 Fazer o `Dockerfile` escutar `${PORT:-8000}` e verificar por inspeção do CMD/entrypoint que a porta padrão continua 8000 quando `PORT` está vazio
- [x] 2.2 Adicionar `render.yaml` com runtime Docker e health check `/health` e verificar que o arquivo declara `healthCheckPath: /health`
- [x] 2.3 Reescrever a seção Render do README (Web Service Docker, health `/health`, colar URL depois) e verificar que um leitor replica o deploy só com o README

## 3. Hiperparâmetros e naive

- [x] 3.1 No `notebooks/02_treino_e_avaliacao.ipynb`, acrescentar tabela do recorte escolhido (64/32, dropout 0.2, patience 5, batch 32, epochs 40) versus alternativas 32/16 e dropout 0.4, e verificar que o texto aponta `python -m src.model.train` como treino oficial e early stopping em `val_loss` como critério
- [x] 3.2 Incluir no notebook 02 e no README (junto das métricas) a defesa da naive em preço absoluto, ligando a previsão de exemplo (~41) ao último close (~48), e verificar que o texto não pede retreino para “ganhar” da baseline
