# kaggle data link: https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires/data

from wildfires_api import WildfireAPI
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


def main():
    api = WildfireAPI()
    api.connect("FPA_FOD_20170508.sqlite")

    app = Dash(__name__)

    app.layout = html.Div([
        html.Div(
            html.H1("W I L D  F I R E S"),
            style={'text-align': 'center'}
        ),

        html.Div(
            html.H4('Wildfire Interactive Dashboard'),
            style={'text-align': 'center'}
        ),

        # Bar graph for fire causes
        dcc.Graph(id="bar-graph", style={'width': '50%', 'height': '90vh', 'display': 'inline-block'}),

        # Line plot graph for fire size vs. year
        dcc.Graph(id="scatter-plot", style={'width': '50%', 'height': '90vh', 'display': 'inline-block'}),

        # Dropdown for selecting state
        html.P("Select State:"),
        dcc.Dropdown(id='state', options=api.get_state_list(), value="AL"),

        # Range slider for selecting year range
        html.P("Select Year Range:"),
        dcc.RangeSlider(
            id='year-range',
            min=1992,
            max=2015,
            step=1,
            marks={year: str(year) for year in range(1992, 2016)},
            value=[1992, 2015]
        )
    ])

    @app.callback(
        Output("bar-graph", "figure"),
        [Input("state", "value")]
    )
    def display_bar(state):
        if state:
            causes = api.get_cause_list()
            counts = api.get_cause_count(state)
            color_scale = [[0, 'yellow'], [1, 'red']]
            colors = [int(count) / max(counts) for count in counts]
            data = [{
                'x': causes,
                'y': counts,
                'type': 'bar',
                'hoverinfo': 'text',
                'text': [f'State: {state}<br>Cause: {cause}<br>Count: {count}' for cause, count in zip(causes, counts)],
                'marker': {'color': colors, 'colorscale': color_scale}
            }]
            fig = {
                'data': data,
                'layout': {'title': 'Fire Causes Count for {}'.format(state)}
            }
            return fig
        else:
            return {}

    @app.callback(
        Output("scatter-plot", "figure"),
        [Input("state", "value"),
         Input("year-range", "value")]
    )
    def display_line_plot(state, year_range):
        if state:
            fire_data = api.get_fire_data_by_state(state, year_range)
            counts_per_year = fire_data.groupby('FIRE_YEAR').size().reset_index(name='count')

            fig = px.line(counts_per_year, x='FIRE_YEAR', y='count', title=f'Number of Fires per Year in {state}')
            fig.update_xaxes(title_text='Year')
            fig.update_yaxes(title_text='Number of Fires')
            return fig
        else:
            return {}

    # run it!
    app.run(debug=True)


main()