# 🚀 Guia de Início: MVP de Machine Learning (Calculadora de Salários)

Este documento resume as diretrizes obrigatórias para que seu projeto seja aceito e bem avaliado, seguindo as fontes oficiais do curso 1, 2.

## 1. 🛑 Regras de Ouro (Não Negociáveis)

Antes de escrever a primeira linha de código, garanta que:

- **Dados inéditos:** O dataset **não pode** ser nenhum dos usados em aula (como o de temperatura global ou diabetes) 1, 3.
- **Acesso via URL:** Você deve carregar os dados diretamente de uma **URL pública** (ex.: link "Raw" do GitHub). Não é permitido fazer upload manual de arquivos .csv 1, 4.
- **Reprodutibilidade:** O código deve ser executável do início ao fim sem erros, utilizando uma semente fixa (SEED = 42) para garantir resultados consistentes 1, 5.

## 2. 📝 Estrutura obrigatória do notebook

O seu trabalho deve funcionar como um **relatório técnico executável**, seguindo esta ordem 6, 7:

- **Definição do problema:** Descreva o contexto da "Calculadora de Salários", quem é o usuário e por que prever salários com base em experiência/cargo é relevante 8.
- **Análise exploratória de dados (EDA):** Mostre a distribuição dos salários e como eles se relacionam com os anos de experiência por meio de gráficos e tabelas 9, 10.
- **Pré-processamento e pipelines:** Use **pipelines** para tratar os dados (ex.: converter cargos em números e normalizar anos de experiência) para evitar vazamento de dados (_data leakage_) 1, 11.
- **Divisão de dados:** Separe o dataset em conjunto de **treino (80%)** e **teste (20%)** 12, 13.
- **Modelagem e baseline:**
  - Crie um **baseline** simples (usando `DummyRegressor`) para servir de comparação 14, 15.
  - Treine e compare pelo menos **dois modelos candidatos** (ex.: Regressão Linear e Random Forest) 1, 16.
- **Otimização:** Realize o ajuste de hiperparâmetros (como o `RandomizedSearchCV`) em pelo menos um dos modelos para tentar melhorar os resultados 17, 18.
- **Avaliação final:** Teste o melhor modelo no conjunto de dados que ele ainda não viu (o teste) e discuta os erros cometidos 19, 20.

## 3. 📊 Métricas de sucesso (foco em regressão)

Como seu objetivo é uma calculadora de valores numéricos (salários), você deve obrigatoriamente utilizar e explicar estas métricas 7, 21:

- **MAE (Erro Médio Absoluto):** Indica, em média, quantos reais o seu modelo erra para cima ou para baixo.
- **RMSE (Raiz do Erro Quadrático Médio):** Penaliza erros maiores, sendo útil para identificar desvios graves.
- **$R^2$ (Coeficiente de Determinação):** Mostra o quanto o seu modelo explica a variação dos dados (quanto mais próximo de 1, melhor).

## 4. ✅ Checklist de entrega

Antes de postar seu MVP, verifique se 22:

- O problema está definido como **regressão**.
- O dataset foi carregado por **URL**.
- Foi utilizado um **pipeline** de pré-processamento.
- O modelo final superou o **baseline**.
- Há uma conclusão discutindo as **limitações** do modelo (ex.: "o modelo não considera a região geográfica").

**Dica para começar agora:** Abra o arquivo `template_mvp_ml_analytics_20261.py.txt` disponível nas suas fontes 23. Ele já contém a estrutura básica e os comandos de importação necessários para você apenas preencher com o seu tema de salários.
Gostaria que eu ajudasse você a redigir o texto da **Seção 1 (Definição do Problema)** focado nessa calculadora de salários?

## 5. Registro das decisões do projeto

Todas as escolhas relevantes feitas durante o desenvolvimento devem ser registradas em [docs/decision_log.md](decision_log.md) e, quando a decisão afetar o recorte de dados ou as colunas usadas no modelo, também em [docs/scope_decisions.md](scope_decisions.md).

Isso inclui, no mínimo:

- recorte de dados e filtros aplicados;
- colunas mantidas, removidas ou tratadas como redundantes;
- estratégia de armazenamento do dataset consolidado;
- tamanho da amostra de modelagem;
- baseline, modelos candidatos e parâmetros de busca;
- métricas finais e conclusão crítica.
