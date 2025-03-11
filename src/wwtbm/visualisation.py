"""Quiz Performance Visualization Module.

This module provides functions for creating interactive visualizations of user performance on quizzes or assessments.
It uses Plotly to generate interactive graphics that help analyze how users performed on multiple-choice questions.

The module contains two main visualization functions:
- get_user_performance_graph: Creates a stacked bar chart showing correct vs. incorrect answers for each user
- get_answer_distribution_graph: Creates a histogram showing the distribution of selected answers for a specific question

Both functions return Plotly Figure objects that can be displayed in web applications or notebooks.

Dependencies:
    - pandas: For data manipulation
    - plotly.graph_objects: For creating interactive visualizations

Example usage:
    ```
    import pandas as pd

    # Sample data
    data = {
        "Name": ["Alice", "Bob", "Alice", "Charlie", "Bob"],
        "Question": [1, 1, 2, 1, 2],
        "Answer": [1, 2, 3, 1, 4],
        "Correct": [True, False, True, True, True],
    }

    df = pd.DataFrame(data)

    # Generate user performance graph
    performance_fig = get_user_performance_graph(df, top_n=3)
    performance_fig.show()

    # Generate answer distribution for question 1
    distribution_fig = get_answer_distribution_graph(df, question_number=1)
    distribution_fig.show()
    ```
"""

import pandas as pd
import plotly.graph_objects as go


def get_user_performance_graph(df_answer: pd.DataFrame, top_n: int = 5) -> go.Figure:
    """Creates an interactive stacked bar graph showing correct and incorrect answers per user.

    Args:
        df_answer (pd.DataFrame): DataFrame containing user answers with columns
                                'Name', 'Question', and 'Correct'
        top_n (int, optional): Number of users to display. If None, shows all users.
                              Users are sorted by number of correct answers.

    Returns:
        plotly.graph_objects.Figure: Interactive stacked bar chart
    """
    # Group by Name and Correct to get counts
    performance_data = df_answer.groupby(["Name", "Correct"])["Question"].count().unstack(fill_value=0)

    # Rename columns for clarity
    performance_data.columns = ["Incorrect", "Correct"]

    # Calculate total questions and sort by correct answers
    performance_data["Total"] = performance_data["Correct"] + performance_data["Incorrect"]
    performance_data = performance_data.sort_values("Correct", ascending=False)

    # Apply top_n filter if specified
    if top_n is not None:
        performance_data = performance_data.head(top_n)

    # Create the stacked bar chart
    fig = go.Figure()

    # Add correct answers bar
    fig.add_trace(
        go.Bar(
            x=performance_data.index,
            y=performance_data["Correct"],
            name="Correct",
            marker_color="#FFFFFF",  # Green color
            marker_line_width=0,
            hovertemplate="<br>".join(
                ["Name: %{x}", "Correct Answers: %{y}", "Success Rate: %{customdata:.1f}%", "<extra></extra>"],
            ),
            customdata=(performance_data["Correct"] / performance_data["Total"] * 100),
        ),
    )

    # Add incorrect answers bar
    fig.add_trace(
        go.Bar(
            x=performance_data.index,
            y=performance_data["Incorrect"],
            marker_line_width=0,
            name="Incorrect",
            marker_color="#000099",  # Red color
            hovertemplate="<br>".join(
                ["Name: %{x}", "Incorrect Answers: %{y}", "Error Rate: %{customdata:.1f}%", "<extra></extra>"],
            ),
            customdata=(performance_data["Incorrect"] / performance_data["Total"] * 100),
        ),
    )

    # Update layout
    fig.update_layout(
        # xaxis_title="User Name",
        # yaxis_title="Number of Answers",
        barmode="stack",
        paper_bgcolor="#2a2a2a",
        plot_bgcolor="#2a2a2a",
        font={"color": "#ffffff"},
        showlegend=True,
        legend={
            "orientation": "h",  # Horizontal legend
            "yanchor": "bottom",
            "y": -0.15,  # Position below the plot
            "xanchor": "center",
            "x": 0.5,  # Center horizontally
            "bgcolor": "#00003B",
            "bordercolor": "grey",
            "borderwidth": 1,
        },
        hoverlabel=dict(bgcolor="#00003B", font_size=14),
        margin=dict(l=0, r=0, b=0, t=0),
    )

    # Update axes
    fig.update_xaxes(showgrid=False, tickfont={"size": 10})

    fig.update_yaxes(showgrid=True, gridcolor="grey", zeroline=True, zerolinecolor="grey")

    return fig


def get_answer_distribution_graph(df: pd.DataFrame, question_number: int) -> go.Figure:
    """Returns a Plotly graph object showing answer distribution for a specific question.

    Args:
        filtered_df (pd.DataFrame): Filtered DataFrame with first occurrences.
        question_number (int): The question number to visualize.

    Returns:
        plotly.graph_objects.Figure: The Plotly figure object for the given question.
    """
    # Filter DataFrame for the specific question

    df_question = df[df["Question"] == question_number]

    # Create the histogram
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=df_question["Answer"],
            name=f"Question {question_number}",
            marker={"line": {"width": 1, "color": "black"}},
            nbinsx=4,  # Ensure we have exactly 4 bins (for answers 1, 2, 3, 4)
        ),
    )

    # Update layout
    fig.update_layout(
        title=f"Answer Distribution for Question {question_number}",
        xaxis_title="Selected Answer",
        yaxis_title="Count",
        xaxis={
            "tickmode": "array",
            "tickvals": [1, 2, 3, 4],  # Ensure only 1, 2, 3, 4 appear
            "ticktext": ["A", "B", "C", "D"],
            "dtick": 1,
        },
        bargap=0.1,
        paper_bgcolor="#2a2a2a",
        plot_bgcolor="#2a2a2a",
        font={"color": "#ffffff"},
        margin={"t": 50, "b": 50},
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig
