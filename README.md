# A machine learning approach to classifying sustainability practices in hotel management

## Description

This repository contains the code used for the experimental work of the paper titled 
"A MACHINE LEARNING APPROACH TO CLASSIFYING SUSTAINABILITY PRACTICES IN HOTEL MANAGEMENT"
authored by María Carmen Pérez-López, Ana María Plata Díaz, Manuel Martín Salvador, and Germán López Pérez;
and published in the Journal of Sustainable Tourism RSUS in 2024.

https://doi.org/10.1080/09669582.2024.2397645

## Code structure

- `classification`: Knime workflow to run binary classification.
- `hotel_scraper`: Python code for downloading and parsing hotels webpages, Booking.com and Google Hotels.
- `utils`: Additional Python code used for data preprocessing.

## Setup Python

- Setup a virtual environment using Python 3.8
- Install the requirements: `pip install -r requirements.txt`

## Setup Knime

- Install KNIME Analytics Platform 4.7.3
- Load `classification/classifying-hotels-sustainability.knwf`

## Running example

**Download and parse hotels pages from Booking.com**
```
python hotels_scraper/main.py
--input "hotels_sample.csv" 
--output "results_booking.csv" 
--indicators "resources/indicators.csv" 
--dump "dump_folder" 
--flavors Booking 
```

You can also skip either downloading or parsing stages using `--skip-download` or `--skip-parser`.

## Disclaimer

Please beware that the parsing script was used in 2023, so it may happen that the websites have changed
their internal structure and thus this script might need adjustments. 

USE THIS CODE AT YOUR OWN RISK.

## License

Please see LICENSE file.

