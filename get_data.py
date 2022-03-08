import pandas as pd
import eurostat

LHV_LNG = 0.006291  # kWh/m3 = MWh/10^3m3
eu27 = [
    "AT",
    "BE",
    "BG",
    "HR",
    "CY",
    "CZ",
    "DK",
    "EE",
    "FI",
    "FR",
    "DE",
    "GR",
    "HU",
    "IE",
    "IT",
    "LV",
    "LT",
    "LU",
    "MT",
    "NL",
    "PL",
    "PT",
    "RO",
    "SK",
    "SI",
    "ES",
    "SE",
]


def get_eurostat_data(commodity, nlargest):
    table_dict = {
        "ng": "nrg_ti_gas",
        "lng": "nrg_ti_gas",
        "oil": "nrg_ti_oil",
        "sff": "nrg_ti_sff",
    }
    table_name = table_dict.get(commodity)

    df_raw = eurostat.get_data_df(table_name)
    df_raw.rename({"geo\\time": "geo"}, inplace=True, axis=1)

    if commodity == "ng":
        df = df_raw[
            df_raw.siec.isin(["G3000"]) & df_raw.unit.isin(["TJ_GCV"])
        ]  # gas_df.geo.isin(eu27)
    elif commodity == "lng":
        df = df_raw[
            df_raw.siec.isin(["G3200"]) & df_raw.unit.isin(["TJ_GCV"])
        ]  # df_raw.geo.isin(eu27)
    else:
        # df = df_raw[
        #     df_raw.geo.isin(eu27)
        # ]
        df = df_raw.copy()

    df_nlargest = (
        df.groupby("partner")
        .sum()
        .sort_values(by=2020, ascending=False)
        .nlargest(nlargest, 2020)
    )
    df_nlargest = df_nlargest / 3600  # TJ -> TWh

    total_ds = df_nlargest.loc["TOTAL", :]

    if "NSP" in df_nlargest.index:
        df_nlargest.drop(["NSP"], axis=0, inplace=True)
    if "TOTAL" in df_nlargest.index:
        df_nlargest.drop(["TOTAL"], axis=0, inplace=True)

    sum_ds = df_nlargest.sum(axis=0)

    df_nlargest.loc["Other", :] = total_ds - sum_ds

    df_single_year = df_nlargest.loc[:, 2020]
    return df_nlargest, df_single_year


def get_fzjColor():
    FZJcolor = pd.read_csv("Input/FZJcolor.csv")

    def rgb_to_hex(reg_vals):
        def clamp(x):
            return int(max(0, min(x * 255, 255)))

        return "#{0:02x}{1:02x}{2:02x}".format(
            clamp(reg_vals[0]), clamp(reg_vals[1]), clamp(reg_vals[2])
        )

    col_names = FZJcolor.columns
    hex_vals = [rgb_to_hex(FZJcolor.loc[:, col]) for col in col_names]

    FZJcolor_dict = dict(zip(col_names, hex_vals))
    return FZJcolor_dict


def get_lng_storage():
    lng_df = pd.read_excel("Input/lng_data_5a.xlsx")
    lng_df["dtmi"] = lng_df["dtmi"] * LHV_LNG
    lng_df["lngInventory"] = lng_df["lngInventory"] * LHV_LNG
    lng_df["dtmi_median"] = lng_df["dtmi"].median()
    lng_df["dtrs_median"] = lng_df["dtrs"].median()
    lng_df["free_inventory"] = lng_df["dtmi_median"] - lng_df["lngInventory"]
    return lng_df


def get_ng_storage():
    gng_df = pd.read_excel("Input/storage_data_5a.xlsx")
    gng_df["workingGasVolume_median"] = gng_df["workingGasVolume"].median()
    gng_df["withdrawalCapacity_median"] = gng_df["withdrawalCapacity"].median()
    gng_df["free_cap"] = gng_df["workingGasVolume_median"] - gng_df["gasInStorage"]
    return gng_df


def get_ng_share():
    # Natura Gas Import, Source: Eurostat (2020),  Unit: 10**3 TWh
    data = {
        "Russia": 1625,
        "Norway": 786,
        "Algeria": 317,
        "Qatar": 178,
        "United States": 168,
        "Others": 1179,
    }
    df = pd.DataFrame.from_dict(data, orient="index")
    df.rename(columns={0: "value"}, inplace=True)
    return df


def get_solid_fuel_share():
    # Source: Eurostat, 2019
    data = {
        "Russia": 46.7,
        "United States": 17.7,
        "Australia": 13.7,
        "Colombia": 8.2,
        "South Africa": 2.8,
        "Others": 10.9,
    }
    df = pd.DataFrame.from_dict(data, orient="index")
    df.rename(columns={0: "value"}, inplace=True)
    return df


def get_crude_oil_share():
    # Year: 2019
    data = {
        "Russia": 26.9,
        "Iraq": 9.0,
        "Nigeria": 7.9,
        "Saudi Arabia": 7.7,
        "Kazakhstan": 7.3,
        "Norway": 7.0,
        "Libya": 6.2,
        "United States": 5.3,
        "United Kingdom": 4.9,
        "Azerbaijan": 4.5,
        "Algeria": 2.4,
        "Others": 10.9,
    }
    df = pd.DataFrame.from_dict(data, orient="index")
    df.rename(columns={0: "value"}, inplace=True)
    return df


# Pipeline Data


def get_OPAL():
    df = pd.read_excel("Input/Pipeline_Transportation/Greifswald_OPAL.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_NEL():
    df = pd.read_excel("Input/Pipeline_Transportation/Greifswald_NEL.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Wysokoje():
    df = pd.read_excel("Input/Pipeline_Transportation/Wysokoje.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Drozdovichi():
    df = pd.read_excel("Input/Pipeline_Transportation/Drozdovichi_GCP_GAZ_SYSTEM.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Imatra():
    df = pd.read_excel("Input/Pipeline_Transportation/Imatra(Finland).xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Isaccea1():
    df = pd.read_excel("Input/Pipeline_Transportation/Isaccea - Orlovka I.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Isaccea2():
    df = pd.read_excel("Input/Pipeline_Transportation/Isaccea - Orlovka II.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Isaccea3():
    df = pd.read_excel("Input/Pipeline_Transportation/Isaccea - Orlovka III.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Isaccea0():
    df = pd.read_excel("Input/Pipeline_Transportation/Isaccea - Orlovka.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Kipoi():
    df = pd.read_excel("Input/Pipeline_Transportation/Kipoi.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Kondratki():
    df = pd.read_excel("Input/Pipeline_Transportation/Kondratki.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Kotlovka():
    df = pd.read_excel("Input/Pipeline_Transportation/Kotlovka.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Mediesu_Aurit():
    df = pd.read_excel("Input/Pipeline_Transportation/Mediesu Aurit - Tekovo.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Narva():
    df = pd.read_excel("Input/Pipeline_Transportation/Narva.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Strandzha():
    df = pd.read_excel("Input/Pipeline_Transportation/Strandzha 2.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Värska():
    df = pd.read_excel("Input/Pipeline_Transportation/Värska.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_Velke_Kapusany():
    df = pd.read_excel("Input/Pipeline_Transportation/Velke Kapusany (Eustream).xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df


def get_VIP_Bereg():
    df = pd.read_excel("Input/Pipeline_Transportation/VIP Bereg.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"] / 10 ** 6  # kWh/d -> GWh/d
    return df

