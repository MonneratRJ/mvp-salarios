# Decisões de Escopo do MVP de Salários

Este documento acompanha as decisões de limpeza e filtragem acordadas durante o projeto.

## Escopo atual

- O MVP está focado apenas em salários da área de Tecnologia da Informação.
- A primeira passagem de limpeza deve manter o conjunto menor e mais alinhado com o objetivo da calculadora.
- A direção atual acordada é manter cobertura nacional para o conjunto base.

## Colunas usadas para filtrar o conjunto de dados

Estas colunas serão usadas para isolar o escopo de interesse antes da engenharia de atributos.

- `seção`
- `categoria`
- `cbo2002ocupação`

## Colunas excluídas na primeira limpeza

Esses campos não são adequados para o escopo atual da calculadora porque podem adicionar ruído, instabilidade ou não representam o tipo de entrada por pessoa que queremos no MVP.

- `indtrabintermitente`

## Observações

- A filtragem por `seção`, `categoria` e `cbo2002ocupação` deve acontecer antes da modelagem.
- A filtragem regional não está ativa no baseline atual (escopo nacional).
- Regra de qualidade salarial: manter apenas `unidadesaláriocódigo = 5` (Mês).
- Regra de consistência salarial: remover linhas em que `salário != valorsaláriofixo` e linhas com `salário` preenchido, mas `valorsaláriofixo` vazio.
- Regra de variáveis temporais: manter `ano` e `mes` como contexto temporal numérico e excluir `competencia_mov` e `ano_mes` do caminho de modelagem por serem duplicatas em string.
- Regra de variáveis com baixa variabilidade: excluir `horas_contratuais` da modelagem nesta versão quando a EDA confirmar alta concentração em poucos valores dominantes.
- Qualquer mudança futura de escopo deve ser registrada aqui antes de ser aplicada no notebook.
