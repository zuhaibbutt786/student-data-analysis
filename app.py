import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Load the data
airports_df = pd.read_csv('airports.csv')

# Extract state from the city name
airports_df['STATE'] = airports_df['DISPLAY_AIRPORT_CITY_NAME_FULL'].str.extract(r', ([A-Z]{2})$')

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

# App layout
app.layout = html.Div([
    html.H1("US Airports Data Analysis Dashboard", style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    html.Div([
        html.Div([
            html.H3("Airport Geographic Distribution", style={'textAlign': 'center'}),
            dcc.Graph(id='map-plot'),
        ], className="six columns"),
        
        html.Div([
            html.H3("Top States by Number of Airports", style={'textAlign': 'center'}),
            dcc.Graph(id='state-bar-chart'),
            html.Div([
                html.Label("Number of States to Display:"),
                dcc.Slider(
                    id='state-slider',
                    min=5,
                    max=20,
                    step=1,
                    value=10,
                    marks={i: str(i) for i in range(5, 21, 5)}
                ),
            ], style={'marginTop': '20px'})
        ], className="six columns"),
    ], className="row"),
    
    html.Div([
        html.Div([
            html.H3("Airport Distribution by Latitude", style={'textAlign': 'center'}),
            dcc.Graph(id='latitude-histogram'),
        ], className="six columns"),
        
        html.Div([
            html.H3("Airport Distribution by Longitude", style={'textAlign': 'center'}),
            dcc.Graph(id='longitude-histogram'),
        ], className="six columns"),
    ], className="row", style={'marginTop': '30px'}),
    
    html.Div([
        html.H3("Airport Details", style={'textAlign': 'center'}),
        html.Div(id='airport-details', style={'marginTop': '20px', 'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px'}),
    ], style={'marginTop': '30px'}),
    
], className="container", style={'maxWidth': '1200px'})

# Callbacks
@app.callback(
    Output('map-plot', 'figure'),
    Input('map-plot', 'clickData')
)
def update_map(clickData):
    fig = px.scatter_geo(
        airports_df,
        lat='LATITUDE',
        lon='LONGITUDE',
        hover_name='AIRPORT',
        hover_data=['DISPLAY_AIRPORT_NAME', 'DISPLAY_AIRPORT_CITY_NAME_FULL'],
        color='STATE',
        projection='albers usa',
        title='US Airports Distribution'
    )
    
    fig.update_layout(
        height=500,
        margin={"r":0,"t":30,"l":0,"b":0},
        geo=dict(
            showland=True,
            landcolor="rgb(212, 212, 212)",
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)",
            showlakes=True,
            lakecolor="rgb(255, 255, 255)",
            showsubunits=True,
            showcountries=True,
            showcoastlines=True,
            coastlinecolor="rgb(255, 255, 255)",
        )
    )
    
    return fig

@app.callback(
    Output('state-bar-chart', 'figure'),
    Input('state-slider', 'value')
)
def update_state_chart(n_states):
    state_counts = airports_df['STATE'].value_counts().reset_index()
    state_counts.columns = ['STATE', 'COUNT']
    state_counts = state_counts.head(n_states)
    
    fig = px.bar(
        state_counts,
        x='STATE',
        y='COUNT',
        color='COUNT',
        color_continuous_scale='Viridis',
        title=f'Top {n_states} States by Number of Airports'
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="State",
        yaxis_title="Number of Airports",
        coloraxis_showscale=False
    )
    
    return fig

@app.callback(
    Output('latitude-histogram', 'figure'),
    Input('map-plot', 'clickData')
)
def update_latitude_histogram(clickData):
    fig = px.histogram(
        airports_df,
        x='LATITUDE',
        nbins=20,
        color_discrete_sequence=['#636EFA'],
        title='Airport Distribution by Latitude'
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Latitude",
        yaxis_title="Number of Airports"
    )
    
    return fig

@app.callback(
    Output('longitude-histogram', 'figure'),
    Input('map-plot', 'clickData')
)
def update_longitude_histogram(clickData):
    fig = px.histogram(
        airports_df,
        x='LONGITUDE',
        nbins=20,
        color_discrete_sequence=['#00CC96'],
        title='Airport Distribution by Longitude'
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Longitude",
        yaxis_title="Number of Airports"
    )
    
    return fig

@app.callback(
    Output('airport-details', 'children'),
    Input('map-plot', 'clickData')
)
def display_airport_details(clickData):
    if clickData is None:
        return html.P("Click on an airport in the map to see details")
    
    point_index = clickData['points'][0]['pointIndex']
    airport = airports_df.iloc[point_index]
    
    return [
        html.H4(f"{airport['DISPLAY_AIRPORT_NAME']} ({airport['AIRPORT']})"),
        html.P(f"Location: {airport['DISPLAY_AIRPORT_CITY_NAME_FULL']}"),
        html.P(f"Coordinates: {airport['LATITUDE']:.4f}, {airport['LONGITUDE']:.4f}"),
        html.P(f"State: {airport['STATE']}")
    ]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=12000)