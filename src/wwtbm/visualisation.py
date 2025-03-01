import plotly.graph_objects as go
import pandas as pd

def get_user_performance_graph(df_answer, top_n=5):
    """
    Creates an interactive stacked bar graph showing correct and incorrect answers per user.
    
    Args:
        df_answer (pd.DataFrame): DataFrame containing user answers with columns 
                                'Name', 'Question', and 'Correct'
        top_n (int, optional): Number of users to display. If None, shows all users.
                              Users are sorted by number of correct answers.
    
    Returns:
        plotly.graph_objects.Figure: Interactive stacked bar chart
    """
    # Group by Name and Correct to get counts
    performance_data = df_answer.groupby(['Name', 'Correct'])['Question'].count().unstack(fill_value=0)
    
    # Rename columns for clarity
    performance_data.columns = ['Incorrect', 'Correct']
    
    # Calculate total questions and sort by correct answers
    performance_data['Total'] = performance_data['Correct'] + performance_data['Incorrect']
    performance_data = performance_data.sort_values('Correct', ascending=False)
    
    # Apply top_n filter if specified
    if top_n is not None:
        performance_data = performance_data.head(top_n)
    
    # Create the stacked bar chart
    fig = go.Figure()
    
    # Add correct answers bar
    fig.add_trace(go.Bar(
        x=performance_data.index,
        y=performance_data['Correct'],
        name='Correct',
        marker_color='#28a745',  # Green color
        hovertemplate="<br>".join([
            "Name: %{x}",
            "Correct Answers: %{y}",
            "Success Rate: %{customdata:.1f}%",
            "<extra></extra>"
        ]),
        customdata=(performance_data['Correct'] / performance_data['Total'] * 100)
    ))
    
    # Add incorrect answers bar
    fig.add_trace(go.Bar(
        x=performance_data.index,
        y=performance_data['Incorrect'],
        name='Incorrect',
        marker_color='#dc3545',  # Red color
        hovertemplate="<br>".join([
            "Name: %{x}",
            "Incorrect Answers: %{y}",
            "Error Rate: %{customdata:.1f}%",
            "<extra></extra>"
        ]),
        customdata=(performance_data['Incorrect'] / performance_data['Total'] * 100)
    ))
    
    # Update layout
    fig.update_layout(
        title='User Performance Overview',
        xaxis_title='User Name',
        yaxis_title='Number of Answers',
        barmode='stack',
        paper_bgcolor="#2a2a2a",
        plot_bgcolor="#2a2a2a",
        font=dict(color="#ffffff"),
        showlegend=True,
        legend=dict(
            bgcolor="#1a1a1a",
            bordercolor="#ffffff",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="#1a1a1a",
            font_size=14
        ),
        margin=dict(t=50, b=50)
    )
    
    # Update axes
    fig.update_xaxes(
        showgrid=False,
        tickangle=45,
        gridcolor='#404040',
        tickfont=dict(size=10)
    )
    
    fig.update_yaxes(
        showgrid=False,
        gridcolor='#404040',
        zeroline=True,
        zerolinecolor='#404040'
    )
    
    return fig

def get_answer_distribution_graph(df, question_number):
    """
    Returns a Plotly graph object showing answer distribution for a specific question.

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
        bargap=0.1,
        paper_bgcolor="#2a2a2a",
        plot_bgcolor="#2a2a2a",
        font=dict(color="#ffffff"),
        margin=dict(t=50, b=50)
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig