"""Download and process NOVO CAGED movement archives from the MTPS FTP server.

Main workflow per month:
1. Download CAGEDMOVYYYYMM.7Z.
2. Extract CAGEDMOVYYYYMM.txt.
3. Filter to TI scope and write processed CSV.
4. Delete extracted .txt (unless --keep-txt is used).
"""

from __future__ import annotations

import argparse
import logging
from ftplib import FTP, error_perm
from pathlib import Path
from typing import Iterator, Optional, Tuple

import pandas as pd

try:
    import py7zr
except ImportError:
    py7zr = None

FTP_HOST = "ftp.mtps.gov.br"
FTP_BASE_DIR = "/pdet/microdados/NOVO CAGED"
DEFAULT_OUTPUT_DIR = Path("data/raw/novo_caged")
DEFAULT_PROCESSED_DIR = Path("data/processed/novo_caged")

# TI filters agreed in project docs.
TI_SUBCLASSE = {
    "6201500",
    "6201501",
    "6201502",
    "6202300",
    "6203100",
    "6204000",
    "6209100",
    "6311900",
}

TI_CBO = {
    "142510",
    "142515",
    "142520",
    "142525",
    "142530",
    "142535",
    "212205",
    "212210",
    "212215",
    "212305",
    "212310",
    "212315",
    "212320",
    "212405",
    "212410",
    "212415",
    "212420",
    "212425",
    "212430",
    "317105",
    "317110",
    "317205",
    "317210",
}

REQUIRED_COLUMNS = [
    "compet\u00eanciamov",
    "regi\u00e3o",
    "uf",
    "munic\u00edpio",
    "se\u00e7\u00e3o",
    "subclasse",
    "saldomovimenta\u00e7\u00e3o",
    "cbo2002ocupa\u00e7\u00e3o",
    "categoria",
    "graudeinstru\u00e7\u00e3o",
    "idade",
    "horascontratuais",
    "ra\u00e7acor",
    "sexo",
    "tipoempregador",
    "tipoestabelecimento",
    "tipomovimenta\u00e7\u00e3o",
    "tipodedefici\u00eancia",
    "indtrabintermitente",
    "indtrabparcial",
    "sal\u00e1rio",
    "tamestabjan",
    "indicadoraprendiz",
    "origemdainforma\u00e7\u00e3o",
    "compet\u00eanciadec",
    "indicadordeforadoprazo",
    "unidadesal\u00e1rioc\u00f3digo",
    "valorsal\u00e1riofixo",
]


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def iter_months(start_year: int, start_month: int, end_year: int, end_month: int) -> Iterator[Tuple[int, int]]:
    year, month = start_year, start_month

    while (year, month) <= (end_year, end_month):
        yield year, month
        month += 1
        if month > 12:
            year += 1
            month = 1


def download_cagedmov_archive(
    year: int,
    month: int,
    output_dir: Path,
    force: bool = False,
) -> Optional[Path]:
    yyyymm = f"{year}{month:02d}"
    remote_dir = f"{FTP_BASE_DIR}/{year}/{yyyymm}"
    filename = f"CAGEDMOV{yyyymm}.7Z"
    local_dir = output_dir / str(year) / yyyymm
    local_dir.mkdir(parents=True, exist_ok=True)
    local_file = local_dir / filename

    if local_file.exists() and not force:
        logger.info("Skipping existing file: %s", local_file)
        return local_file

    try:
        with FTP(FTP_HOST, timeout=120) as ftp:
            ftp.login()
            ftp.cwd(remote_dir)
            with local_file.open("wb") as handle:
                ftp.retrbinary(f"RETR {filename}", handle.write)

        logger.info("Downloaded %s", local_file)
        return local_file

    except error_perm as exc:
        logger.warning("Skipping %s: %s", yyyymm, exc)
        if local_file.exists() and local_file.stat().st_size == 0:
            local_file.unlink(missing_ok=True)
        return None


def extract_archive(archive_path: Path) -> Path:
    if py7zr is None:
        raise RuntimeError("py7zr is required. Install with: pip install py7zr")

    output_dir = archive_path.parent
    expected_txt = output_dir / f"{archive_path.stem}.txt"

    if expected_txt.exists():
        logger.info("Using existing extracted file: %s", expected_txt)
        return expected_txt

    with py7zr.SevenZipFile(archive_path, mode="r") as archive:
        archive.extractall(path=output_dir)

    if expected_txt.exists():
        logger.info("Extracted %s", expected_txt)
        return expected_txt

    txt_files = sorted(output_dir.glob("*.txt"))
    if not txt_files:
        raise FileNotFoundError(f"No .txt extracted from {archive_path}")

    logger.info("Extracted %s", txt_files[0])
    return txt_files[0]


def process_txt_to_filtered_csv(
    txt_path: Path,
    output_dir: Path,
    year: int,
    month: int,
    chunksize: int = 500_000,
) -> Tuple[Path, dict]:
    yyyymm = f"{year}{month:02d}"
    month_output_dir = output_dir / str(year) / yyyymm
    month_output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = month_output_dir / f"CAGEDMOV{yyyymm}_ti_filtered.csv"

    stats = {
        "rows_total": 0,
        "rows_salary_valid": 0,
        "rows_filtered": 0,
    }

    if output_csv.exists():
        output_csv.unlink()

    first_write = True
    for chunk in pd.read_csv(
        txt_path,
        sep=";",
        encoding="utf-8",
        dtype=str,
        chunksize=chunksize,
        usecols=REQUIRED_COLUMNS,
    ):
        stats["rows_total"] += len(chunk)

        for col in [
            "categoria",
            "se\u00e7\u00e3o",
            "subclasse",
            "cbo2002ocupa\u00e7\u00e3o",
            "unidadesal\u00e1rioc\u00f3digo",
            "valorsal\u00e1riofixo",
        ]:
            chunk[col] = chunk[col].fillna("").astype(str).str.strip()

        salary = chunk["sal\u00e1rio"].fillna("").astype(str).str.strip()
        fixed_salary = chunk["valorsal\u00e1riofixo"].fillna("").astype(str).str.strip()
        salary_unit = chunk["unidadesal\u00e1rioc\u00f3digo"].fillna("").astype(str).str.strip()

        valid_salary = salary.ne("") & salary.ne("0") & salary.ne("0,00")
        salary_consistent = fixed_salary.ne("") & (salary == fixed_salary)
        monthly_salary_unit = salary_unit == "5"

        base = chunk[valid_salary & salary_consistent & monthly_salary_unit].copy()
        stats["rows_salary_valid"] += len(base)

        filtered = base[
            (base["categoria"] == "101")
            & (base["se\u00e7\u00e3o"] == "J")
            & (base["subclasse"].isin(TI_SUBCLASSE))
            & (base["cbo2002ocupa\u00e7\u00e3o"].isin(TI_CBO))
        ].copy()

        stats["rows_filtered"] += len(filtered)

        if len(filtered) > 0:
            filtered.to_csv(output_csv, mode="w" if first_write else "a", index=False, header=first_write)
            first_write = False

    return output_csv, stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download and process NOVO CAGED movement archives.")
    parser.add_argument("--start-year", type=int, required=True)
    parser.add_argument("--start-month", type=int, required=True)
    parser.add_argument("--end-year", type=int, required=True)
    parser.add_argument("--end-month", type=int, required=True)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where the archives will be stored.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Redownload files even if they already exist locally.",
    )
    parser.add_argument(
        "--process",
        action="store_true",
        help="Extract .7z and generate TI-filtered CSV for each month.",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=DEFAULT_PROCESSED_DIR,
        help="Directory where filtered outputs will be stored.",
    )
    parser.add_argument(
        "--keep-txt",
        action="store_true",
        help="Keep extracted .txt after processing (default deletes it).",
    )
    parser.add_argument(
        "--chunksize",
        type=int,
        default=500_000,
        help="Chunk size used while processing .txt files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    downloaded = 0
    skipped = 0
    processed = 0
    failed_processing = 0

    for year, month in iter_months(args.start_year, args.start_month, args.end_year, args.end_month):
        result = download_cagedmov_archive(year, month, args.output_dir, force=args.force)
        if result is None:
            skipped += 1
        else:
            downloaded += 1

        if args.process and result is not None:
            try:
                txt_path = extract_archive(result)
                output_csv, stats = process_txt_to_filtered_csv(
                    txt_path=txt_path,
                    output_dir=args.processed_dir,
                    year=year,
                    month=month,
                    chunksize=args.chunksize,
                )
                processed += 1

                retained_pct = (
                    (stats["rows_filtered"] / stats["rows_total"] * 100)
                    if stats["rows_total"]
                    else 0.0
                )
                logger.info(
                    "Processed %s | total=%s salary_valid=%s filtered=%s retained=%.4f%%",
                    output_csv,
                    stats["rows_total"],
                    stats["rows_salary_valid"],
                    stats["rows_filtered"],
                    retained_pct,
                )

                if not args.keep_txt and txt_path.exists():
                    txt_path.unlink()
                    logger.info("Deleted extracted txt: %s", txt_path)

            except Exception as exc:
                failed_processing += 1
                logger.exception("Failed processing %s: %s", result, exc)

    logger.info(
        "Finished. Downloaded: %s | Skipped: %s | Processed: %s | Processing failures: %s",
        downloaded,
        skipped,
        processed,
        failed_processing,
    )


if __name__ == "__main__":
    main()
