import streamlit as st
import pandas as pd
import plotly.express as px


# Page Configuration
st.set_page_config(
    page_title="India Housing Price Analysis",
    page_icon="🏠",
    layout="wide"
)

# Dashboard Header

st.title("India Housing Price Analysis")

st.markdown(
"""
### Welcome to India Housing Analytics Dashboard

```
This interactive dashboard provides insights into housing prices across different states, cities, property types and other features in India.

Technologies Used: Python, Pandas, Plotly, and Streamlit 
"""

)

st.divider()

# Load Dataset
df = pd.read_csv("data/india_housing_prices_cleaned.csv")

# Display Dataset
st.subheader("Housing Dataset")
st.dataframe(df.head(10))


# Dynamic Filters Section

st.subheader("Filter Housing Data")

col1, col2 = st.columns(2)

# State Filter
with col1:
    selected_state = st.selectbox(
        "Select State",
        ["All"] + sorted(df["State"].unique().tolist())
    )

# Filter data according to selected state
if selected_state == "All":
    state_filtered_df = df.copy()
else:
    state_filtered_df = df[df["State"] == selected_state]

# Property Type Filter
with col2:
    available_properties = sorted(
        state_filtered_df["Property_Type"].unique().tolist()
    )

    selected_property = st.selectbox(
        "Select Property Type",
        ["All"] + available_properties
    )

# Apply Property Type Filter
if selected_property != "All":
    filtered_df = state_filtered_df[
        state_filtered_df["Property_Type"] == selected_property
    ]
else:
    filtered_df = state_filtered_df.copy()


# Dynamic KPI Cards

st.subheader("Housing Market Overview")

col1, col2, col3, col4 = st.columns(4)

total_properties = len(filtered_df)
average_price = filtered_df["Price_in_Lakhs"].mean()
maximum_price = filtered_df["Price_in_Lakhs"].max()
minimum_price = filtered_df["Price_in_Lakhs"].min()

with col1:
    st.metric(
label="Total Properties",
value=f"{total_properties:,}"
)

with col2:
    st.metric(
label="Average Price",
value=f"₹{average_price:.2f} Lakhs"
)

with col3:
    st.metric(
label="Maximum Price",
value=f"₹{maximum_price:.2f} Lakhs"
)

with col4:
    st.metric(
label="Minimum Price",
value=f"₹{minimum_price:.2f} Lakhs"
)

st.divider()

# Charts

# Chart 1: State-wise Average Property Price

st.subheader("State-wise Average Property Price")

state_avg_price = (
filtered_df.groupby("State")["Price_in_Lakhs"]
.mean()
.sort_values(ascending=True)
.reset_index()
)

fig = px.bar(
state_avg_price,
x="Price_in_Lakhs",
y="State",
orientation="h",
text_auto=".2f",
title="Average Property Price by State",
labels={
"Price_in_Lakhs": "Average Price (Lakhs)",
"State": "State"
},
color_discrete_sequence=["#00A6A6"]
)

fig.update_traces(
textposition="outside",
hovertemplate="<b>%{y}</b><br>Average Price: ₹%{x:.2f} Lakhs<extra></extra>"
)

fig.update_layout(
template="plotly_white",
height=550,
title_x=0.5,
title_font_size=20,
font=dict(family="Arial", size=12),
margin=dict(l=20, r=70, t=70, b=40),
showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Chart 2: City-wise Average Property Price

st.subheader("City-wise Average Property Price")

city_avg_price = (
filtered_df.groupby("City")["Price_in_Lakhs"]
.mean()
.sort_values(ascending=True)
.reset_index()
)

fig = px.bar(
city_avg_price,
x="Price_in_Lakhs",
y="City",
text_auto = ".2f",
orientation="h",
title="Average Property Price by City",
labels={
"Price_in_Lakhs": "Average Price (Lakhs)",
"City": "City"
},
color_discrete_sequence=["#00A6A6"]
)

fig.update_traces(
textposition="outside",
hovertemplate="<b>%{y}</b><br>Average Price: ₹%{x:.2f} Lakhs<extra></extra>"
)

fig.update_layout(
template="plotly_white",
height=max(750, len(city_avg_price) * 25),
title_x=0.5,
title_font_size=22,
font=dict(family="Arial", size=14),
margin=dict(l=30, r=100, t=80, b=50),
showlegend=False
)

st.plotly_chart(fig, use_container_width=True)


# Chart 3: Property Type Distribution

st.subheader("Property Type Distribution")

property_counts = filtered_df["Property_Type"].value_counts().reset_index()
property_counts.columns = ["Property_Type", "Count"]

fig = px.pie(
    property_counts,
    names="Property_Type",
    values="Count",
    title="Distribution of Property Types",
    color_discrete_sequence=["#00A6A6", "#17365D", "#F4B183"],
    hole=0.35
)

fig.update_traces(
    textposition="inside",
    textinfo="label+percent",
    insidetextfont=dict(size=14, color="white"),
    hovertemplate="<b>%{label}</b><br>Properties: %{value:,}<br>Share: %{percent}<extra></extra>"
)

fig.update_layout(
    template="plotly_white",
    height=450,
    title_x=0.5,
    title_font_size=20,
    font=dict(family="Arial", size=12),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Chart 4: BHK Distribution

st.subheader("🛏️ BHK Distribution")

bhk_counts = (
    filtered_df["BHK"]
    .value_counts()
    .sort_index()
    .reset_index()
)

bhk_counts.columns = ["BHK", "Count"]

fig = px.bar(
    bhk_counts,
    x="BHK",
    y="Count",
    title="Number of Properties by BHK",
    labels={
        "BHK": "Number of Bedrooms (BHK)",
        "Count": "Number of Properties"
    },
    color_discrete_sequence=["#00A6A6"]
)

fig.update_traces(
    hovertemplate="<b>%{x} BHK</b><br>Properties: %{y:,}<extra></extra>"
)

fig.update_layout(
    template="plotly_white",
    height=400,
    title_x=0.5,
    title_font_size=20,
    font=dict(family="Arial", size=12),
    margin=dict(l=40, r=40, t=70, b=50),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Chart 5: Average Property Price by BHK

st.subheader("Average Property Price by BHK")

avg_price_bhk = (
filtered_df.groupby("BHK")["Price_in_Lakhs"]
.mean()
.sort_index()
.reset_index()
)

fig = px.bar(
avg_price_bhk,
x="BHK",
y="Price_in_Lakhs",
title="Average Property Price for Each BHK",
labels={
"BHK": "Number of Bedrooms (BHK)",
"Price_in_Lakhs": "Average Price (Lakhs)"
},
color_discrete_sequence=["#00A6A6"]
)

fig.update_traces(
textposition="outside",
hovertemplate="<b>%{x} BHK</b><br>Average Price: ₹%{y:.2f} Lakhs<extra></extra>"
)

fig.update_layout(
template="plotly_white",
height=420,
title_x=0.5,
title_font_size=20,
font=dict(family="Arial", size=12),
margin=dict(l=40, r=40, t=70, b=50),
showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# chart 6: Furnishing Status Distribution

st.subheader("Furnishing Status Distribution")

furnishing_counts = filtered_df["Furnished_Status"].value_counts()

fig = px.pie(
    names=furnishing_counts.index,
    values=furnishing_counts.values,
    title="Distribution of Furnishing Status",
    color_discrete_sequence=["#00A6A6", "#17365D", "#F4B183"],
    hole=0.35
)

fig.update_traces(
    textposition="inside",
    textinfo="label+percent",
    insidetextfont=dict(size=14, color="white"),
    hovertemplate=(
        "<b>%{label}</b><br>"
        "Properties: %{value:,}<br>"
        "Share: %{percent}"
        "<extra></extra>"
    )
)

fig.update_layout(
    template="plotly_white",
    height=450,
    title_x=0.5,
    title_font_size=20,
    font=dict(family="Arial", size=12),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Chart 7: Property Size vs Price

st.subheader("Property Size vs Price")

fig = px.scatter(
    filtered_df,
    x="Size_in_SqFt",
    y="Price_in_Lakhs",
    title="Relationship Between Property Size and Price",
    labels={
        "Size_in_SqFt": "Property Size (Sq. Ft.)",
        "Price_in_Lakhs": "Property Price (Lakhs)"
    },
    color_discrete_sequence=["#00A6A6"],
    opacity=0.6
)

fig.update_traces(
    marker=dict(
        size=3,
        opacity=0.25
    ),
    hovertemplate=(
        "<b>Property Details</b><br>"
        "Size: %{x} Sq. Ft.<br>"
        "Price: ₹%{y:.2f} Lakhs"
        "<extra></extra>"
    )
)

fig.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.5,
    title_font_size=20,
    font=dict(family="Arial", size=12),
    margin=dict(l=50, r=40, t=70, b=50),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)


# Chart 8: Average Property Price by Property Age

st.subheader("Average Property Price by Property Age")

age_price = (
    filtered_df.groupby("Age_of_Property")["Price_in_Lakhs"]
    .mean()
    .reset_index()
    .sort_values("Age_of_Property")
)

fig = px.bar(
    age_price,
    x="Age_of_Property",
    y="Price_in_Lakhs",
    title="Average Property Price by Age",
    labels={
        "Age_of_Property": "Property Age (Years)",
        "Price_in_Lakhs": "Average Price (Lakhs)"
    },
    color_discrete_sequence=["#00A6A6"]
)

fig.update_traces(
    textposition="outside",
    hovertemplate=(
        "Property Age: %{x} Years<br>"
        "Average Price: ₹%{y:.2f} Lakhs"
        "<extra></extra>"
    )
)

fig.update_layout(
    template="plotly_white",
    height=450,
    title_x=0.5,
    title_font_size=20,
    font=dict(family="Arial", size=12),
    margin=dict(l=50, r=40, t=70, b=50),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Display Filtered Data

st.subheader("Filtered Housing Data")

st.write("Total Filtered Properties:", len(filtered_df))

st.dataframe(filtered_df.head(10))    


