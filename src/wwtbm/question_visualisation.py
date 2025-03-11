import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_ques_vis(number: int) -> dict:
    index = [question_1, question_2, question_3, question_4]
    return index[number]()


def question_1() -> dict[str, go.Figure]:
    apple_df = pd.read_csv("data/question-dataset/2014_apple_stocks.csv")
    apple_df["AAPL_x"] = pd.to_datetime(apple_df["AAPL_x"])
    fig1 = px.line(apple_df, x="AAPL_x", y="AAPL_y", title="Apple Stock Prices in 2014")
    fig1.update_layout(
        xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        plot_bgcolor="#000066",  # Change the background color of the plot
        paper_bgcolor="#000066",  # Change the background color of the entire figure
        font={"color": "white"},  # Change the font color to white for better visibility
    )
    fig1.update_yaxes(showgrid=True, gridcolor="grey", zeroline=True, zerolinecolor="grey")
    fig1.update_xaxes(showgrid=True, gridcolor="grey", zeroline=True, zerolinecolor="grey")
    fig1.update_traces(line={"color": "yellow"})
    return {"Apple SP": fig1}


def question_3() -> dict[str, go.Figure]:
    milk_df = pd.read_csv("data/question-dataset/monthly-milk-production-pounds.csv")
    milk_df["Month"] = pd.to_datetime(milk_df["Month"])
    milk_df["Year"] = milk_df["Month"].dt.year
    milk_df["Month"] = milk_df["Month"].dt.strftime("%b")

    heatmap_data = milk_df.pivot(index="Year", columns="Month", values="Monthly milk production (pounds per cow)")

    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    heatmap_data = heatmap_data[month_order]
    fig1 = px.imshow(
        heatmap_data,
        labels={"x": "Month", "y": "Year", "color": "Milk Production (lbs)"},
        color_continuous_scale="blues",
    )
    fig1.update_layout(
        title="Monthly Milk Production Heatmap (1962-1975)",
        xaxis_title="Month",
        yaxis_title="Year",
        # xaxis=dict(side="top"),
    )

    fig1.update_layout(
        plot_bgcolor="#000066",  # Change the background color of the plot
        paper_bgcolor="#000066",  # Change the background color of the entire figure
        font={"color": "white"},  # Change the font color to white for better visibility
    )

    return {"Milk Production": fig1}


def question_2() -> dict[str, go.Figure]:
    df = pd.read_csv("data/question-dataset/pigeon_poop_2010_to_present_20250302.csv")
    # Focus on pigeon-related complaints
    pigeon_df = df[df["Complaint Type"].str.contains("Pigeon|Bird|Litter", case=False)]
    pigeon_df["year"] = pd.DatetimeIndex(pigeon_df["Created Date"]).year

    pigeon_df = pigeon_df.sort_values(by="year")

    # Create the map
    fig = px.scatter_map(
        pigeon_df,
        lat="Latitude",
        lon="Longitude",
        color="Borough",
        size_max=15,
        zoom=9,
        height=600,
        # width=1200,
        hover_name="Unique Key",
        hover_data={
            "Complaint Type": True,
            "Created Date": True,
            "Status": True,
            "Latitude": False,
            "Longitude": False,
        },
        title="NYC Pigeon Droppings & Related Complaints Map",
        animation_frame="year",
    )

    # Update the map style
    fig.update_layout(
        mapbox_style="carto-positron",  # A clean, light map style
        legend_title_text="Borough",
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
    )

    fig.update_layout(
        plot_bgcolor="#000066",  # Change the background color of the plot
        paper_bgcolor="#000066",  # Change the background color of the entire figure
        font={"color": "white"},  # Change the font color to white for better visibility
    )

    return {"Pigeon DooDoo": fig}


def question_4() -> dict[str, go.Figure]:
    iris_df = pd.read_csv("data/question-dataset/iris-data.csv")

    # Create the 3D scatter plot
    fig1 = px.scatter_3d(
        iris_df,
        x="sepal length",
        y="petal width",
        z="petal length",
        color="class",
        title="3D Visualization of Iris Data",
    )

    # Update layout for background and grid colors
    fig1.update_layout(
        plot_bgcolor="#000066",  # Background color of the plot
        paper_bgcolor="#000066",  # Background color of the entire figure
        font={"color": "white"},  # Font color to white for visibility
        scene={
            "xaxis": {
                "backgroundcolor": "#000066",  # Match grid background to plot background
                "gridcolor": "grey",  # Keep gridlines grey
                "zerolinecolor": "grey",  # Optional: set zeroline to grey too
            },
            "yaxis": {
                "backgroundcolor": "#000066",  # Match grid background to plot background
                "gridcolor": "grey",  # Keep gridlines grey
                "zerolinecolor": "grey",
            },
            "zaxis": {
                "backgroundcolor": "#000066",  # Match grid background to plot background
                "gridcolor": "grey",  # Keep gridlines grey
                "zerolinecolor": "grey",
            },
        },
    )

    return {"Iris": fig1}


def question_5() -> dict[str, go.Figure]:
    airport_df = pd.read_csv("data/question-dataset/jfk_weather_sample.csv")
    return airport_df.head()
