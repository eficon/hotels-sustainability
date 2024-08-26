"""

* Replace n.d. and n.s. by missing
* Convert columns to float
    * ^Rentabilidad
    * ^Margen
    * ^Rotación
    * ^Ratio
    * ^Costes
* Convert columns to int
    * ^Período
    * ^Coste medio
    * ^Capital circulante
* Remove . and convert to int
    * ^Ingresos de explotación
    * ^Result. ordinarios
    * ^Resultado del Ejercicio
    * ^Total Activo
* Remove duplicated columns

Variables interesantes:
* Booking_Estrellas_Contexto
* Booking_Puntuación_Contexto
* Booking_Nivel_Sostenibilidad_Contexto
* Google_Puntuación_Contexto
* Google_Reseñas_Contexto
* Google_Gimnasio
* Google_Piscina
* Google_Spa
* DIRECTOR EJECUTIVO CODIGO (1 HOMBRE; 2 MUJER, 3 EMPRESAS, N.D SIN DATO)
* Rentabilidad sobre recursos propios?
* Rentabilidad sobre capital empleado?
* Resultado del ejercicio - se puede normalizar o eso ya lo cubre la rentabilidad?

Columnas a separar:
* Booking_Agua_Contexto
* Booking_Destino_Contexto
* Booking_Energía_Contexto
* Booking_Naturaleza_Contexto
* Booking_Residuos_Contexto
* Google_Abastecimiento_Sostenible_Contexto
* Google_Accesibilidad_Contexto
* Google_Agua_Contexto
* Google_Certificaciones_Ecológicas_Contexto
* Google_Eficiencia_Energética_Contexto
* Google_Residuos_Contexto

Crear buckets:
* Google_Reseñas_Contexto
"""
import argparse

import numpy as np
import pandas as pd

from hotels_scraper.enums import BookingPropertySustainabilitySplits, BookingColumnsIndicators

def main(args: argparse.Namespace) -> None:
    indicador_independencia_mapping = {
        "D": 0,
        "C": 1,
        "C+": 2,
        "B-": 3,
        "B": 4,
        "B+": 5,
        "A-": 6,
        "A": 7,
        "A+": 8
    }
    columns_to_remove = [
        "Código NIF.1",
        "Localidad.1",
        "Dirección web.1",
    ]
    df = pd.read_csv(args.input)
    df.columns = df.columns.str.replace("\n", " ")
    df.drop(columns=columns_to_remove, inplace=True)

    # keep only hotels with number of employees between 10 and 250
    mask_num_employees = (df["Número empleados 2019"] >= 10) & (df["Número empleados 2019"] <= 250)
    df = df[mask_num_employees]

    missing_level_index = pd.isna(df["Booking_Nivel_Sostenibilidad_Contexto"])
    df.loc[missing_level_index, ["Booking_Nivel_Sostenibilidad_Contexto"]] = "NO_LEVEL"
    df.loc[
        df["Booking_Nivel_Sostenibilidad_Contexto"] == "NONE", ["Booking_Nivel_Sostenibilidad_Contexto"]] = "NO_LEVEL"

    df.loc[
        df["Booking_Nivel_Sostenibilidad_Contexto"] == "BRONZE", ["Booking_Nivel_Sostenibilidad_Contexto"]] = "LEVEL_1"
    df.loc[
        df["Booking_Nivel_Sostenibilidad_Contexto"] == "SILVER", ["Booking_Nivel_Sostenibilidad_Contexto"]] = "LEVEL_2"
    df.loc[
        df["Booking_Nivel_Sostenibilidad_Contexto"] == "GOLD", ["Booking_Nivel_Sostenibilidad_Contexto"]] = "LEVEL_3"

    missing_group_index = pd.isna(df["PERTENECE A UN GRUPO O HAY MÁS HOTELES"])
    df.loc[missing_group_index, ["PERTENECE A UN GRUPO O HAY MÁS HOTELES"]] = 0

    missing_playa_index = pd.isna(df["PLAYA (PLAYA= 1 HASTA 10 KM; otros)"])
    no_playa_index = df["PLAYA (PLAYA= 1 HASTA 10 KM; otros)"] == "0"
    playa_index = (df["PLAYA (PLAYA= 1 HASTA 10 KM; otros)"] == "1") | (
                df["PLAYA (PLAYA= 1 HASTA 10 KM; otros)"] == "PLAYA")
    df.loc[playa_index, ["PLAYA (PLAYA= 1 HASTA 10 KM; otros)"]] = 1
    df.loc[~playa_index, ["PLAYA (PLAYA= 1 HASTA 10 KM; otros)"]] = 0


    df["Total Activo log 2019"] = np.log(df["Total Activo EUR 2019"])


    def convert_to_numerical(value):
        return indicador_independencia_mapping.get(value, "")


    df["Indicator de Independencia num"] = df["Indicator de Independencia BvD"].apply(convert_to_numerical)

    df["Tasa variación rentabilidad económica"] = (df["Rentabilidad económica (%) % 2019"] - df[
        "Rentabilidad económica (%) % 2018"]) / df["Rentabilidad económica (%) % 2018"]
    df["Tasa variación rentabilidad financiera"] = (df["Rentabilidad financiera (%) % 2019"] - df[
        "Rentabilidad financiera (%) % 2018"]) / df["Rentabilidad financiera (%) % 2018"]

    # split Booking sustainability context into columns
    booking_columns = [
        "Booking_Estrellas_Contexto",
        "Booking_Puntuación_Contexto",
        "Booking_Nivel_Sostenibilidad_Contexto",
    ]
    for context_key, context_dict in BookingPropertySustainabilitySplits.items():
        for text, column_name in context_dict.items():
            df[column_name] = df[context_key].apply(
                lambda value: int(text in value if isinstance(value, str) else False))
            booking_columns.append(column_name)

    target_columns = [
                         "NIF",
                         "Nombre EMPRESA",
                         "Indicator de Independencia num",
                         "PERTENECE A UN GRUPO O HAY MÁS HOTELES",
                         "PLAYA (PLAYA= 1 HASTA 10 KM; otros)",
                         "Genero Director Ejecutivo",
                         "Tasa variación rentabilidad económica",
                         "Tasa variación rentabilidad financiera"
                     ] + booking_columns
    prefix_columns = [
        "Rentabilidad sobre capital empleado",
        "Rentabilidad económica",
        "Rentabilidad financiera",
        "Número empleados",
        "Endeudamiento",
        "Margen de beneficio",
        "Ingresos de explotación",
        "Ratio de solvencia",
        "Result. ordinarios antes Impuestos",
        "EBIT",
        "Total Activo log",
    ]

    for column in df.columns:
        for pre in prefix_columns:
            if not column.endswith("2019"):
                continue  # skip all years except 2019

            if column.startswith(pre):
                target_columns.append(column)

    # add up all indicators
    df["Número de indicadores"] = df[BookingColumnsIndicators].sum(axis=1)
    target_columns.append("Número de indicadores")
    target_columns = list(set(target_columns))
    target_df = df[target_columns].set_index("NIF")
    target_df.rename(columns={
        "Booking_Estrellas_Contexto": "Star rating",
        "Genero Director Ejecutivo": "Gender of CEO",
        "Número empleados 2019": "Employees",
        "PERTENECE A UN GRUPO O HAY MÁS HOTELES": "Group",
        "PLAYA (PLAYA= 1 HASTA 10 KM; otros)": "Beach",
        "EBIT 2019": "EBIT",
        "EBITDA 2019": "EBITDA",
        "Endeudamiento (%) % 2019": "Indebtedness",
        "Ingresos de explotación EUR 2019": "Operating income",
        "Margen de beneficio (%) % 2019": "Profit margin",
        "Ratio de solvencia % 2019": "Solvency",
        "Rentabilidad económica (%) % 2019": "ROA",
        "Rentabilidad financiera (%) % 2019": "ROE",
        "Rentabilidad sobre capital empleado (%) % 2019": "ROIC",
        "Result. ordinarios antes Impuestos EUR 2019": "EBT",
        "Tasa variación rentabilidad económica": "Variation in ROA",
        "Tasa variación rentabilidad financiera": "Variation in ROE",
        "Total Activo log 2019": "Asset",
        "Indicator de Independencia num": "Independence indicator",
        "Booking_Nivel_Sostenibilidad_Contexto": "Level Sustainability Index",
    }, inplace=True)
    target_df.to_csv(args.output, index_label="NIF")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Path to the raw CSV file")
    parser.add_argument("--output", type=str, help="Path to the resulting CSV file")
    args = parser.parse_args()
    main(args)