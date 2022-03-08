# %%
import pandas as pd
import eurostat
import matplotlib.pyplot as plt
from typing import List
import numpy as np

# %%
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

natural_gas_table = "nrg_ti_gas"
oil_table = "nrg_ti_oil"
solid_fossil_fuels_table = "nrg_ti_sff"


def look_up_siec(identifiers: List, timeout=5):
    import requests
    import lxml.html

    url = "https://dd.eionet.europa.eu/vocabulary/eurostat/siec/json"
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    siec_df = pd.DataFrame(r.json()["concepts"])
    if identifiers == []:
        return siec_df
    else:
        return siec_df[siec_df.Identifier.isin(identifiers)]


# %%
gas_df = eurostat.get_data_df(natural_gas_table)
gas_df.rename({"geo\\time": "geo"}, inplace=True, axis=1)

ng_EU = gas_df[
    gas_df.geo.isin(eu27) & gas_df.siec.isin(["G3000"]) & gas_df.unit.isin(["TJ_GCV"])
]

ng_nlargest_partner_2020 = (
    ng_EU.groupby("partner")
    .sum()
    .sort_values(by=2020, ascending=False)
    .nlargest(6, 2020)
)


# ng_nlargest_partner_2020 = (
#     ng_EU.groupby("partner")
#     .sum()
#     .sort_values(by=2020, ascending=False)[2020]
#     .nlargest(6)
# )

####

lng_EU = gas_df[
    gas_df.geo.isin(eu27) & gas_df.siec.isin(["G3200"]) & gas_df.unit.isin(["TJ_GCV"])
]
lng_nlargest_partner_2020 = (
    lng_EU.groupby("partner")
    .sum()
    .sort_values(by=2020, ascending=False)[2020]
    .nlargest(6)
)

####

combined_EU = gas_df[
    gas_df.geo.isin(eu27)
    & gas_df.siec.isin(["G3000", "G3200"])
    & gas_df.unit.isin(["TJ_GCV"])
]
combined_nlargest_partner_2020 = (
    combined_EU.groupby("partner")
    .sum()
    .sort_values(by=2020, ascending=False)[2020]
    .nlargest(6)
)

# %%
gas_df.head()

# %%
df_ng_from_RU_to_EU = gas_df[
    gas_df.geo.isin(eu27)
    & gas_df.partner.isin(["RU"])
    & gas_df.siec.isin(["G3000"])
    & gas_df.unit.isin(["TJ_GCV"])
]
df_ng_from_RU_to_EU = pd.melt(
    df_ng_from_RU_to_EU,
    id_vars=[],
    value_vars=[i for i in range(1990, 2021)],
    var_name="year",
    value_name="amount",
).sort_values(by="year", ascending=False)

df_lng_from_RU_to_EU = gas_df[
    gas_df.geo.isin(eu27)
    & gas_df.partner.isin(["RU"])
    & gas_df.siec.isin(["G3200"])
    & gas_df.unit.isin(["TJ_GCV"])
]
df_lng_from_RU_to_EU = pd.melt(
    df_lng_from_RU_to_EU,
    id_vars=[],
    value_vars=[i for i in range(1990, 2021)],
    var_name="year",
    value_name="amount",
).sort_values(by="year", ascending=False)
# %%
fig, ax = plt.subplots()
ax.bar(df_ng_from_RU_to_EU.year, df_ng_from_RU_to_EU.amount / 3600)
ax.set_title(r"Russian natural gas imports to Germany [TWh]")
plt.show()
# %%
fig, ax = plt.subplots()
ax.bar(df_lng_from_RU_to_EU.year, df_lng_from_RU_to_EU.amount / 3600)
ax.set_title(r"Russian LNG imports to Germany [TWh]")
plt.show()

# %%

sff_df = eurostat.get_data_df(solid_fossil_fuels_table)
sff_df.rename({"geo\\time": "geo"}, inplace=True, axis=1)
# %%
sff_EU = sff_df[sff_df.geo.isin(eu27)]
sff_nlargest_partner_2020 = (
    sff_EU.groupby("partner")
    .sum()
    .sort_values(by=2020, ascending=False)[2020]
    .nlargest(6)
)

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = sff_nlargest_partner_2020.index[1:]
sizes = sff_nlargest_partner_2020.values[1:]
explode = np.zeros(len(sizes))  # only "explode" the 2nd slice (i.e. 'Hogs')
explode[0] = 0.1

fig1, ax1 = plt.subplots()
ax1.pie(
    sizes, explode=explode, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90
)
ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

# %%
oil_df = eurostat.get_data_df(oil_table)
oil_df.rename({"geo\\time": "geo"}, inplace=True, axis=1)
# %%
oil_EU = oil_df[oil_df.geo.isin(eu27)]
oil_nlargest_partner_2020 = (
    oil_EU.groupby("partner")
    .sum()
    .sort_values(by=2020, ascending=False)[2020]
    .nlargest(10)
)

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = oil_nlargest_partner_2020.index[1:]
sizes = oil_nlargest_partner_2020.values[1:]
explode = np.zeros(len(sizes))  # only "explode" the 2nd slice (i.e. 'Hogs')
explode[0] = 0.1

fig1, ax1 = plt.subplots()
ax1.pie(
    sizes, explode=explode, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90
)
ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
# %%
