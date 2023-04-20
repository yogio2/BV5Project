import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

df = px.data.gapminder()

app = dash.Dash(__name__)
server = app.server

choro_fig = px.choropleth(
    df,
    locations="iso_alpha",
    hover_name="country",
    hover_data=df.columns,
    color="lifeExp",
    projection="natural earth"
)

scatter_fig = px.scatter(
    df,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    size_max=50,
    log_x=True,
    animation_frame="year",
    animation_group="country",
    range_y=[20, 100],
    color="continent",
    hover_name="country",
    hover_data=df.columns
)

sunburst_fig = px.sunburst(
    df,
    path=["continent", "country"],
    values="pop",
    hover_name="country",
    color="lifeExp"
)

treemap_fig = px.treemap(
    df,
    path=["continent","country"],
    values="pop",
    hover_name="country",
    color="lifeExp"
)


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

dropdown = dcc.Dropdown(
    id="dropdown",
    options=[
        {"label": "Life Expectancy", "value": "lifeExp"},
        {"label": "Population", "value": "pop"},
        {"label": "GDP per Capita", "value": "gdpPercap"}
    ],
    value="lifeExp",
    clearable=False
)

choro_graph = dcc.Graph(
    id="choro-graph",
    figure=choro_fig
)

scatter_button = dbc.Button("Open Scatter Plot", id="scatter-button", color="primary", className="mb-3", outline=True)

scatter_modal = dbc.Modal(
    [
        dbc.ModalHeader("Scatter Plot"),
        dbc.ModalBody(
            dcc.Graph(
                id="scatter-graph",
                figure=scatter_fig
            )
        ),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-button", className="ml-auto")
        )
    ],
    id="scatter-modal",
    size="lg"
)

sunburst_button = dbc.Button("Open Sunburst Plot", id="sunburst-button", color="primary", className="mb3", outline=True, style={"margin-left": "10px"})

sunburst_modal = dbc.Modal(
    [
        dbc.ModalHeader("Sunburst Plot"),
        dbc.ModalBody(
            dcc.Graph(
                id="sunburst-plot",
                figure=sunburst_fig
            )
        ),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-button", className="ml-auto")
        )
    ],
    id="sunburst-modal",
    size="lg"
)

treemap_button = dbc.Button("Open Treemap Plot", id="treemap-button", color="primary", className="mb3", outline=True, style={"margin-left": "10px"})

treemap_modal = dbc.Modal(
    [
        dbc.ModalHeader("Treemap Plot"),
        dbc.ModalBody(
            dcc.Graph(
                id="treemap-plot",
                figure=treemap_fig
            )
        ),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-button", className="ml-auto")
        )
    ],
    id="treemap-modal",
    size="lg"
)

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Business Visaulization Project"),
                html.P("Select a variable to display on the choropleth map:"),
                dropdown,
                choro_graph,
                scatter_button,
                sunburst_button,
                treemap_button,
                scatter_modal,
                sunburst_modal,
                treemap_modal
            ])
        ])
    ])
])

@app.callback(
    dash.dependencies.Output("choro-graph", "figure"),
    [dash.dependencies.Input("dropdown", "value")]
)
def update_choro_graph(value):
    fig = px.choropleth(
        df,
        locations="iso_alpha",
        hover_name="country",
        hover_data=df.columns,
        color=value,
        projection="natural earth",
        height=550
    )
    return fig

@app.callback(
    dash.dependencies.Output("scatter-modal", "is_open"),
    [dash.dependencies.Input("scatter-button", "n_clicks"),
     dash.dependencies.Input("close-button", "n_clicks")],
    [dash.dependencies.State("scatter-modal", "is_open")]
)
def toggle_scatter_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    dash.dependencies.Output("sunburst-modal", "is_open"),
    [dash.dependencies.Input("sunburst-button", "n_clicks"),
     dash.dependencies.Input("close-button", "n_clicks")],
    [dash.dependencies.State("sunburst-modal", "is_open")]
)
def toggle_sunburst_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    dash.dependencies.Output("treemap-modal", "is_open"),
    [dash.dependencies.Input("treemap-button", "n_clicks"),
     dash.dependencies.Input("close-button", "n_clicks")],
    [dash.dependencies.State("treemap-modal", "is_open")]
)
def toggle_treemap_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
