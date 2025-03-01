import pandas as pd
import plotly.express as px
apple_df = pd.read_csv("data/question-dataset/2014_apple_stocks.csv")
us_city_df = pd.read_csv("data/question-dataset/2014_us_cities.csv")
coffee_df = pd.read_csv("data/question-dataset/simplified_coffee.csv")
iris_df = pd.read_csv("data/question-dataset/iris-data.csv")
airport_df = pd.read_csv("data/question-dataset/jfk_weather_sample.csv")
milk_df = pd.read_csv("data/question-dataset/monthly-milk-production-pounds.csv")

def Q1():
    apple_df['AAPL_x'] = pd.to_datetime(apple_df['AAPL_x'])
    fig1 = px.line(apple_df, x='AAPL_x', y='AAPL_y', title='Apple Stock Prices in 2014')
    return fig1

def Q2():
    milk_df['Month'] = pd.to_datetime(milk_df['Month'])
    milk_df["Year"] = milk_df["Month"].dt.year
    milk_df["Month"] = milk_df["Month"].dt.strftime("%b") 

    heatmap_data = milk_df.pivot(index="Year", columns="Month", values="Monthly milk production (pounds per cow)")

    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    heatmap_data = heatmap_data[month_order]
    fig1 = px.imshow(
        heatmap_data,
        labels={"x": "Month", "y": "Year", "color": "Milk Production (lbs)"},
        color_continuous_scale="blues"
    )   
    fig1.update_layout(
        title="Monthly Milk Production Heatmap (1962-1975)",
        xaxis_title="Month",
        yaxis_title="Year",
        xaxis=dict(side="top")
    )

    return fig1

def Q3():
    coffee_df1 = coffee_df[['origin','roast']]
    grouped_counts = coffee_df1.groupby(["origin", "roast"]).size().reset_index(name='count')
    # df_dominant = grouped_counts.loc[grouped_counts.groupby("origin")["count"].idxmax()]
    print(grouped_counts['origin'].unique)
    # Create a choropleth map
    fig1 = px.scatter_geo(
        grouped_counts,
        locations="origin",
        locationmode="country names",
        color="roast",  # Different colors for roast types
        size="count",  # Size of bubbles based on count
        hover_name="origin",
        hover_data={"roast": True, "count": True},
        title="Coffee Roast Types by Country",
        projection="orthographic",  # Change projection as needed
        color_discrete_map={
            "Light": "yellow",
            "Medium-Light": "orange",
            "Medium": "brown",
            "Dark": "black"
        },
        size_max=50 
    )
    fig1.update_layout(
    geo=dict(
        showcoastlines=True,   # Show coastlines
        showland=True,         # Show land areas
        landcolor="rgb(217, 217, 217)",  # Light gray for land
        showframe=True,        # Show map borders
        showcountries=True,    # Show country borders
        countrycolor="black"   # Make country borders black
    )
)
    return fig1
def Q4():

    fig1 = px.scatter_3d(iris_df, x="sepal length", y="petal width", z="petal length", 
                    color="class", title="3D Visualization of Iris Data")
    return fig1

def Q5():

    return airport_df.head()

def Q6():
    fig1 = px.line(apple_df, x='AAPL_x', y='AAPL_y', title='Apple Stock Prices in 2014')
    return fig1

# fig = Q5()
# # fig.show()
# print(fig)