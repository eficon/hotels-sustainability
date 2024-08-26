import argparse
import os
from typing import Dict, List

import pandas as pd

from hotels_scraper.downloader import Downloader
from hotels_scraper.enums import ExtractionTypes, Flavor
from hotels_scraper.parser import Parser

VALID_BOOKING_URL = "https://www.booking.com/hotel/es"
AUTOFIX = True


def sanity_check(df: pd.DataFrame) -> None:
    nifs = df["Código NIF"]
    if len(nifs.unique()) != len(nifs):
        raise RuntimeError("Hay NIFs duplicados, por favor revise el listado")

    df.set_index("Código NIF", inplace=True)

    for nif, url in df["BOOKING"].items():
        if not pd.isna(url) and not url.startswith(VALID_BOOKING_URL):
            if AUTOFIX:
                print(f"{nif} tiene una URL de booking no válida - eliminando")
                df.at[nif, "BOOKING"] = ""
            else:
                raise RuntimeError(f"{nif} tiene una URL de booking no válida: {url}")

    for nif, url in df["Dirección web"].items():
        if not url.startswith("http"):
            print(f"{nif} tiene una URL de empresa no válida - modificando")
            df.at[nif, "Dirección web"] = f"https://{url}"


def load_indicators(csv_path: str, flavors_to_load: List[Flavor] = None) -> Dict:
    df = pd.read_csv(csv_path)
    indicators = {}

    # split keywords into a list
    for i, row in df.iterrows():
        keywords = row["Búsqueda"]
        keywords = keywords.replace("\n", "/")
        keywords = keywords.split("/")
        keywords = [k.strip().lower() for k in keywords]

        flavor = Flavor(row["Web"])
        if flavors_to_load is not None and flavor not in flavors_to_load:
            continue

        if flavor not in indicators:
            indicators[flavor] = {}

        indicators[flavor][row["Identificador"]] = {
            "keywords": keywords,
            "extract": ExtractionTypes(row["Extracción"])
        }

    return indicators


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input CSV file", required=True)
    parser.add_argument("--output", type=str, help="Output CSV file", required=True)
    parser.add_argument("--dump", type=str, help="Dump folder to save html files", required=True)
    parser.add_argument("--indicators", type=str, help="CSV file with indicators", required=True)
    parser.add_argument("--flavors", type=Flavor, nargs="*", choices=list(Flavor), help="Flavors to process")
    parser.add_argument("--skip-download", action="store_true", help="Avoid to download the pages")
    parser.add_argument("--skip-parser", action="store_true", help="Avoid parsing the pages")
    args = parser.parse_args()

    output_folder = args.dump
    os.makedirs(output_folder, exist_ok=True)

    df = pd.read_csv(args.input)
    sanity_check(df)
    df.sort_index(inplace=True)

    if not args.skip_download:
        d = Downloader(output_folder)
        if Flavor.EMPRESA in args.flavors:
            d.download_htmls(df, url_column="Dirección web", post_fix="Empresa")
        if Flavor.BOOKING in args.flavors:
            d.download_htmls(df, url_column="BOOKING", post_fix="Booking")
        if Flavor.GOOGLE in args.flavors:
            d.download_htmls(df, url_column="GOOGLE", post_fix="Google")

    if not args.skip_parser:
        indicators = load_indicators(args.indicators, args.flavors)
        p = Parser(output_folder, indicators)
        results = p.find_indicators_in_htmls()
        results.to_csv(args.output, encoding="utf-8")
        results.to_excel(args.output.replace(".csv", ".xls"))


if __name__ == "__main__":
    main()
