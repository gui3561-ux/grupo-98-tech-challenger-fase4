# AI ENGINEERING GUIDE

Este projeto utiliza uma abordagem de engenharia assistida por IA.

## Arquitetura
A arquitetura deve ser identificada a partir do código existente.
Não presuma Clean Architecture, DDD ou qualquer outro padrão sem verificar sua existência.

Quando aplicável, respeite:
- separação de responsabilidades;
- baixo acoplamento;
- alta coesão;
- inversão de dependências;
- domínio independente de infraestrutura.

## SOLID
Aplique SOLID de forma pragmática.
Não crie interfaces, factories, repositories ou abstrações apenas para cumprir um padrão.

## Clean Code
Priorize nomes claros, funções focadas, baixo acoplamento, alta coesão, legibilidade e tratamento explícito de erros.

## KISS / YAGNI / DRY
Prefira soluções simples.
Não implemente funcionalidades não solicitadas.
Evite duplicação significativa, mas não crie abstrações prematuramente.

## Dependências
Antes de adicionar dependência:
1. verifique se o projeto já possui solução equivalente;
2. avalie necessidade e compatibilidade;
3. consulte documentação oficial;
4. considere manutenção e segurança.

## Compatibilidade
Preserve APIs, schemas, banco, integrações, eventos, jobs e comportamentos existentes sempre que possível.
Breaking changes devem ser explícitas.

## Documentação
Documente decisões arquiteturais e comportamentos não óbvios.
Comentários devem explicar principalmente o porquê.

## OpenSpec
Mudanças relevantes devem utilizar o workflow OpenSpec configurado no projeto.
Não invente comandos: verifique a versão instalada e o workflow disponível.
