import json
import multiprocessing
import os
import re
from functools import partial
from glob import glob
from typing import Dict, Tuple, List

import pandas as pd
from bs4 import BeautifulSoup
from natsort import natsorted
from tqdm import tqdm

from hotels_scraper.enums import ExtractionTypes, Flavor, BookingSustainabilityMapping, \
    BookingPropertySustainabilityFacilityMapping, BookingPropertySustainabilityTextMapping


class Parser:
    _GOOGLE_STARS_REGEX = re.compile(r"([\d,\.]+) de 5 estrellas a partir de ([\d\.]+) reseñas")
    _BOOKING_COMMENTS_REGEX = re.compile(r"([\d\.]+) comentarios")
    _BOOKING_SCORE_REGEX = re.compile("Puntuación: ([\d,\.]+)")
    CONTEXT_POSTFIX = "_Contexto"

    def __init__(self, output_folder: str, indicators: Dict):
        self._output_folder = output_folder
        self._indicators = indicators

    def find_indicators_in_htmls(self) -> pd.DataFrame:
        nifs_availables = os.listdir(self._output_folder)

        with multiprocessing.Pool() as pool:
            results = []
            for result in tqdm(pool.imap_unordered(partial(Parser._process_single_nif,
                                                           output_folder=self._output_folder,
                                                           indicators=self._indicators),
                                                   nifs_availables),
                               total=len(nifs_availables),
                               desc="Finding indicators"):
                results.append(result)

        results = {nif: x[nif] for nif, x in results}

        df = pd.DataFrame(results).T
        df = Parser._sort_columns(df)
        return df

    @staticmethod
    def _sort_columns(df: pd.DataFrame) -> pd.DataFrame:
        sorted_columns = []
        for column in natsorted(df.columns):
            if column.endswith(Parser.CONTEXT_POSTFIX):
                continue
            sorted_columns.append(column)
            if column + Parser.CONTEXT_POSTFIX in df.columns:
                sorted_columns.append(column + Parser.CONTEXT_POSTFIX)
        df = df.reindex(sorted_columns, axis=1)
        return df

    @staticmethod
    def _process_single_nif(nif: str, output_folder: str, indicators: Dict) -> Tuple[str, Dict]:
        results = {nif: {}}
        for flavor in indicators:

            # initialize indicators
            for name in indicators[flavor]:
                results[nif][name] = ""

            # process all HTMLs for this company
            html_files = glob(os.path.join(output_folder, nif, f"{nif}_{flavor}*.html"))
            for html_file in html_files:
                try:
                    Parser._process_single_html(flavor, html_file, indicators, nif, results)
                except RuntimeError as e:
                    print(f"[{nif}] Can't process {html_file}: {e}")

        return nif, results

    @staticmethod
    def _process_single_html(flavor: Flavor, html_file: str, indicators: Dict, nif: str, results: Dict) -> None:
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, "html.parser")

        if flavor == Flavor.EMPRESA:
            Parser._process_empresa(soup, indicators[flavor], nif, results)
        elif flavor == Flavor.BOOKING:
            Parser._process_booking(soup, indicators[flavor], nif, results)
        elif flavor == Flavor.GOOGLE:
            Parser._process_google(soup, indicators[flavor], nif, results)
        else:
            raise ValueError(f"Flavor not supported: {flavor}")

    @staticmethod
    def _sanitize(content: str) -> str:
        content = content.replace("\n", " ")
        content = " ".join(content.split())
        return content

    @staticmethod
    def _process_empresa(soup: BeautifulSoup, indicators: Dict, nif: str, results: Dict) -> None:
        # Extract text
        html_content = soup.text.lower()

        # Find indicators
        for name in tqdm(indicators, desc="Searching indicators"):
            if results[nif][name] != "":
                continue  # skip if this indicator is already filled

            extraction_type = indicators[name]["extract"]
            keywords = indicators[name]["keywords"]
            for keyword in keywords:
                # TODO improve finding
                if keyword in html_content:
                    index = html_content.find(keyword)
                    first_index = max(index - 80, 0)
                    last_index = min(index + 80, len(html_content))
                    context = html_content[first_index:last_index]
                    occurrences = re.findall(fr"( {keyword}(\s|\.|,|;|:)+)", context)
                    if len(occurrences) == 0:
                        continue

                    if extraction_type == ExtractionTypes.PHRASE:
                        # phrases = re.findall(fr"([^.]*? {keyword} [^.]*\.)", context)
                        pass  # TODO
                    elif extraction_type == ExtractionTypes.SECTION:
                        pass  # TODO
                    elif extraction_type == ExtractionTypes.WORD:
                        pass  # TODO
                    elif extraction_type == ExtractionTypes.NUMBER:
                        pass  # TODO

                    # Set flag
                    results[nif][name] = True

                    # Add context
                    context = context.replace(keyword, f"**{keyword}**")
                    results[nif][name + Parser.CONTEXT_POSTFIX] = Parser._sanitize(context)
                    # print(f"[{name}]\t[{extraction_type}]\t{keyword=}\t`{results[nif][name + Parser.CONTEXT_POSTFIX]}`")
                    break

    @staticmethod
    def _process_booking(soup: BeautifulSoup, indicators: Dict, nif: str, results: Dict) -> None:
        all_divs = soup.find_all(name="div")
        all_scripts = soup.find_all(name="script")

        relevant_div = [div for div in all_divs
                        if "data-testid" in div.attrs and div.attrs["data-testid"] == "sustainability-banner-container"]

        if len(relevant_div) != 1:
            print("Can't find sustainability banner")
            booking_sustainability_content = None
            booking_sustainability_tier = None
        else:

            relevant_script = [script for script in all_scripts if "PropertySustainability" in script.text]
            if len(relevant_script) != 1:
                print("Problem retrieving SustainabilityBannerDesktop")
                booking_sustainability_content = None
                booking_sustainability_tier = None
            else:
                booking_sustainability_content = []
                booking_sustainability_tier = None
                relevant_script = relevant_script[0]
                script_content = json.loads(relevant_script.contents[0])
                for key, value in script_content.items():
                    if "PropertySustainabilityFacility" in key:
                        property_id = str(value["id"])
                        booking_sustainability_content.append(property_id)
                    elif "PropertySustainabilityTier" in key:
                        booking_sustainability_tier = value["type"]

        relevant_script = [script for script in all_scripts
                           if "type" in script.attrs and script.attrs["type"] == "application/json"
                           and "chainProgrammes" in script.text]
        booking_cert_content = None
        booking_stars = None
        if len(relevant_script) != 1:
            print("Problem retrieving chainProgrammes")
        else:
            relevant_script = relevant_script[0]
            relevant_json = json.loads(relevant_script.contents[0])
            if 'PropertySustainability:{}' in relevant_json and \
                    'chainProgrammes' in relevant_json['PropertySustainability:{}'] and \
                    relevant_json['PropertySustainability:{}']['chainProgrammes'] is not None:
                booking_cert_content = [f"{x['chainName']}_{x['programmeName']}"
                                        for x in relevant_json['PropertySustainability:{}']['chainProgrammes']]
            if 'StarRating:{}' in relevant_json and 'value' in relevant_json['StarRating:{}']:
                booking_stars = relevant_json['StarRating:{}']['value']

        relevant_div = [div for div in all_divs
                        if "data-capla-component" in div.attrs and div.attrs["data-capla-component"].endswith(
                "PropertyReviewScoreRight")]
        if len(relevant_div) != 1:
            print("Problem retrieving PropertyReviewScoreRight")
            score = None
            comments = None
        else:
            relevant_div = relevant_div[0]
            booking_review_content = relevant_div.contents[0].find_all("div")
            try:
                score = Parser._get_booking_score(booking_review_content)
            except RuntimeError as e:
                score = None
                print(e)
            try:
                comments = Parser._get_booking_reviews(booking_review_content)
            except Exception as e:
                comments = None
                print(e)

        # Find indicators
        for name in tqdm(indicators, desc="Searching indicators"):
            if results[nif][name] != "":
                continue  # skip if this indicator is already filled

            if name in BookingSustainabilityMapping and booking_sustainability_content is not None:
                prefix = BookingSustainabilityMapping[name]
                for property_id in booking_sustainability_content:
                    property_key = BookingPropertySustainabilityFacilityMapping[property_id]
                    if property_key.startswith(prefix):
                        # Set flag
                        results[nif][name] = True

                        # Add context
                        if name + Parser.CONTEXT_POSTFIX not in results[nif]:
                            results[nif][name + Parser.CONTEXT_POSTFIX] = ""
                        results[nif][name + Parser.CONTEXT_POSTFIX] += BookingPropertySustainabilityTextMapping[property_key] + "; "

            if name == "Booking_Puntuación" and score is not None:
                results[nif][name] = True
                results[nif][name + Parser.CONTEXT_POSTFIX] = score

            elif name == "Booking_Comentarios" and comments is not None:
                results[nif][name] = True
                results[nif][name + Parser.CONTEXT_POSTFIX] = comments

            elif name == "Booking_Estrellas" and booking_stars is not None:
                results[nif][name] = True
                results[nif][name + Parser.CONTEXT_POSTFIX] = booking_stars

            elif name == "Booking_Certificados_Sostenibilidad" and booking_cert_content is not None:
                results[nif][name] = True
                results[nif][name + Parser.CONTEXT_POSTFIX] = ";".join(booking_cert_content)

            elif name == "Booking_Nivel_Sostenibilidad" and booking_sustainability_tier is not None:
                results[nif][name] = True
                results[nif][name + Parser.CONTEXT_POSTFIX] = booking_sustainability_tier
                print(nif, booking_sustainability_tier)

    @staticmethod
    def _get_booking_reviews(booking_review_content: List) -> str:
        comments = [div.text for div in booking_review_content if div.text.endswith("comentarios")][0]
        regex_result = Parser._BOOKING_COMMENTS_REGEX.search(comments)
        if regex_result is not None:
            comments = regex_result.group(1)
        return comments

    @staticmethod
    def _get_booking_score(booking_review_content: List) -> str:
        score = [div.attrs["aria-label"] for div in booking_review_content
                 if "aria-label" in div.attrs and div.attrs["aria-label"].startswith("Puntuación")]
        if len(score) != 1:
            raise RuntimeError("Problem retrieving Puntuación")
        score = score[0]
        regex_result = Parser._BOOKING_SCORE_REGEX.search(score)
        if regex_result is not None:
            score = regex_result.group(1)
        return score

    @staticmethod
    def _process_google(soup: BeautifulSoup, indicators: Dict, nif: str, results: Dict) -> None:
        all_h4 = soup.find_all("h4")

        expected_keywords = []
        for name in indicators:
            expected_keywords.extend(indicators[name]["keywords"])

        all_div = [div for div in soup.find_all("div")
                   if "aria-label" in div.attrs and (div.attrs["aria-label"].lower() in expected_keywords
                                                     or Parser._GOOGLE_STARS_REGEX.match(
                        div.attrs["aria-label"]) is not None)]

        # Find indicators
        for name in tqdm(indicators, desc="Searching indicators"):
            if results[nif][name] != "":
                continue  # skip if this indicator is already filled

            extraction_type = indicators[name]["extract"]
            keywords = indicators[name]["keywords"]
            for keyword in keywords:
                if extraction_type == ExtractionTypes.SECTION:
                    for h4 in all_h4:
                        if keyword == h4.text.lower():
                            results[nif][name] = True
                            results[nif][name + Parser.CONTEXT_POSTFIX] = h4.text
                            results[nif][name + Parser.CONTEXT_POSTFIX] += ";" + ";".join(list(h4.nextSibling.strings))
                            break
                elif extraction_type == ExtractionTypes.PHRASE:
                    for div in all_div:
                        if keyword == div.attrs["aria-label"].lower():
                            results[nif][name] = True
                            results[nif][name + Parser.CONTEXT_POSTFIX] = div.text
                            break
                elif name in ["Google_Reseñas", "Google_Puntuación"]:
                    for div in all_div:
                        regex_result = Parser._GOOGLE_STARS_REGEX.match(div.attrs["aria-label"])
                        if regex_result is not None:
                            results[nif][name] = True
                            if name == "Google_Reseñas":
                                results[nif][name + Parser.CONTEXT_POSTFIX] = regex_result.group(2)
                            elif name == "Google_Puntuación":
                                results[nif][name + Parser.CONTEXT_POSTFIX] = regex_result.group(1)
                            break

                if results[nif][name] is True:
                    break
