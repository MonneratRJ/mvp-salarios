# MVP de Estimativa Salarial

Este repositório contém os arquivos de trabalho para um MVP de calculadora salarial baseado em dados de movimentação do NOVO CAGED.

## Estratégia de seleção de colunas

A regra principal para seleção de atributos é simples: manter apenas colunas que estariam disponíveis no momento da previsão para uma pessoa real e que possam explicar de forma plausível a variação salarial. Colunas administrativas, temporais, relacionadas ao controle de versão ou usadas apenas para descrever o evento bruto devem ser excluídas do conjunto de atributos.

Para informação temporal, prefira o desdobramento numérico `ano` + `mes` em vez das duplicatas em string `competencia_mov` + `ano_mes`. A forma numérica é mais fácil de modelar e reduz a complexidade do pré-processamento sem perda de informação.

## Decisões de redução de escopo

Na primeira passagem de limpeza, estamos restringindo o projeto a salários da área de Tecnologia da Informação. O objetivo é reduzir o tamanho do conjunto de dados e manter o MVP focado no caso de uso final da calculadora.

O plano atual de filtragem é:

1. Usar `seção`, `categoria` e `cbo2002ocupação` para manter apenas o escopo de Tecnologia da Informação.
2. Manter cobertura nacional (todas as regiões brasileiras) no conjunto principal.
3. Excluir `indtrabintermitente` na primeira passagem porque ele pode introduzir volatilidade que não ajuda o objetivo da calculadora.
4. Manter apenas registros com `unidadesaláriocódigo == 5` (unidade de pagamento mensal).
5. Manter apenas registros em que `salário` e `valorsaláriofixo` estejam preenchidos e iguais.

Essas decisões estão documentadas em [docs/scope_decisions.md](docs/scope_decisions.md) e devem ser atualizadas sempre que o escopo mudar.

As listas concretas de códigos para filtragem estão em [docs/ti_filter_codes.md](docs/ti_filter_codes.md).

## Referência de filtragem (teste)

Executamos um processamento de teste completo em:

- `data/raw/novo_caged/2026/202604/CAGEDMOV202604.txt`

Saída filtrada gerada em:

- `data/processed/novo_caged/2026/202604/CAGEDMOV202604_ti_filtered.csv`

### Resultados

| Métrica                                                                                               |     Valor |
| ----------------------------------------------------------------------------------------------------- | --------: |
| Linhas brutas (`CAGEDMOV202604.txt`)                                                                  | 4,451,422 |
| Linhas após a regra de qualidade salarial (`salário` válido, unidade mensal, salário fixo compatível) | 4,092,938 |
| Linhas após o filtro de TI (`seção` + `categoria` + `subclasse` + `cbo2002ocupação`)                  |    18,517 |
| Redução em relação às linhas brutas                                                                   |  99.5840% |
| Retido em relação às linhas brutas                                                                    |   0.4160% |

### Decisão para o próximo passo

Com base nesse teste, a estratégia atual de filtragem de TI já reduz o conjunto de dados de forma agressiva e parece suficiente para seguir com mais meses/anos, mesmo após a regra mais rígida de qualidade salarial.

Vamos manter o escopo nacional (sem restrição Sul/Sudeste) para os próximos downloads.

## Totais atuais do conjunto processado

Após reprocessar todos os meses disponíveis de `2020-01` até `2026-04` com a regra de qualidade salarial, a base filtrada atual contém:

| Métrica                      |     Valor |
| ---------------------------- | --------: |
| Arquivos mensais processados |        76 |
| Total de linhas filtradas    | 1,350,074 |
| Tamanho do CSV processado    |   0.14 GB |

## Regra de armazenamento do dataset consolidado

Os arquivos mensais filtrados somam aproximadamente 0.14 GB, então um único CSV consolidado sem compressão ultrapassaria o limite de 100 MB do GitHub.

Para manter a base de modelagem versionável no repositório, o script de consolidação agora gera um arquivo compactado em gzip:

- `data/processed/modeling/ti_salary_modeling_base.csv.gz`

No corpus atual de `2020-01` até `2026-04`, o artefato comprimido gerado tem 12.67 MB.

O notebook deve preferir esse artefato comprimido e usar o caminho legado `.csv` apenas como fallback local.

## Manter como preditores principais

Esses campos são os mais diretamente ligados ao perfil da pessoa e são os primeiros candidatos para entrada do modelo.

| Coluna              | Motivo                                                                      |
| ------------------- | --------------------------------------------------------------------------- |
| `idade`             | Atributo pessoal básico e geralmente disponível em um formulário salarial.  |
| `graudeinstrução`   | Nível de escolaridade é um dos principais fatores de salário.               |
| `sexo`              | Variável demográfica importante para análise de base.                       |
| `raçacor`           | Útil para análise exploratória e monitoramento de justiça/fairness.         |
| `tipodedeficiência` | Relevante se o formulário coleta informações de acessibilidade ou inclusão. |
| `indtrabparcial`    | Captura a situação de jornada parcial versus integral.                      |
| `indicadoraprendiz` | A condição de aprendiz pode alterar fortemente a estrutura salarial.        |
| `horascontratuais`  | Relacionado diretamente com remuneração e carga horária.                    |
| `cbo2002ocupação`   | A ocupação é um dos determinantes mais fortes do salário.                   |

## Manter como variáveis contextuais opcionais

Essas colunas são úteis se a calculadora também perguntar por contexto de trabalho, localização ou setor.

| Coluna      | Motivo                                                               |
| ----------- | -------------------------------------------------------------------- |
| `categoria` | A categoria de vínculo pode afetar regras de pagamento.              |
| `região`    | Diferenças regionais de salário são relevantes.                      |
| `uf`        | Diferenças salariais entre estados são relevantes.                   |
| `município` | O mercado de trabalho local pode influenciar o salário.              |
| `seção`     | O setor econômico pode alterar materialmente o nível de remuneração. |
| `subclasse` | Detalhe setorial mais fino pode melhorar o ajuste do modelo.         |

Se quisermos uma calculadora baseada apenas em informações da pessoa, essas colunas opcionais podem ser removidas em uma versão mais simples.

## Manter como variáveis temporais contextuais

Essas colunas são úteis porque preservam o contexto temporal sem duplicar a mesma informação em forma de string.

| Coluna | Motivo                                                                  |
| ------ | ----------------------------------------------------------------------- |
| `ano`  | Variável numérica de ano que ajuda a capturar tendência temporal ampla. |
| `mes`  | Variável numérica de mês que ajuda a capturar efeitos sazonais.         |

As colunas string redundantes `competencia_mov` e `ano_mes` devem ficar fora da entrada do modelo quando `ano` e `mes` já estiverem disponíveis.

## Não usar como preditores

Essas colunas devem ficar fora da matriz de atributos porque são administrativas, temporais, propensas a vazamento ou não úteis para uma calculadora salarial centrada na pessoa.

| Coluna                   | Motivo                                                                             |
| ------------------------ | ---------------------------------------------------------------------------------- |
| `competencia_mov`        | Mês da movimentação; útil para fatiamento de dados, não para inferência do perfil. |
| `ano_mes`                | Redundante com `ano` + `mes`; mantenha o desdobramento numérico.                   |
| `saldomovimentação`      | Campo de balanço do evento, não é um fator de salário para este MVP.               |
| `tipoempregador`         | Classificação do empregador, não é atributo da pessoa.                             |
| `tipoestabelecimento`    | Classificação do estabelecimento, não é atributo da pessoa.                        |
| `tipomovimentação`       | Tipo administrativo de movimentação, não é entrada do perfil da pessoa.            |
| `origemdainformação`     | Metadado de origem, não é preditor.                                                |
| `competênciadec`         | Campo de data administrativa, não é entrada do perfil da pessoa.                   |
| `indicadordeforadoprazo` | Metadado de status de envio, não é preditor.                                       |
| `unidadesaláriocódigo`   | Campo de codificação/metadado, não é preditor de salário.                          |
| `indtrabintermitente`    | Excluído na primeira limpeza porque pode adicionar volatilidade.                   |

## Variável alvo

O alvo do modelo será o próprio valor salarial. Uma coluna relacionada ao salário será usada apenas como rótulo `y`, e nunca deve aparecer nos preditores `X`.

Para implementação, a política do alvo é:

1. Usar `salário` como `y`.
2. Aceitar apenas registros com `unidadesaláriocódigo == 5` (Mês).
3. Descartar registros em que `salário != valorsaláriofixo`.
4. Descartar registros em que `salário` esteja preenchido, mas `valorsaláriofixo` esteja vazio.

Isso mantém um conjunto salarial mensal mais limpo e comparável.

## Arquivos de apoio

- [docs/novo_caged_mov_schema.md](docs/novo_caged_mov_schema.md)
- [data/reference/novo_caged/README.md](data/reference/novo_caged/README.md)
- [docs/ti_filter_codes.md](docs/ti_filter_codes.md)

## Escolha prática do MVP

Para a primeira versão, a configuração de modelagem mais segura é:

1. Usar primeiro os preditores principais.
2. Adicionar variáveis contextuais opcionais apenas se elas melhorarem a validação.
3. Excluir todos os campos administrativos e propensos a vazamento.
4. Manter `ano` e `mes` se o contexto temporal for útil, mas remover `competencia_mov` e `ano_mes` porque eles duplicam a mesma informação em string.
5. Manter um campo salarial como alvo e removê-lo do conjunto de atributos.
6. Aplicar os filtros de escopo acordados antes de construir o dataset do modelo.
