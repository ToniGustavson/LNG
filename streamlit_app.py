#%%
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from preprocessing import *




# Get Data
FZJcolor = get_fzjColor()
lng_df = get_lng_storage()
gng_df = get_ng_storage()

# Pipelines
pl_opal = get_OPAL()
pl_nel = get_NEL()
pl_wysokoje = get_Wysokoje()
pl_drozdovichi = get_Drozdovichi()
pl_imatra = get_Imatra()
pl_isaccea1 = get_Isaccea1()
pl_isaccea2 = get_Isaccea2()
pl_isaccea3 = get_Isaccea3()
pl_isaccea0 = get_Isaccea0()
pl_kipoi = get_Kipoi()
pl_kondratki = get_Kondratki()
pl_kotlovka = get_Kotlovka()
pl_mediesu = get_Mediesu_Aurit()
pl_narva = get_Narva()
pl_standzha = get_Strandzha()
pl_varska = get_Värska()
pl_velke = get_Velke_Kapusany()
pl_berge = get_VIP_Bereg()


ng_share = get_ng_share()
solid_fuel_share = get_solid_fuel_share()
crude_oil_share = get_crude_oil_share()

xval = lng_df["gasDayStartedOn"]

### Functions 

def annual_mean(df, scalefac):
    annual_mean_val = df.mean()*365/scalefac
    annual_mean_val = int(round(annual_mean_val, 0))
    return annual_mean_val

def get_color(key, default_col="blue"):
    return {"Russia": FZJcolor.get(default_col)}.get(key, FZJcolor.get("grey1") )


legend_dict = dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5)
font_dict = dict(size=18)

font_size = 18

### Streamlit App
st.set_page_config(
    page_title="Energy Independence", page_icon="🇪🇺", layout="wide" # layout="wide" 🚢
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("# Energy imports from Russia and possible alternatives")
st.markdown("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.")

st.markdown("## EU energy imports by country of origin")
st.markdown("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.")
cols = st.columns(3)

# Natrural Gas Import
colors = [get_color(x, default_col="blue4") for x in ng_share.index]
fig = go.Figure()
fig.add_trace(go.Pie(labels=ng_share.index, values = ng_share.value, hole=.3, marker=dict(colors=colors)))
fig.update_layout(
    title="Natural gas [10³ TWh/a]",
    font=dict(size=16),
)

cols[0].plotly_chart(fig, use_container_width=True)
cols[0].caption("Source: Eurostat, 2020")

# Solid Fuels
colors = [get_color(x, default_col="blue4") for x in solid_fuel_share.index]
fig = go.Figure()
fig.add_trace(go.Pie(labels=solid_fuel_share.index, values = solid_fuel_share.value, hole=.3, marker=dict(colors=colors)))
fig.update_layout(
    title="Solid fuels",
    font=dict(size=16),
)
cols[1].plotly_chart(fig, use_container_width=True)
cols[1].caption("Source: Eurostat, 2019")

# Crude oil imports
colors = [get_color(x, default_col="blue4") for x in crude_oil_share.index]
fig = go.Figure()
fig.add_trace(go.Pie(labels=crude_oil_share.index, values = crude_oil_share.value, hole=.3, marker=dict(colors=colors)))
fig.update_layout(
    title="Crude oil",
    font=dict(size=16),
)
cols[2].plotly_chart(fig, use_container_width=True)
cols[2].caption("Source: Eurostat, 2019")

# Pipeline Flow
st.markdown("## Pipeline import of natural gas")

st.markdown("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.")

pl_opal = get_OPAL()
pl_nel = get_NEL()
pl_wysokoje = get_Wysokoje()
pl_drozdovichi = get_Drozdovichi()
pl_imatra = get_Imatra()
pl_isaccea1 = get_Isaccea1()
pl_isaccea2 = get_Isaccea2()
pl_isaccea3 = get_Isaccea3()
pl_isaccea0 = get_Isaccea0()
pl_kipoi = get_Kipoi()
pl_kondratki = get_Kondratki()
pl_kotlovka = get_Kotlovka()
pl_mediesu = get_Mediesu_Aurit()
pl_narva = get_Narva()
pl_standzha = get_Strandzha()
pl_varska = get_Värska()
pl_velke = get_Velke_Kapusany()
pl_berge = get_VIP_Bereg()

fig = go.Figure()
# fig.add_trace(go.Scatter(x=xval, y=opal_df["value"],stackgroup='one', name = f"OPAL (Nord Stream 1, Ø {annual_mean(opal_df['value'], 10**3)} TWh/a)",  marker=dict(color= FZJcolor.get("blue2"))))
fig.add_trace(go.Scatter(x=xval, y=pl_opal["value"],stackgroup='one', name = "OPAL (DE)",  marker=dict(color= FZJcolor.get("green"))))
fig.add_trace(go.Scatter(x=xval, y=pl_nel["value"],stackgroup='one', name = f"NEL (DE)",  marker=dict(color= FZJcolor.get("green"))))
fig.add_trace(go.Scatter(x=xval, y=pl_kondratki["value"],stackgroup='one', name = f"Kondratki (PL)",  marker=dict(color= FZJcolor.get("red"))))
fig.add_trace(go.Scatter(x=xval, y=pl_kipoi["value"],stackgroup='one', name = f"Kipoi (GR)",  marker=dict(color= FZJcolor.get("grey3"))))
fig.add_trace(go.Scatter(x=xval, y=pl_wysokoje["value"],stackgroup='one', name = f"Wysokoje (PL)",  marker=dict(color= FZJcolor.get("red"))))
fig.add_trace(go.Scatter(x=xval, y=pl_drozdovichi["value"],stackgroup='one', name = f"Drozdovichi (PL)",  marker=dict(color= FZJcolor.get("red"))))
fig.add_trace(go.Scatter(x=xval, y=pl_imatra["value"],stackgroup='one', name = f"Imatra (FI)",  marker=dict(color= FZJcolor.get("red"))))
fig.add_trace(go.Scatter(x=xval, y=pl_isaccea1["value"],stackgroup='one', name = f"Isaccea I (RO)",  marker=dict(color= FZJcolor.get("orange"))))
fig.add_trace(go.Scatter(x=xval, y=pl_isaccea2["value"],stackgroup='one', name = f"Isaccea II (RO)",  marker=dict(color= FZJcolor.get("orange"))))
fig.add_trace(go.Scatter(x=xval, y=pl_isaccea3["value"],stackgroup='one', name = f"Isaccea III (RO)",  marker=dict(color= FZJcolor.get("orange"))))
fig.add_trace(go.Scatter(x=xval, y=pl_isaccea0["value"],stackgroup='one', name = f"Isaccea (RO)",  marker=dict(color= FZJcolor.get("orange"))))
fig.add_trace(go.Scatter(x=xval, y=pl_kotlovka["value"],stackgroup='one', name = f"Kotlovka (LT)",  marker=dict(color= FZJcolor.get("yellow"))))
fig.add_trace(go.Scatter(x=xval, y=pl_mediesu["value"],stackgroup='one', name = f"Mediesu Aurit (RO)",  marker=dict(color= FZJcolor.get("orange"))))
fig.add_trace(go.Scatter(x=xval, y=pl_narva["value"],stackgroup='one', name = f"Narva (EE)",  marker=dict(color= FZJcolor.get("lblue"))))
fig.add_trace(go.Scatter(x=xval, y=pl_varska["value"],stackgroup='one', name = f"Värska (EE)",  marker=dict(color= FZJcolor.get("lblue"))))
fig.add_trace(go.Scatter(x=xval, y=pl_standzha["value"],stackgroup='one', name = f"Strandzha (BG)",  marker=dict(color= FZJcolor.get("pink"))))
fig.add_trace(go.Scatter(x=xval, y=pl_berge["value"],stackgroup='one', name = f"VIP Bereg (BG)",  marker=dict(color= FZJcolor.get("pink"))))
fig.add_trace(go.Scatter(x=xval, y=pl_velke["value"],stackgroup='one', name = f"Velke Kapusany (SK)",  marker=dict(color= FZJcolor.get("blue"))))


fig.update_layout(
    title="EU pipeline imports from Russia",
    yaxis_title= "NG [GWh/d]",
    yaxis=dict(range=[0, 6700]),
    font=font_dict,
    legend=legend_dict,
    barmode='stack',
)


st.plotly_chart(fig, use_container_width=True)
st.caption("Source: ENTSOG, 2022")


st.markdown("## Storages")

st.markdown("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.")


col1, col2 = st.columns(2)
col1.markdown("### Liquefied Natural Gas (LNG)")
col2.markdown("### Natural Gas (NG)")

############
###  LNG
############


# Plot inventory LNG
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=lng_df["dtmi_median"], name = "Max capacity",  marker=dict(color= FZJcolor.get("black"))))
fig.add_trace(go.Scatter(x=xval, y=lng_df["lngInventory"], name="State of charge", marker=dict(color=FZJcolor.get("blue")), fill = 'tozeroy'))


fig.update_layout(
    title="Storage level of LNG facilities in the EU",
    yaxis_title= "LNG [TWh]",
    yaxis=dict(range=[0, 60]),
    font=font_dict,
    legend=legend_dict,
)
col1.plotly_chart(fig, use_container_width=True)
col1.caption("Source: GIE, 2022")

# Plot free capacity LNG
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=lng_df["dtmi_median"], name = "Max capacity",  marker=dict(color= FZJcolor.get("black"))))
fig.add_trace(go.Scatter(x=xval, y=lng_df["free_inventory"], name="Free capacity", marker=dict(color=FZJcolor.get("green")), fill = 'tozeroy'))


fig.update_layout(
    title="Spare LNG storage capacity (Max capacity - State of charge)",
    yaxis_title= "LNG [TWh]",
    yaxis=dict(range=[0, 60]),
    font=font_dict,
    legend=legend_dict,
)
col1.plotly_chart(fig, use_container_width=True)
col1.caption("Source: GIE, 2022")


# Send Out
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=lng_df["dtrs_median"], name = f"Max send out (Ø {int(lng_df['dtrs_median'].mean()*365/10**3)} TWh/a)",  marker=dict(color= FZJcolor.get("black"))))
fig.add_trace(go.Scatter(x=xval, y=lng_df["sendOut"], name=f"Send out rate (Ø {int(lng_df['sendOut'].mean()*365/10**3)} TWh/a)", marker=dict(color= FZJcolor.get("orange"))))


fig.update_layout(
    title="Send out of LNG",
    yaxis_title= "LNG [GWh/d]",
    yaxis=dict(range=[0, 7000]),
    font=font_dict,
    legend=legend_dict,
)
col1.plotly_chart(fig, use_container_width=True)
col1.caption("Source: GIE, 2022")

############
###  NG
############

# Plot NG
fig = go.Figure()
xval_gng = lng_df["gasDayStartedOn"]
fig.add_trace(go.Line(x=xval, y=gng_df["workingGasVolume_median"], name = "Max capacity",  marker=dict(color= FZJcolor.get("black"))))
fig.add_trace(go.Scatter(x=xval_gng, y=gng_df["gasInStorage"], name="State of charge", marker=dict(color= FZJcolor.get("blue")), fill = 'tozeroy'))

fig.update_layout(
    title="Storage level NG in the EU",
    yaxis_title= "NG [TWh]",
    yaxis=dict(range=[0, 1200]),
    font=font_dict,
    legend=legend_dict,
)

col2.plotly_chart(fig, use_container_width=True)
col2.caption("Source: GIE, 2022")

# Plot NG free
fig = go.Figure()
xval_gng = lng_df["gasDayStartedOn"]
fig.add_trace(go.Line(x=xval, y=gng_df["workingGasVolume_median"], name = "Max capacity",  marker=dict(color= FZJcolor.get("black"))))
# fig.add_trace(go.Bar(x=xval_gng, y=gng_df["gasInStorage"], name="State of charge", marker=dict(color= rgb_to_hex(FZJcolor.orange))))
fig.add_trace(go.Scatter(x=xval_gng, y=gng_df["free_cap"], name="Free capacity", marker=dict(color= FZJcolor.get("green")), fill = 'tozeroy'))

fig.update_layout(
    title="Spare NG storage capacity (Max capacity - State of charge)",
    yaxis_title= "NG [TWh]",
    yaxis=dict(range=[0, 1200]),
    font=font_dict,
    legend=legend_dict,
)
col2.plotly_chart(fig, use_container_width=True)
col2.caption("Source: GIE, 2022")

# Withdrawal
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=gng_df["withdrawalCapacity_median"], name = f"Max withdrawl (Ø {int(gng_df['withdrawalCapacity_median'].mean()*365/10**3)} TWh/a)",  marker=dict(color= FZJcolor.get("black"))))
fig.add_trace(go.Scatter(x=xval, y=gng_df["withdrawal"], name=f"Withdrawl rate (Ø {int(gng_df['withdrawal'].mean()*365/10**3)} TWh/a)", marker=dict(color= FZJcolor.get("orange"))))


fig.update_layout(
    title="Withdrawal of NG",
    yaxis_title= "NG [GWh/d]",
    yaxis=dict(range=[0, 20000]),
    font=font_dict,
    legend=legend_dict,
)
col2.plotly_chart(fig, use_container_width=True)
col2.caption("Source: GIE, 2022")