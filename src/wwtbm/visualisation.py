import plotly.graph_objects as go
# df_question,df_answer = get_data()  # Call get_data() to get the DataFrame



def get_answer_distribution_graph(filtered_df, question_number):
    """
    Returns a Plotly graph object showing answer distribution for a specific question.

    Args:
        filtered_df (pd.DataFrame): Filtered DataFrame with first occurrences.
        question_number (int): The question number to visualize.

    Returns:
        plotly.graph_objects.Figure: The Plotly figure object for the given question.
    """
    # Filter DataFrame for the specific question
    df_question = filtered_df[filtered_df["Question"] == question_number]

    # Create the histogram
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=df_question["Answer"],
            name=f"Question {question_number}",
            marker=dict(line=dict(width=1, color="black")),
            nbinsx=4  # Ensure we have exactly 4 bins (for answers 1, 2, 3, 4)
        )
    )

    # Update layout
    fig.update_layout(
        title=f"Answer Distribution for Question {question_number}",
        xaxis_title="Selected Answer",
        yaxis_title="Count",
        xaxis=dict(
            tickmode="array",
            tickvals=[1, 2, 3, 4],  # Ensure only 1, 2, 3, 4 appear
            ticktext=["Option 1", "Option 2", "Option 3", "Option 4"],
            dtick=1
        ),
        bargap=0.1
    )

    return fig



# fig = get_answer_distribution_graph(df_answer, 2)
# fig.show()