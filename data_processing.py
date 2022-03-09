import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Speicher einlesen
capacity_max = 1106.5582

df_storage = pd.read_excel("Input/Storage/storage_data_5a.xlsx", index_col=0)
year = 2022
bool_year = [str(year) in str(x) for x in df_storage.gasDayStartedOn]
df_storage = df_storage.loc[bool_year, :]
df_storage.sort_values("gasDayStartedOn", ignore_index = True, inplace=True)

# Januar-März Werte vorgeben, restiliche Zeit soc_max = capacity_max
soc_max_day = [capacity_max for x in range(365)]
for idx, real_val in enumerate(df_storage.gasInStorage):
    soc_max_day[idx] = real_val

# Tageswerte in Stundenwerte umrechnen (Stundenwert=Tageswert), ggf interpolieren
soc_max_hour = []
for value in soc_max_day:
    hour_val = [value]
    soc_max_hour = soc_max_hour + 24 * hour_val


pass
# gasDayStartedOn
# gasInStorage


# # Pipeline Werte einlesen
# pl_import_all = pd.read_excel(
#     "Input/Pipeline_Transportation/Pipelines_Russia_EU_renamed.xlsx", index_col=0
# )

# # Entsprechendes Jahr herausfiltern
# year = 2021  # Achtung, 2020 ist Schaltjahr
# bool_year = [str(year) in x for x in pl_import_all.columns]
# pl_import_single = pl_import_all.loc[:, bool_year]
# pl_import_sum = pl_import_single.sum(axis=0)

# # Tageswerte in Stundenwerte umrechnen (Durchschnitt)
# data = []
# for value in pl_import_sum:
#     value = value / 1000  # GWh -> TWh
#     hour_val = [value / 24]
#     data = data + 24 * hour_val

# print(f"{int(sum(data))} TWh/a {year}")

