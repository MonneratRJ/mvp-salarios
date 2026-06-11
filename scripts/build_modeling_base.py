from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Iterable

import pandas as pd

DEFAULT_INPUT_DIR = Path("data/processed/novo_caged")
DEFAULT_OUTPUT_FILE = Path("data/processed/modeling/ti_salary_modeling_base.csv.gz")

COLUMN_MAP = {
    "competênciamov": "competencia_mov",
    "região": "regiao",
    "uf": "uf",
    "município": "municipio",
    "seção": "secao",
    "subclasse": "subclasse",
    "cbo2002ocupação": "cbo2002ocupacao",
    "categoria": "categoria",
    "graudeinstrução": "grau_de_instrucao",
    "idade": "idade",
    "horascontratuais": "horas_contratuais",
    "raçacor": "raca_cor",
    "sexo": "sexo",
    "tipodedeficiência": "tipo_de_deficiencia",
    "indtrabparcial": "ind_trab_parcial",
    "indicadoraprendiz": "indicador_aprendiz",
    "salário": "salario",
}

NUMERIC_COLUMNS = {
    "idade",
    "horas_contratuais",
    "salario",
}

CATEGORICAL_COLUMNS = {
    "regiao",
    "uf",
    "municipio",
    "secao",
    "subclasse",
    "cbo2002ocupacao",
    "categoria",
    "grau_de_instrucao",
    "raca_cor",
    "sexo",
    "tipo_de_deficiencia",
    "ind_trab_parcial",
    "indicador_aprendiz",
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a single modeling base from monthly TI-filtered NOVO CAGED files.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help="Directory with monthly TI-filtered CSV files.",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
        help="Target CSV file for the consolidated modeling base.",
    )
    return parser.parse_args()


def iter_monthly_files(input_dir: Path) -> Iterable[Path]:
    return sorted(input_dir.rglob("CAGEDMOV*_ti_filtered.csv"))


def convert_decimal_series(series: pd.Series) -> pd.Series:
    normalized = series.fillna("").astype(str).str.strip().str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    normalized = normalized.mask(normalized == "")
    return pd.to_numeric(normalized, errors="coerce")


def prepare_chunk(df: pd.DataFrame) -> pd.DataFrame:
    modeling = df[list(COLUMN_MAP.keys())].copy()
    modeling = modeling.rename(columns=COLUMN_MAP)

    for column in NUMERIC_COLUMNS:
        modeling[column] = convert_decimal_series(modeling[column])

    for column in CATEGORICAL_COLUMNS:
        modeling[column] = modeling[column].fillna("").astype(str).str.strip()
        modeling[column] = modeling[column].mask(modeling[column] == "", other=pd.NA)

    modeling["competencia_mov"] = modeling["competencia_mov"].fillna("").astype(str).str.strip()
    modeling["ano_mes"] = modeling["competencia_mov"]
    modeling["ano"] = pd.to_numeric(modeling["competencia_mov"].str.slice(0, 4), errors="coerce").astype("Int64")
    modeling["mes"] = pd.to_numeric(modeling["competencia_mov"].str.slice(4, 6), errors="coerce").astype("Int64")

    return modeling


def build_modeling_base(input_dir: Path, output_file: Path) -> dict:
    monthly_files = list(iter_monthly_files(input_dir))
    if not monthly_files:
        raise FileNotFoundError(f"No monthly files found under {input_dir}")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    if output_file.exists():
        output_file.unlink()

    rows_written = 0
    first_write = True

    for csv_path in monthly_files:
        logger.info("Consolidating %s", csv_path)
        monthly_df = pd.read_csv(csv_path, dtype=str)
        modeling_df = prepare_chunk(monthly_df)
        modeling_df.to_csv(
            output_file,
            mode="w" if first_write else "a",
            index=False,
            header=first_write,
            compression="infer",
        )
        rows_written += len(modeling_df)
        first_write = False

    summary = {
        "files": len(monthly_files),
        "rows": rows_written,
        "output_file": output_file,
        "output_size_mb": round(output_file.stat().st_size / (1024 * 1024), 2),
        "columns": list(prepare_chunk(pd.read_csv(monthly_files[0], dtype=str, nrows=5)).columns),
    }
    return summary


def main() -> None:
    args = parse_args()
    summary = build_modeling_base(args.input_dir, args.output_file)
    logger.info(
        "Finished consolidation | files=%s rows=%s output=%s size_mb=%s",
        summary["files"],
        summary["rows"],
        summary["output_file"],
        summary["output_size_mb"],
    )
    logger.info("Columns: %s", ", ".join(summary["columns"]))


if __name__ == "__main__":
    main()
