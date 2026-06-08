# TI Filter Codes for MVP

This file defines the concrete code filters to build the first modeling dataset for the salary calculator.

## 1) seção (CNAE section)

Use only section:

- `J` - Informação e Comunicação

## 2) categoria (employment category)

To reduce heterogeneity in the first MVP dataset, keep only:

- `101` - Empregado geral CLT (including public employee under CLT)

Notes:

- `103` (aprendiz) is excluded in this first pass because apprenticeship contracts have a different salary structure.
- `111` (intermitente) remains excluded as previously agreed.

## 3) subclasse (CNAE subclass)

Use the core software and IT service subclasses:

- `6201500` - Desenvolvimento de programas de computador sob encomenda
- `6201501` - Desenvolvimento de Programas de Computador Sob Encomenda
- `6201502` - Web Design
- `6202300` - Desenvolvimento e Licenciamento de Programas de Computador Customizáveis
- `6203100` - Desenvolvimento e Licenciamento de Programas de Computador Não-Customizáveis
- `6204000` - Consultoria em Tecnologia da Informação
- `6209100` - Suporte Técnico, Manutenção e Outros Serviços em Tecnologia da Informação
- `6311900` - Tratamento de Dados, Provedores de Serviços de Aplicação e Serviços de Hospedagem na Internet

Optional expansion after baseline:

- `6319400` - Portais, Provedores de Conteúdo e Outros Serviços de Informação na Internet
- Telecom-related subclasses (`611*`, `612*`, `613*`, `619*`) if we decide to expand from software/IT services to broader ICT.

## 4) cbo2002ocupação (IT occupations)

Use the following occupation codes:

- `142510` - Gerente de Desenvolvimento de Sistemas
- `142515` - Gerente de Producao de Tecnologia da Informacao
- `142520` - Gerente de Projetos de Tecnologia da Informacao
- `142525` - Gerente de Seguranca de Tecnologia da Informacao
- `142530` - Gerente de Suporte Tecnico de Tecnologia da Informacao
- `142535` - Tecnólogo em Gestão da Tecnologia da Informação
- `212205` - Engenheiro de Aplicativos em Computacao
- `212210` - Engenheiro de Equipamentos em Computacao
- `212215` - Engenheiros de Sistemas Operacionais em Computacao
- `212305` - Administrador de Banco de Dados
- `212310` - Administrador de Redes
- `212315` - Administrador de Sistemas Operacionais
- `212320` - Administrador em Segurança da Informação
- `212405` - Analista de Desenvolvimento de Sistemas
- `212410` - Analista de Redes e de Comunicacao de Dados
- `212415` - Analista de Sistemas de Automacao
- `212420` - Analista de Suporte Computacional
- `212425` - Arquiteto de Soluções de Tecnologia da Informação
- `212430` - Analista de Testes de Tecnologia da Informação
- `317105` - Programador de Internet
- `317110` - Programador de Sistemas de Informacao
- `317205` - Operador de Computador (Inclusive Microcomputador)
- `317210` - Tecnico de Apoio ao Usuario de Informatica (Helpdesk)

Excluded from IT occupation list:

- `317115` - Programador de Maquinas (CNC), not software engineering role.
- `317120` - Programador de Multimidia, can be reassessed later.

## 5) Region scope

Active decision for the MVP baseline:

- Keep all Brazilian regions (national scope).
- Do not apply Sul/Sudeste restriction in the main extraction pipeline.

## 6) Filter order

Recommended order for reproducible cleaning:

1. Remove records with missing/invalid salary target.
2. Keep `categoria == 101`.
3. Keep `seção == 'J'`.
4. Keep `subclasse` in the selected TI subclass list.
5. Keep `cbo2002ocupação` in the selected IT occupation list.
6. Keep national records (no regional filter).
