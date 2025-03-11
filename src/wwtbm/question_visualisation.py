"""Data Visualization Module for Quiz Questions.

This module provides functions to generate interactive visualizations for a quiz application.
Each visualization represents a different question in the quiz, drawing from various datasets
to create engaging Plotly charts including line graphs, heatmaps, geographic maps, and 3D plots.

The module uses a factory pattern through the get_ques_vis function to retrieve the appropriate
visualization based on the question number. Each question function returns a dictionary with
a descriptive name as the key and a Plotly figure object as the value.

Dependencies:
    - pandas: For data manipulation and processing
    - plotly.express: For creating expressive, easy-to-use plots
    - plotly.graph_objects: For more customized plotting capabilities

Example usage:
    ```
    # Get visualization for question 1
    apple_stock_viz = get_ques_vis(0)

    # Display the figure
    for name, fig in apple_stock_viz.items():
        fig.show()
    ```
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_ques_vis(number: int) -> dict:
    """Factory function to retrieve the visualization for a specific question.

    Args:
        number (int): Zero-based index of the question (0-3)

    Returns:
        dict: Dictionary with visualization name as key and Plotly figure as value

    Raises:
        IndexError: If question number is out of range
    """
    index = [question_1, question_2, question_3, question_4]
    return index[number]()


def question_1() -> dict[str, go.Figure]:
    """Generate visualization for Question 1: Apple stock price trend in 2014.

    Creates a line chart showing Apple's stock prices throughout 2014
    with a dark blue background and yellow line for contrast.

    Returns:
        dict[str, go.Figure]: Dictionary with 'Apple SP' as key and the line chart as value
    """
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
    """Generate visualization for Question 3: Monthly milk production heatmap (1962-1975).

    Creates a heatmap showing milk production patterns by month and year,
    using a blue color scale on a dark blue background.

    Returns:
        dict[str, go.Figure]: Dictionary with 'Milk Production' as key and the heatmap as value
    """
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
    """Generate visualization for Question 2: NYC pigeon-related complaints map.

    Creates an animated scatter map showing the locations of pigeon-related complaints
    in NYC from 2010 to present, with animation by year and color-coding by borough.

    Returns:
        dict[str, go.Figure]: Dictionary with 'Pigeon DooDoo' as key and the map as value
    """
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
    """Generate visualization for Question 4: 3D visualization of Iris dataset.

    Creates a 3D scatter plot showing the relationship between sepal length,
    petal width, and petal length in the Iris dataset, color-coded by species class.

    Returns:
        dict[str, go.Figure]: Dictionary with 'Iris' as key and the 3D scatter plot as value
    """
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
    """Generate visualization for Question 5: JFK airport weather data.

    This function appears to be incomplete or for testing purposes.
    Currently, it only returns the first few rows of a weather dataset.

    Returns:
        pandas.DataFrame: First 5 rows of the JFK weather dataset
    """
    airport_df = pd.read_csv("data/question-dataset/jfk_weather_sample.csv")
    return airport_df.head()
