# MVP Salary Estimation

This repository contains the working files for a salary calculator MVP based on NOVO CAGED movement data.

## Column selection strategy

The main rule for feature selection is simple: keep only columns that would be available at prediction time for a real person and that can plausibly explain salary variation. Columns that are administrative, time-based, source-control related, or used only to describe the raw event should be excluded from the feature set.

## Scope reduction decisions

For the first cleaning pass, we are narrowing the project to salaries in the Technology Information area only. The goal is to reduce dataset size and keep the MVP focused on the final calculator use case.

The current filtering plan is:

1. Use `seção`, `categoria`, and `cbo2002ocupação` to keep only the target technology-information scope.
2. Keep national coverage (all Brazilian regions) for the main dataset.
3. Exclude `indtrabintermitente` in the first pass because it can introduce volatility that does not help the calculator objective.
4. Keep only records with `unidadesaláriocódigo == 5` (monthly payment unit).
5. Keep only records where `salário` and `valorsaláriofixo` are both filled and equal.

These decisions are documented in [docs/scope_decisions.md](docs/scope_decisions.md) and should be updated whenever the scope changes.

The concrete code lists for filtering are in [docs/ti_filter_codes.md](docs/ti_filter_codes.md).

## Filtering benchmark (test run)

We ran a full test processing on:

- `data/raw/novo_caged/2026/202604/CAGEDMOV202604.txt`

Filtered output generated at:

- `data/processed/novo_caged/2026/202604/CAGEDMOV202604_ti_filtered.csv`

### Results

| Metric                                                                                |     Value |
| ------------------------------------------------------------------------------------- | --------: |
| Raw rows (`CAGEDMOV202604.txt`)                                                       | 4,451,422 |
| Rows after salary-quality rule (`salário` valid, monthly unit, fixed salary matching) | 4,092,938 |
| Rows after TI filter (`seção` + `categoria` + `subclasse` + `cbo2002ocupação`)        |    18,517 |
| Reduction vs raw rows                                                                 |  99.5840% |
| Retained vs raw rows                                                                  |   0.4160% |

### Decision for next step

Based on this test, the current TI filtering strategy already reduces the dataset aggressively and appears sufficient to proceed with more months/years, even after the stricter salary-quality rule.

We will proceed with national scope (no Sul/Sudeste restriction) for the next downloads.

## Current processed dataset totals

After reprocessing all available months from `2020-01` through `2026-04` with the salary-quality rule, the current filtered base contains:

| Metric                  |     Value |
| ----------------------- | --------: |
| Processed monthly files |        76 |
| Total filtered rows     | 1,350,074 |
| Processed CSV size      |   0.14 GB |

## Consolidated dataset storage rule

The monthly filtered files add up to roughly 0.14 GB, so a single uncompressed consolidated CSV would exceed GitHub's 100 MB file limit.

To keep the modeling base versionable in the repository, the consolidation script now targets a gzip-compressed file:

- `data/processed/modeling/ti_salary_modeling_base.csv.gz`

On the current 2020-01 to 2026-04 corpus, the generated compressed artifact is 12.67 MB.

The notebook should prefer this compressed artifact and only fall back to the legacy `.csv` path if needed locally.

## Keep as core predictors

These fields are the most directly related to the person profile and are the first candidates for the model input.

| Column              | Reason                                                                   |
| ------------------- | ------------------------------------------------------------------------ |
| `idade`             | Basic personal attribute and usually available in a salary profile form. |
| `graudeinstrução`   | Education level is one of the strongest salary drivers.                  |
| `sexo`              | Important demographic variable for baseline analysis.                    |
| `raçacor`           | Useful for exploratory analysis and fairness monitoring.                 |
| `tipodedeficiência` | Relevant if the form collects accessibility or inclusion information.    |
| `indtrabparcial`    | Captures part-time versus full-time arrangement.                         |
| `indicadoraprendiz` | Apprenticeship status can strongly change salary structure.              |
| `horascontratuais`  | Directly related to pay and workload.                                    |
| `cbo2002ocupação`   | Occupation is one of the strongest salary determinants.                  |

## Keep as optional context features

These columns are useful if the calculator will also ask for job context, location, or sector information.

| Column      | Reason                                            |
| ----------- | ------------------------------------------------- |
| `categoria` | Employment category can affect pay rules.         |
| `região`    | Regional wage differences are relevant.           |
| `uf`        | State-level wage differences are relevant.        |
| `município` | Local labor market can influence salary.          |
| `seção`     | Economic sector can materially change pay levels. |
| `subclasse` | Finer sector detail can improve model fit.        |

If we want a calculator based only on person information, these optional fields can be removed in a simpler version.

## Do not use as predictors

These columns should stay out of the feature matrix because they are administrative, temporal, leakage-prone, or not useful for a person-level calculator.

| Column                   | Reason                                                                            |
| ------------------------ | --------------------------------------------------------------------------------- |
| `competênciamov`         | Month of the movement; useful for data slicing, not for person profile inference. |
| `saldomovimentação`      | Event balance field, not a salary driver for this MVP.                            |
| `tipoempregador`         | Employer classification, not a person attribute.                                  |
| `tipoestabelecimento`    | Establishment classification, not a person attribute.                             |
| `tipomovimentação`       | Administrative movement type, not a person profile input.                         |
| `origemdainformação`     | Source metadata, not a predictor.                                                 |
| `competênciadec`         | Administrative date field, not a person profile input.                            |
| `indicadordeforadoprazo` | Filing status metadata, not a predictor.                                          |
| `unidadesaláriocódigo`   | Encoding/metadata field, not a salary predictor.                                  |
| `indtrabintermitente`    | Excluded in the first cleaning pass because it can add volatility.                |

## Target variable

The model target will be the salary amount itself. One salary-related column will be used only as the label `y`, and it must never appear in the predictors `X`.

For implementation, the target policy is:

1. Use `salário` as `y`.
2. Accept only records with `unidadesaláriocódigo == 5` (Mês).
3. Discard records where `salário != valorsaláriofixo`.
4. Discard records where `salário` is filled but `valorsaláriofixo` is empty.

This keeps a cleaner and more comparable monthly salary dataset.

## Supporting files

- [docs/novo_caged_mov_schema.md](docs/novo_caged_mov_schema.md)
- [data/reference/novo_caged/README.md](data/reference/novo_caged/README.md)
- [docs/ti_filter_codes.md](docs/ti_filter_codes.md)

## Practical MVP choice

For the first version, the safest modeling setup is:

1. Use the core predictors first.
2. Add optional context features only if they improve validation.
3. Exclude all administrative and leakage-prone fields.
4. Keep one salary field as the target and remove it from the feature set.
5. Apply the agreed scope filters before building the model dataset.
