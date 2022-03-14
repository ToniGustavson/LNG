#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import plotly.graph_objects as go
from get_data import *

#%%

df = pd.read_excel("Input/Optimization/GasSocScen50_24.xlsx", index_col=0)
df.fillna(0, inplace=True)

#%%
FZJcolor = get_fzjColor()


#%%
# Demand
total_demand = df.dom_Dem + df.elec_Dem + df.ind_Dem + df.ghd_Dem
total_demand_served = df.dom_served + df.elec_served + df.ind_served + df.ghd_served
fig = go.Figure()
xvals = df.index

# fig.add_trace(
#     go.Line(
#         x=xvals,
#         y=total_demand,
#         name="Demand",
#         # mode="none",
#         line=dict(width=0.1, color=FZJcolor.get("black")),
#         # marker=marker_dict,
#     )
# )

fig.add_trace(
    go.Scatter(
        x=xvals,
        y=total_demand,
        stackgroup="two",
        name="Unserved demand",
        mode="none",
        fillcolor=FZJcolor.get("red"),
        # marker=marker_dict,
    )
)

fig.add_trace(
    go.Scatter(
        x=xvals,
        y=df.ind_served,
        stackgroup="one",
        name="ind_served",
        mode="none",
        fillcolor=FZJcolor.get("orange"),
        # marker=marker_dict,
    )
)

fig.add_trace(
    go.Scatter(
        x=xvals,
        y=df.elec_served,
        stackgroup="one",
        name="elec_served",
        mode="none",
        fillcolor=FZJcolor.get("blue")
        # marker=marker_dict,
    )
)

fig.add_trace(
    go.Scatter(
        x=xvals,
        y=df.dom_served,
        stackgroup="one",
        name="dom_served",
        mode="none",
        fillcolor=FZJcolor.get("green")
        # marker=marker_dict,
    )
)

fig.add_trace(
    go.Scatter(
        x=xvals,
        y=df.ghd_served,
        stackgroup="one",
        name="ghd_served",
        mode="none",
        fillcolor=FZJcolor.get("purple")
        # marker=marker_dict,
    )
)

#%%
# Pipeline Import
fig = go.Figure()
xvals = df.index

fig.add_trace(
    go.Scatter(
        x=xvals,
        y=df.pipeServed,
        stackgroup="one",
        name="pipeServed",
        mode="none",
        fillcolor=FZJcolor.get("yellow")
        # marker=marker_dict,
    )
)

fig.add_trace(
    go.Scatter(
        x=xvals,
        y=df.lngServed,  # lng_val / 24,
        stackgroup="one",
        name="lngServed",
        mode="none",
        fillcolor=FZJcolor.get("blue3")
        # marker=marker_dict,
    )
)

#%%
# SOC
fig = go.Figure()
xvals = df.index

fig.add_trace(
    go.Scatter(
        x=xvals,
        y=df.soc,
        stackgroup="one",
        name="soc",
        mode="none",
        fillcolor=FZJcolor.get("orange")
        # marker=marker_dict,
    )
)

#%%
# Storage Charge and discharge
storage_operation = df.lngServed + df.pipeServed - total_demand_served
storage_operation_pl = df.pipeServed - total_demand_served
storage_operation_lng = storage_operation - storage_operation_pl

storage_discharge = [min(0, x) for x in storage_operation]
storage_charge_pl = [max(0, x) for x in storage_operation_pl]
storage_charge_lng = [max(0, x) for x in storage_operation_lng]

fig = go.Figure()
xvals = df.index

# fig.add_trace(
#     go.Line(
#         x=xvals,
#         y=df.lngServed + df.pipeServed - total_demand_served,
#         # stackgroup="one",
#         name="soc",
#         # mode="none",
#         # fillcolor=FZJcolor.get("orange")
#         # marker=marker_dict,
#     )
# )

fig.add_trace(
    go.Scatter(
        x=xvals,
        y=storage_discharge,
        stackgroup="one",
        name="Discharge",
        mode="none",
        fillcolor=FZJcolor.get("red")
        # marker=marker_dict,
    )
)

fig.add_trace(
    go.Scatter(
        x=xvals,
        y=storage_charge_pl,
        stackgroup="one",
        name="Charge Pipeline",
        mode="none",
        fillcolor=FZJcolor.get("yellow")
        # marker=marker_dict,
    )
)

fig.add_trace(
    go.Scatter(
        x=xvals,
        y=storage_charge_lng,
        stackgroup="one",
        name="Charge LNG",
        mode="none",
        fillcolor=FZJcolor.get("blue")
        # marker=marker_dict,
    )
)

#%%

# # Speicher einlesen
# capacity_max = 1106.5582

# df_storage = pd.read_excel("Input/Storage/storage_data_5a.xlsx", index_col=0)
# year = 2022
# bool_year = [str(year) in str(x) for x in df_storage.gasDayStartedOn]
# df_storage = df_storage.loc[bool_year, :]
# df_storage.sort_values("gasDayStartedOn", ignore_index = True, inplace=True)

# # Januar-März Werte vorgeben, restiliche Zeit soc_max = capacity_max
# soc_max_day = [capacity_max for x in range(365)]
# for idx, real_val in enumerate(df_storage.gasInStorage):
#     soc_max_day[idx] = real_val

# # Tageswerte in Stundenwerte umrechnen (Stundenwert=Tageswert), ggf interpolieren
# soc_max_hour = []
# for value in soc_max_day:
#     hour_val = [value]
#     soc_max_hour = soc_max_hour + 24 * hour_val


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

