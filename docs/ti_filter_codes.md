# Códigos de Filtro de TI para o MVP

Este arquivo define os filtros concretos de códigos para montar o primeiro conjunto de modelagem da calculadora de salários.

## 1) seção (seção CNAE)

Usar apenas a seção:

- `J` - Informação e Comunicação

## 2) categoria (categoria de vínculo)

Para reduzir a heterogeneidade no primeiro conjunto do MVP, manter apenas:

- `101` - Empregado geral CLT (incluindo empregado público sob CLT)

Observações:

- `103` (aprendiz) é excluído nesta primeira passagem porque contratos de aprendizagem têm estrutura salarial diferente.
- `111` (intermitente) continua excluído conforme já acordado.

## 3) subclasse (subclasse CNAE)

Usar as subclasses centrais de software e serviços de TI:

- `6201500` - Desenvolvimento de programas de computador sob encomenda
- `6201501` - Desenvolvimento de Programas de Computador Sob Encomenda
- `6201502` - Web Design
- `6202300` - Desenvolvimento e Licenciamento de Programas de Computador Customizáveis
- `6203100` - Desenvolvimento e Licenciamento de Programas de Computador Não-Customizáveis
- `6204000` - Consultoria em Tecnologia da Informação
- `6209100` - Suporte Técnico, Manutenção e Outros Serviços em Tecnologia da Informação
- `6311900` - Tratamento de Dados, Provedores de Serviços de Aplicação e Serviços de Hospedagem na Internet

Expansão opcional após o baseline:

- `6319400` - Portais, Provedores de Conteúdo e Outros Serviços de Informação na Internet
- Subclasses ligadas a telecom (`611*`, `612*`, `613*`, `619*`) se decidirmos expandir de software/serviços de TI para TIC mais ampla.

## 4) cbo2002ocupação (ocupações de TI)

Usar os seguintes códigos de ocupação:

- `142510` - Gerente de Desenvolvimento de Sistemas
- `142515` - Gerente de Produção de Tecnologia da Informação
- `142520` - Gerente de Projetos de Tecnologia da Informação
- `142525` - Gerente de Segurança de Tecnologia da Informação
- `142530` - Gerente de Suporte Técnico de Tecnologia da Informação
- `142535` - Tecnólogo em Gestão da Tecnologia da Informação
- `212205` - Engenheiro de Aplicativos em Computação
- `212210` - Engenheiro de Equipamentos em Computação
- `212215` - Engenheiro de Sistemas Operacionais em Computação
- `212305` - Administrador de Banco de Dados
- `212310` - Administrador de Redes
- `212315` - Administrador de Sistemas Operacionais
- `212320` - Administrador em Segurança da Informação
- `212405` - Analista de Desenvolvimento de Sistemas
- `212410` - Analista de Redes e de Comunicação de Dados
- `212415` - Analista de Sistemas de Automação
- `212420` - Analista de Suporte Computacional
- `212425` - Arquiteto de Soluções de Tecnologia da Informação
- `212430` - Analista de Testes de Tecnologia da Informação
- `317105` - Programador de Internet
- `317110` - Programador de Sistemas de Informação
- `317205` - Operador de Computador (Inclusive Microcomputador)
- `317210` - Técnico de Apoio ao Usuário de Informática (Helpdesk)

Excluídas da lista de TI:

- `317115` - Programador de Máquinas (CNC), não é função de engenharia de software.
- `317120` - Programador de Multimídia, pode ser reavaliado depois.

## 5) Escopo regional

Decisão ativa para o baseline do MVP:

- Manter todas as regiões brasileiras (escopo nacional).
- Não aplicar restrição Sul/Sudeste na extração principal.

## 6) Ordem dos filtros

Ordem recomendada para uma limpeza reprodutível:

1. Remover registros com target salarial ausente ou inválido.
2. Manter `categoria == 101`.
3. Manter `seção == 'J'`.
4. Manter `subclasse` na lista de subclasses de TI selecionadas.
5. Manter `cbo2002ocupação` na lista de ocupações de TI selecionadas.
6. Manter registros nacionais (sem filtro regional).
7. Manter apenas `unidadesaláriocódigo == 5` (Mês).
8. Manter apenas linhas em que `salário` e `valorsaláriofixo` estejam preenchidos e iguais.

## 7) Regra de consistência do target salarial

Para melhorar a comparabilidade dos valores salariais mensais no conjunto do MVP:

- Usar `salário` como target do modelo (`y`).
- Ignorar linhas em que `salário != valorsaláriofixo`.
- Ignorar linhas em que `salário` esteja preenchido e `valorsaláriofixo` esteja vazio.
