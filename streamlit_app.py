#%%
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from get_data import *
from PIL import Image

#%%
# Get Data
FZJcolor = get_fzjColor()
lng_df = get_lng_storage()
gng_df = get_ng_storage()


# Pipelines
pl_import = get_pipeline_data()

# ng_share = get_ng_share()
# solid_fuel_share = get_solid_fuel_share()
# crude_oil_share = get_crude_oil_share()

xval = lng_df["gasDayStartedOn"]

### Functions


def annual_mean(df, scalefac):
    annual_mean_val = df.mean() * 365 / scalefac
    annual_mean_val = int(round(annual_mean_val, 0))
    return annual_mean_val


def get_color(key, default_col="blue"):
    return {"RU": FZJcolor.get(default_col)}.get(key, FZJcolor.get("grey1"))


def eurostat_plots(commodity, mode, df_all, df_single, streamlit_obj):
    unit_dict = {
        "Natural gas": "TWh",
        "LNG": "TWh",
        "Solid fuels": "kt",
        "Crude oil": "kt",
    }
    unit = unit_dict.get(commodity)
    fig = go.Figure()
    years = df_all.columns

    for _, row in df_all.iterrows():
        if "import" in mode.lower():
            marker_dict = dict(color=get_color(row.name))
        else:
            marker_dict = None
        fig.add_trace(
            go.Scatter(
                x=years,
                y=row.values,
                stackgroup="one",
                name=row.name,
                marker=marker_dict,
            )
        )
    fig.update_layout(
        title=f"{commodity} {mode} [{unit}]", font=dict(size=16),
    )

    streamlit_obj.plotly_chart(fig, use_container_width=True)
    # streamlit_obj.caption("Source: Eurostat, 2022")

    # Pie Chart
    try:
        if "import" in mode.lower():
            colors = [get_color(x) for x in df_single.index]
            marker_dict = dict(colors=colors)
        else:
            marker_dict = None

        fig = go.Figure()
        fig.add_trace(
            go.Pie(
                labels=df_single.index,
                values=df_single.values,
                hole=0.3,
                marker=marker_dict,
            )
        )
        fig.update_layout(
            title=f"{commodity} {mode} 2020 [%]", font=dict(size=16),
        )
        streamlit_obj.plotly_chart(fig, use_container_width=True)  #
        # streamlit_obj.caption("Source: Eurostat, 2022")
    except:
        streamlit_obj.markdown("No data  available")


legend_dict = dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5)
font_dict = dict(size=18)

font_size = 18

### Streamlit App
st.set_page_config(
    page_title="Energy Independence", page_icon="🇪🇺", layout="wide"  # layout="wide" 🚢
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.text("")
st.markdown("# Energy imports from Russia and possible alternatives")
st.markdown(
    "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
)


st.markdown("## Scenario calculation: Reduction of Russian gas imports")
st.markdown(
    "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
)

cols = st.columns(2)

pl_reduction = cols[0].slider(
    "Reduction of Russian gas imports [%]",
    min_value=0,
    max_value=100,
    value=90,
    step=10,
)
lng_capacity = cols[1].selectbox("LNG import capacity [TW]", [2.4, 5.6])

cols[0].markdown("### Supply and demand")
try:
    cols[0].image(get_optiImage("Flow", pl_reduction, lng_capacity))
except:
    cols[0].markdown("No image available")

cols[1].markdown("### Storage")
try:
    cols[1].image(get_optiImage("Storage", pl_reduction, lng_capacity))
except:
    cols[0].markdown("No image available")


st.text("")

st.markdown("## Energy imports, production and export by country")
st.markdown(
    "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
)


cols = st.columns(2)
region_list = get_eu27()
region_list = ["EU27"] + region_list
region = cols[0].selectbox("Region", region_list, 0)
balance = cols[1].multiselect("Balance", ["Import", "Production", "Export"], ["Import"])
with st.spinner(text="Connecting to Eurostat Database..."):
    # Import
    if "Import" in balance:
        # with st.expander("Import", expanded=True):
        st.markdown("## Import")
        ng_imports, ng_import_pie = get_eurostat_data("ng", "import", region, 7)
        lng_imports, lng_import_pie = get_eurostat_data("lng", "import", region, 7)
        oil_imports, oil_import_pie = get_eurostat_data("oil", "import", region, 12)
        sff_imports, sff_import_pie = get_eurostat_data("sff", "import", region, 7)

        cols = st.columns(4)
        eurostat_plots("Natural gas", "import", ng_imports, ng_import_pie, cols[0])
        eurostat_plots("LNG", "import", lng_imports, lng_import_pie, cols[1])
        eurostat_plots("Solid fuels", "import", sff_imports, sff_import_pie, cols[2])
        eurostat_plots("Crude oil", "import", oil_imports, oil_import_pie, cols[3])
        st.caption("Source: Eurostat, 2022")

    # Production
    if "Production" in balance:
        # with st.expander("Production", expanded=True):
        st.markdown("## Production")
        ng_production, ng_production_pie = get_eurostat_data(
            "ng", "production", region, 7
        )
        lng_production, lng_production_pie = get_eurostat_data(
            "lng", "production", region, 7
        )
        oil_production, oil_production_pie = get_eurostat_data(
            "oil", "production", region, 7
        )
        sff_production, sff_production_pie = get_eurostat_data(
            "sff", "production", region, 7
        )

        cols = st.columns(4)
        eurostat_plots(
            "Natural gas", "production", ng_production, ng_production_pie, cols[0]
        )
        eurostat_plots("LNG", "production", lng_production, lng_production_pie, cols[1])
        eurostat_plots(
            "Solid fuels", "production", sff_production, sff_production_pie, cols[2]
        )
        eurostat_plots(
            "Crude oil", "production", oil_production, oil_production_pie, cols[3]
        )

    # Export
    if "Export" in balance:
        # with st.expander("Export", expanded=False):
        st.markdown("## Export")
        ng_exports, ng_export_pie = get_eurostat_data("ng", "export", region, 7)
        lng_exports, lng_export_pie = get_eurostat_data("lng", "export", region, 7)
        oil_exports, oil_export_pie = get_eurostat_data("oil", "export", region, 7)
        sff_exports, sff_export_pie = get_eurostat_data("sff", "export", region, 7)

        cols = st.columns(4)
        eurostat_plots("Natural gas", "export", ng_exports, ng_export_pie, cols[0])
        eurostat_plots("LNG", "export", lng_exports, lng_export_pie, cols[1])
        eurostat_plots("Solid fuels", "export", sff_exports, sff_export_pie, cols[2])
        eurostat_plots("Crude oil", "export", oil_exports, oil_export_pie, cols[3])


# Pipeline Flow
st.markdown("## Physical pipeline flow of natural gas")

st.markdown(
    "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
)

fig = go.Figure()
date = pl_import.columns
for _, row in pl_import.iterrows():
    country = row.name[-3:-1]
    marker_dict = dict(color=get_countryColor(country, FZJcolor))
    fig.add_trace(
        go.Scatter(
            x=date, y=row.values, stackgroup="one", name=row.name, marker=marker_dict,
        )
    )

fig.update_layout(
    title="Pipeline flow from Russia to EU",
    yaxis_title="NG [GWh/d]",
    yaxis=dict(range=[0, 7000]),
    font=font_dict,
    legend=legend_dict,
    barmode="stack",
)
fig.update_layout(hovermode="x unified")


st.plotly_chart(fig, use_container_width=True)
st.caption("Source: ENTSOG, 2022")


st.markdown("## Storages")

st.markdown(
    "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
)


col1, col2 = st.columns(2)
col1.markdown("### Liquefied Natural Gas (LNG)")
col2.markdown("### Natural Gas (NG)")

############
###  LNG
############


# Plot inventory LNG
fig = go.Figure()
fig.add_trace(
    go.Line(
        x=xval,
        y=lng_df["dtmi"],  # dtmi_median
        name="Max capacity",
        marker=dict(color=FZJcolor.get("black3")),
    )
)


fig.add_trace(
    go.Scatter(
        x=xval,
        y=lng_df["lngInventory"],
        name="State of charge",
        marker=dict(color=FZJcolor.get("blue")),
        # mode="lines",
        # line=dict(width=0),
        fill="tozeroy",
    )
)


# fig.add_trace(
#     go.Scatter(
#         x=xval,
#         y=lng_df["dtmi_median"],
#         name="Free capacity",
#         marker=dict(color=FZJcolor.get("green")),
#         mode="lines",
#         line=dict(width=0),
#         fill="tonexty",
#     )
# )

fig.update_layout(
    title="Storage level of LNG facilities in the EU",
    yaxis_title="LNG [TWh]",
    yaxis=dict(range=[0, 60]),
    font=font_dict,
    legend=legend_dict,
)
col1.plotly_chart(fig, use_container_width=True)
col1.caption("Source: GIE, 2022")

# # Plot free capacity LNG
# fig = go.Figure()
# fig.add_trace(
#     go.Line(
#         x=xval,
#         y=lng_df["dtmi_median"],
#         name="Max capacity",
#         marker=dict(color=FZJcolor.get("black")),
#     )
# )
# fig.add_trace(
#     go.Scatter(
#         x=xval,
#         y=lng_df["free_inventory"],
#         name="Free capacity",
#         marker=dict(color=FZJcolor.get("green")),
#         fill="tozeroy",
#     )
# )

# fig.update_layout(
#     title="Spare LNG storage capacity (Max capacity - State of charge)",
#     yaxis_title="LNG [TWh]",
#     yaxis=dict(range=[0, 60]),
#     font=font_dict,
#     legend=legend_dict,
# )
# col1.plotly_chart(fig, use_container_width=True)
# col1.caption("Source: GIE, 2022")


# Send Out
fig = go.Figure()
fig.add_trace(
    go.Line(
        x=xval,
        y=lng_df["dtrs"],  # dtrs_median
        name=f"Max send out (Ø {int(lng_df['dtrs_median'].mean()*365/10**3)} TWh/a)",
        marker=dict(color=FZJcolor.get("black")),
    )
)
fig.add_trace(
    go.Scatter(
        x=xval,
        y=lng_df["sendOut"],
        name=f"Send out rate (Ø {int(lng_df['sendOut'].mean()*365/10**3)} TWh/a)",
        marker=dict(color=FZJcolor.get("blue")),
    )
)


fig.update_layout(
    title="Send out of LNG",
    yaxis_title="LNG [GWh/d]",
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
fig.add_trace(
    go.Line(
        x=xval,
        y=gng_df["workingGasVolume"],  # workingGasVolume_median
        name="Max capacity",
        marker=dict(color=FZJcolor.get("black")),
    )
)
fig.add_trace(
    go.Scatter(
        x=xval_gng,
        y=gng_df["gasInStorage"],
        name="State of charge",
        marker=dict(color=FZJcolor.get("orange")),
        fill="tozeroy",
    )
)

fig.update_layout(
    title="Storage level NG in the EU",
    yaxis_title="NG [TWh]",
    yaxis=dict(range=[0, 1200]),
    font=font_dict,
    legend=legend_dict,
)

col2.plotly_chart(fig, use_container_width=True)
col2.caption("Source: GIE, 2022")

# # Plot NG free
# fig = go.Figure()
# xval_gng = lng_df["gasDayStartedOn"]
# fig.add_trace(
#     go.Line(
#         x=xval,
#         y=gng_df["workingGasVolume_median"],
#         name="Max capacity",
#         marker=dict(color=FZJcolor.get("black")),
#     )
# )
# # fig.add_trace(go.Bar(x=xval_gng, y=gng_df["gasInStorage"], name="State of charge", marker=dict(color= rgb_to_hex(FZJcolor.orange))))
# fig.add_trace(
#     go.Scatter(
#         x=xval_gng,
#         y=gng_df["free_cap"],
#         name="Free capacity",
#         marker=dict(color=FZJcolor.get("green")),
#         fill="tozeroy",
#     )
# )

# fig.update_layout(
#     title="Spare NG storage capacity (Max capacity - State of charge)",
#     yaxis_title="NG [TWh]",
#     yaxis=dict(range=[0, 1200]),
#     font=font_dict,
#     legend=legend_dict,
# )
# col2.plotly_chart(fig, use_container_width=True)
# col2.caption("Source: GIE, 2022")

# Withdrawal
fig = go.Figure()
fig.add_trace(
    go.Line(
        x=xval,
        y=gng_df["withdrawalCapacity"],  # withdrawalCapacity_median
        name=f"Max withdrawl (Ø {int(gng_df['withdrawalCapacity_median'].mean()*365/10**3)} TWh/a)",
        marker=dict(color=FZJcolor.get("black")),
    )
)
fig.add_trace(
    go.Scatter(
        x=xval,
        y=gng_df["withdrawal"],
        name=f"Withdrawl rate (Ø {int(gng_df['withdrawal'].mean()*365/10**3)} TWh/a)",
        marker=dict(color=FZJcolor.get("orange")),
    )
)

fig.update_layout(
    title="Withdrawal of NG",
    yaxis_title="NG [GWh/d]",
    yaxis=dict(range=[0, 22000]),
    font=font_dict,
    legend=legend_dict,
)
col2.plotly_chart(fig, use_container_width=True)
col2.caption("Source: GIE, 2022")
