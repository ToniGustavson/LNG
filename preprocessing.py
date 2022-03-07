import pandas as pd


LHV_LNG = 0.006291 # kWh/m3 = MWh/10^3m3


def get_fzjColor():
    FZJcolor = pd.read_csv("Input/FZJcolor.csv")
    def rgb_to_hex(reg_vals):
        def clamp(x): 
            return int(max(0, min(x*255, 255)))
        return "#{0:02x}{1:02x}{2:02x}".format(clamp(reg_vals[0]), clamp(reg_vals[1]), clamp(reg_vals[2]))

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


def get_OPAL():
    df = pd.read_excel("Input/Pipeline_OPAL.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"]/10**6 # kWh/d -> GWh/d
    return df


def get_NEL():
    df = pd.read_excel("Input/Pipeline_NEL.xlsx")
    df.loc[:, "value"] = df.loc[:, "value"]/10**6 # kWh/d -> GWh/d
    return df

def get_ng_share():
    # Natura Gas Import, Source: Eurostat (2020),  Unit: 10**3 TWh
    data = {
        "Russia": 1625, 
        "Norway": 786, 
        "Algeria": 317, 
        "Qatar": 178, 
        "United States": 168, 
        "Others": 1179
    }
    df = pd.DataFrame.from_dict(data, orient='index')
    df.rename(columns={0:"value"}, inplace=True)
    return df

def get_solid_fuel_share():
    # Source: Eurostat, 2019
    data = {"Russia": 46.7, "United States": 17.7, "Australia": 13.7, "Colombia": 8.2, "South Africa": 2.8, "Others": 10.9}
    df = pd.DataFrame.from_dict(data, orient='index')
    df.rename(columns={0:"value"}, inplace=True)
    return df

def get_crude_oil_share():
    # Year: 2019
    data = {"Russia": 26.9, "Iraq": 9.0, "Nigeria": 7.9, "Saudi Arabia": 7.7, "Kazakhstan": 7.3, "Norway": 7.0, "Libya": 6.2, "United States": 5.3, "United Kingdom": 4.9, "Azerbaijan": 4.5, "Algeria": 2.4, "Others": 10.9}
    df = pd.DataFrame.from_dict(data, orient='index')
    df.rename(columns={0:"value"}, inplace=True)
    return df