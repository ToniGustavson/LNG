#%%
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

#%%
### Reading in Data
FZJcolor = pd.read_csv("Input/FZJcolor.csv")
lng_df = pd.read_excel("Input/lng_data_5a.xlsx")
gng_df = pd.read_excel("Input/storage_data_5a.xlsx")
LHV_LNG = 0.006291 # kWh/m3 = MWh/10^3m3

### Data manipulation
lng_df["dtmi"] = lng_df["dtmi"] * LHV_LNG
lng_df["lngInventory"] = lng_df["lngInventory"] * LHV_LNG
lng_df["dtmi_median"] = lng_df["dtmi"].median()
lng_df["dtrs_median"] = lng_df["dtrs"].median()

lng_df["free_inventory"] = lng_df["dtmi_median"] - lng_df["lngInventory"]
xval = lng_df["gasDayStartedOn"]

gng_df["workingGasVolume_median"] = gng_df["workingGasVolume"].median()
gng_df["withdrawalCapacity_median"] = gng_df["withdrawalCapacity"].median()
gng_df["free_cap"] = gng_df["workingGasVolume_median"] - gng_df["gasInStorage"]

#### Functions
def rgb_to_hex(reg_vals):
    def clamp(x): 
        return int(max(0, min(x*255, 255)))
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(reg_vals[0]), clamp(reg_vals[1]), clamp(reg_vals[2]))



### Streamlit App
st.set_page_config(
    page_title="LNG", page_icon="🚢", layout="wide" # layout="wide"
)


st.title("(In)Dependence from Russian Natural Gas")


col1, col2 = st.columns(2)

col1.markdown("## LNG Storages")
col2.markdown("## NG Storages")

############
###  LNG
############


# Plot inventory LNG
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=lng_df["dtmi_median"], name = "Max capacity",  marker=dict(color= rgb_to_hex(FZJcolor.black))))
fig.add_trace(go.Scatter(x=xval, y=lng_df["lngInventory"], name="State of charge", marker=dict(color= rgb_to_hex(FZJcolor.blue)), fill = 'tozeroy'))


fig.update_layout(
    title="Storage level of LNG facilities in the EU",
    yaxis_title= "LNG [TWh]",
    yaxis=dict(range=[0, 60]),
    font=dict(
        size=18,
    )
)
col1.plotly_chart(fig, use_container_width=True)


# Plot free capacity LNG
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=lng_df["dtmi_median"], name = "Max capacity",  marker=dict(color= rgb_to_hex(FZJcolor.black))))
fig.add_trace(go.Scatter(x=xval, y=lng_df["free_inventory"], name="Free capacity", marker=dict(color= rgb_to_hex(FZJcolor.green)), fill = 'tozeroy'))


fig.update_layout(
    title="Spare LNG storage capacity (Max capacity - State of charge)",
    yaxis_title= "LNG [TWh]",
    yaxis=dict(range=[0, 60]),
    font=dict(
        size=18,
    )
)
col1.plotly_chart(fig, use_container_width=True)



# Send Out
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=lng_df["dtrs_median"], name = f"Max send out (Ø {int(lng_df['dtrs_median'].mean()*365/10**3)} TWh/a)",  marker=dict(color= rgb_to_hex(FZJcolor.black))))
fig.add_trace(go.Scatter(x=xval, y=lng_df["sendOut"], name=f"Send out rate (Ø {int(lng_df['sendOut'].mean()*365/10**3)} TWh/a)", marker=dict(color= rgb_to_hex(FZJcolor.orange))))


fig.update_layout(
    title="Send out of LNG",
    yaxis_title= "LNG [GWh/d]",
    yaxis=dict(range=[0, 7000]),
    font=dict(
        size=18,
    )
)
col1.plotly_chart(fig, use_container_width=True)


############
###  NG
############

# Plot NG
fig = go.Figure()
xval_gng = lng_df["gasDayStartedOn"]
fig.add_trace(go.Line(x=xval, y=gng_df["workingGasVolume_median"], name = "Max capacity",  marker=dict(color= rgb_to_hex(FZJcolor.black))))
fig.add_trace(go.Scatter(x=xval_gng, y=gng_df["gasInStorage"], name="State of charge", marker=dict(color= rgb_to_hex(FZJcolor.blue)), fill = 'tozeroy'))

fig.update_layout(
    title="Storage level NG in the EU",
    yaxis_title= "NG [TWh]",
    yaxis=dict(range=[0, 1200]),
    font=dict(
        size=18,
    )
)

col2.plotly_chart(fig, use_container_width=True)

# Plot NG free
fig = go.Figure()
xval_gng = lng_df["gasDayStartedOn"]
fig.add_trace(go.Line(x=xval, y=gng_df["workingGasVolume_median"], name = "Max capacity",  marker=dict(color= rgb_to_hex(FZJcolor.black))))
# fig.add_trace(go.Bar(x=xval_gng, y=gng_df["gasInStorage"], name="State of charge", marker=dict(color= rgb_to_hex(FZJcolor.orange))))
fig.add_trace(go.Scatter(x=xval_gng, y=gng_df["free_cap"], name="Free capacity", marker=dict(color= rgb_to_hex(FZJcolor.green)), fill = 'tozeroy'))

fig.update_layout(
    title="Spare NG storage capacity (Max capacity - State of charge)",
    yaxis_title= "NG [TWh]",
    yaxis=dict(range=[0, 1200]),
    font=dict(
        size=18,
    )
)
col2.plotly_chart(fig, use_container_width=True)

# Withdrawal
fig = go.Figure()
fig.add_trace(go.Line(x=xval, y=gng_df["withdrawalCapacity_median"], name = f"Max withdrawl (Ø {int(gng_df['withdrawalCapacity_median'].mean()*365/10**3)} TWh/a)",  marker=dict(color= rgb_to_hex(FZJcolor.black))))
fig.add_trace(go.Scatter(x=xval, y=gng_df["withdrawal"], name=f"Withdrawl rate (Ø {int(gng_df['withdrawal'].mean()*365/10**3)} TWh/a)", marker=dict(color= rgb_to_hex(FZJcolor.orange))))


fig.update_layout(
    title="Withdrawal of NG",
    yaxis_title= "NG [GWh/d]",
    yaxis=dict(range=[0, 20000]),
    font=dict(
        size=18,
    )
)
col2.plotly_chart(fig, use_container_width=True)
