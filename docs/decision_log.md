# Registro de Decisões do MVP de Salários

Este arquivo registra as principais decisões do projeto à medida que elas são tomadas, para que a entrega final preserve o mesmo rastro de raciocínio usado durante o desenvolvimento.

## Propósito

O objetivo deste registro é concentrar a lógica do projeto em um único local dentro de `docs/`, incluindo escopo dos dados, seleção de variáveis, escolhas de armazenamento, restrições de modelagem e decisões de avaliação.

## Decisões por tema

### Escopo dos dados

- Focar o MVP apenas em salários da área de Tecnologia da Informação.
- Manter cobertura nacional para o conjunto de base.
- Filtrar os dados brutos do CAGED usando `seção`, `categoria` e `cbo2002ocupação`.
- Excluir `indtrabintermitente` na primeira passagem de limpeza.
- Manter apenas linhas com `unidadesaláriocódigo = 5`.
- Manter apenas linhas em que `salário` e `valorsaláriofixo` estejam preenchidos e iguais.

### Variáveis temporais

- Manter `ano` e `mes` como variáveis temporais numéricas.
- Remover `competencia_mov` e `ano_mes` do caminho de modelagem porque elas duplicam a mesma informação temporal em forma de string.
- Usar `competencia_mov` apenas para fatiamento dos dados e rastreabilidade quando necessário.

### Armazenamento da base consolidada

- Consolidar os arquivos mensais filtrados em um único artefato comprimido.
- Usar `data/processed/modeling/ti_salary_modeling_base.csv.gz` em vez de um CSV sem compressão para ficar abaixo do limite de arquivos do GitHub.
- Preferir o arquivo comprimido no notebook e manter o CSV simples apenas como alternativa local.

### Configuração de modelagem

- Tratar o problema como regressão.
- Usar `salario` como alvo.
- Manter uma baseline simples com `DummyRegressor(strategy="median")`.
- Comparar pelo menos dois modelos candidatos.
- Usar `Ridge` e `RandomForestRegressor` como o primeiro par de candidatos.
- Restringir a primeira passagem de modelagem a uma amostra de 30.000 linhas para manter o notebook responsivo.
- Usar `ano`, `mes` e os preditores categóricos selecionados como conjunto de variáveis.
- Excluir `municipio` da primeira versão do modelo por causa da alta cardinalidade.

### Pré-processamento

- Usar um `Pipeline` e um `ColumnTransformer` reprodutíveis.
- Aplicar imputação pela mediana e padronização às variáveis numéricas.
- Aplicar one-hot encoding às variáveis categóricas.
- Usar `OneHotEncoder(handle_unknown="ignore", min_frequency=25)` para limitar a explosão de esparsidade em categorias raras.

### Avaliação

- Usar `MAE`, `RMSE` e `R2` na avaliação de regressão.
- Comparar os modelos candidatos com a baseline em uma divisão holdout de teste.
- Usar `RandomizedSearchCV` para uma rodada de ajuste no modelo de floresta.
- Registrar a análise final dos resíduos e manter a narrativa do notebook alinhada com as métricas.

## Resultados validados até o momento

- Tamanho do dataset consolidado comprimido: 12,67 MB.
- Tamanho da amostra de treinamento: 30.000 linhas.
- Melhor modelo ajustado atualmente: `RandomForestRegressor`.
- Métricas finais validadas no teste para o modelo ajustado: `MAE = 385965,91`, `RMSE = 3235211,00`, `R2 = 0,1855`.

## Regra de atualização

- Sempre que surgir uma nova decisão de limpeza, modelagem ou armazenamento, registre aqui antes ou ao mesmo tempo em que ela for refletida no notebook.
- Manter este arquivo curto, factual e cumulativo.
