# Scope Decisions for the Salary Calculator MVP

This document tracks the cleaning and filtering decisions agreed during the project.

## Current scope

- The MVP is focused on salaries from the Technology Information area only.
- The first cleaning pass should keep the dataset smaller and more aligned with the calculator goal.
- Current agreed direction: keep national coverage for the baseline dataset.

## Columns used for filtering the dataset

These columns will be used to isolate the scope of interest before feature engineering.

- `seção`
- `categoria`
- `cbo2002ocupação`

## Columns to exclude in the first cleaning pass

These fields are not a good fit for the current calculator scope because they can add noise, instability, or do not reflect the person-level input we want for the MVP.

- `indtrabintermitente`

## Notes

- Filtering by `seção`, `categoria`, and `cbo2002ocupação` should happen before modeling.
- Regional filtering is not active in the current baseline (national scope).
- Any future scope change should be logged here before it is applied in the notebook.
