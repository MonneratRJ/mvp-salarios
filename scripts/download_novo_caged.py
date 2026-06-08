"""Download NOVO CAGED movement archives from the MTPS FTP server.

This script downloads only the CAGEDMOV files, using the same year/month pair
in the folder path and in the filename.

Example remote path:
ftp://ftp.mtps.gov.br/pdet/microdados/NOVO%20CAGED/2026/202604/
Example file:
CAGEDMOV202604.7Z
"""

from __future__ import annotations

import argparse
import logging
from ftplib import FTP, error_perm
from pathlib import Path
from typing import Iterator, Optional, Tuple

FTP_HOST = "ftp.mtps.gov.br"
FTP_BASE_DIR = "/pdet/microdados/NOVO CAGED"
DEFAULT_OUTPUT_DIR = Path("data/raw/novo_caged")


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download NOVO CAGED movement archives.")
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    downloaded = 0
    skipped = 0

    for year, month in iter_months(args.start_year, args.start_month, args.end_year, args.end_month):
        result = download_cagedmov_archive(year, month, args.output_dir, force=args.force)
        if result is None:
            skipped += 1
        else:
            downloaded += 1

    logger.info("Finished. Downloaded: %s | Skipped: %s", downloaded, skipped)


if __name__ == "__main__":
    main()
