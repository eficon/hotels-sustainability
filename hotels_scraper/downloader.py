import os
import subprocess
from typing import Optional
from urllib.parse import urlparse

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm


class Downloader:
    __LIMIT: Optional[int] = None

    def __init__(self, output_folder: str):
        self._output_folder = output_folder

    def download_htmls(self, df: pd.DataFrame, url_column: str, post_fix: str) -> None:
        counter = 0

        for nif, url in df[url_column].items():
            if pd.isna(url) or url == "":
                print(f"{nif} no tiene información en {url_column}")
                continue

            url = url.split("?")[0]

            this_web_folder = os.path.join(self._output_folder, nif)
            os.makedirs(this_web_folder, exist_ok=True)
            html_file = os.path.join(this_web_folder, f"{nif}_{post_fix}.html")
            print(f"[{counter}] Procesando {nif} x {url_column}")
            if not os.path.exists(html_file):
                subprocess.call(
                    f"shot-scraper html {url} -o \"{html_file}\" --wait 500 --browser firefox --locale es-ES")

            if post_fix == "Empresa" and os.path.exists(html_file):
                self._download_internal_links(html_file, url, nif, post_fix)

            counter += 1
            if self.__LIMIT is not None and counter > self.__LIMIT:
                break

    def _download_internal_links(self, html_file: str, url: str, nif: str, post_fix: str) -> None:
        parsed_url = urlparse(url)
        main_url = parsed_url.scheme + "://" + parsed_url.hostname

        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
            soup = BeautifulSoup(html_content, "html.parser")
            links = [a["href"] for a in soup.find_all("a", href=True)]
            links = {link for link in links if (link.startswith(main_url) or link.startswith("/"))
                     and not link.endswith("pdf")
                     and not link.endswith("jpg")
                     and not link.endswith("png")
                     and not link.endswith("mp4")}
            this_web_folder = os.path.join(self._output_folder, nif)
            if len(links) > 0:
                for link in tqdm(links, desc=f"Internal links of {nif}"):
                    if link.endswith("/"):
                        link = link[:-1]

                    link = link.split("?")[0]
                    page_name = os.path.basename(link)
                    page_name = page_name.replace("\n", "")
                    if page_name == "" or \
                            page_name.startswith("?") or \
                            page_name.startswith("#") or \
                            page_name.startswith("@"):
                        continue
                    link = link.replace("\n", "")
                    if link.startswith("/"):
                        link = main_url + link

                    html_file = os.path.join(this_web_folder, f"{nif}_{post_fix}_{page_name}.html")
                    if not os.path.exists(html_file):
                        subprocess.call(
                            f"shot-scraper html {link} -o \"{html_file}\" --wait 500 --browser firefox --locale es-ES")
