import dash
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import plotly.io as pio

pio.templates.default = "plotly_dark"

df = pd.read_csv("../uber_trips_cleaned.csv")
df['weekday'] = pd.Categorical(df['weekday'],
                               categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
                                           'Sunday'], ordered=True)

# Hour dropdown options
option_list = []
for number in range(0, 24):
    dict = {'label': f"{number}", 'value': number}
    option_list.append(dict)

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.Div(
                                     className="user-input",
                                     children=[html.H1('NYC Uber Trips Analysis',
                                                         style={#'display': 'block',
                                                                'textAlign': 'center',
                                                                'color': "#6FA4CE",
                                                                'font-size': 40,
                                                                'font-family': "Open Sans",
                                                                'font-weight': 'bold',
                                                               }
                                                      ),

                                              html.Br(),
                                              html.P("Select a month:", style={'font-size': 20, 'color': "white"}),

                                              dcc.Dropdown(id='month-dropdown', options=[
                                                  {'label': 'April', 'value': 4},
                                                  {'label': 'May', 'value': 5},
                                                  {'label': 'June', 'value': 6},
                                                  {'label': 'July', 'value': 7},
                                                  {'label': 'August', 'value': 8},
                                                  {'label': 'September', 'value': 9},
                                                                                        ],
                                                                               value=4,
                                                                               placeholder="Select a Month here",
                                                                               searchable=True,

                                                          ),

                                              html.Br(),
                                              html.P("Select a day of the week:", style={'font-size': 20, 'color': "white"}),

                                              dcc.Dropdown(id='weekday-dropdown', options=[
                                                                  {'label': 'Monday', 'value': "Monday"},
                                                                  {'label': 'Tuesday', 'value': 'Tuesday'},
                                                                  {'label': 'Wednesday', 'value': 'Wednesday'},
                                                                  {'label': 'Thursday', 'value': 'Thursday'},
                                                                  {'label': 'Friday', 'value': 'Friday'},
                                                                  {'label': 'Saturday', 'value': 'Saturday'},
                                                                  {'label': 'Sunday', 'value': 'Sunday'}
                                                                                         ],
                                                                                   value="Monday",
                                                                                   placeholder="Select a Weekday here",
                                                                                   searchable=True
                                                           ),

                                              html.Br(),
                                              html.P("Select a base:", style={'font-size': 20, 'color': "white"}),

                                              dcc.Dropdown(id='base-dropdown', options=[
                                                                  {'label': 'Unter', 'value': 'Unter'},
                                                                  {'label': 'Hinter', 'value': 'Hinter'},
                                                                  {'label': 'Weiter', 'value': 'Weiter'},
                                                                  {'label': 'Schmecken', 'value': 'Schmecken'},
                                                                  {'label': 'Danach-NY', 'value': 'Danach-NY'},
                                                                                       ],
                                                                              value="Unter",
                                                                              placeholder="Select a Base here",
                                                                              searchable=True
                                                          ),

                                              html.Br(),
                                              html.P("Select an hour:", style={'font-size': 20, 'color': "white"}),

                                              dcc.Dropdown(id='hour-dropdown', options=option_list,
                                                                               value=0,
                                                                               placeholder="Select an Hour here",
                                                                               searchable=True
                                                          )
                                              ],
                                     style={'textAlign': 'left',
                                            'color': "#503D36",
                                            'padding-left': 20,
                                            'padding-right': 20,
                                            'padding-top': 60}
                                         ),
                                html.Div(
                                     className="graphs",
                                     children=[html.Div(className="first_row",
                                                        children=[html.Div(dcc.Graph(id='weekdays-bar-chart')),

                                                                  html.Div(dcc.Graph(id='hours-histogram')),],
                                                        style={}
                                                        ),
                                               html.Div(className="second_row",
                                                        children=[html.Div(dcc.Graph(id='rush-hour-line-chart')),

                                                                  html.Div(dcc.Graph(id='map')),],
                                                        style={}
                                                        )
                                               ],
                                     style={'display': 'flex',
                                            'flex-direction': 'row'}
                                         )
                               ],
                    style={'display': 'flex',
                           'flex-direction': 'row',
                           'background-color': '#262926',
                           'margin': 0,
                           #'padding': 0,
                           #'height': 100%,
                           #'width': 100%,
                           }
                   )


@app.callback(Output(component_id='weekdays-bar-chart', component_property='figure'),
              Input(component_id='month-dropdown', component_property='value'))
def weekdays_by_month(month):
    df_month = df[df.month == month]
    bar = px.bar(x=df_month['weekday'].value_counts().index,
                 y=df_month['weekday'].value_counts().values,
                 title="Number of rides for days of the week",
                 labels={"x": "Day of the week", "y": "Counts"},
                 color_discrete_sequence=["#56DC65"])

    bar.update_layout(width=600,
                      height=400,
                      title_font_size=20,
                      plot_bgcolor='#262926',
                      paper_bgcolor='#262926')

    bar.update_xaxes(title_font_size=17)

    bar.update_yaxes(title_font_size=17)
    return bar


@app.callback(Output(component_id='hours-histogram', component_property='figure'),
              Input(component_id='weekday-dropdown', component_property='value'))
def hours_by_weekday(weekday):
    df_day = df[df.weekday == weekday]
    hist = px.histogram(x=df_day.hour,
                        color_discrete_sequence=["#56DC65"])

    hist.update_layout(title_text="Distribution of rides by hour of the day",
                       width=600,
                       height=400,
                       title_font_size=20,
                       showlegend=False,
                       plot_bgcolor='#262926',
                       paper_bgcolor='#262926'
                       )

    hist.update_xaxes(title="Hour",
                      tickmode="linear")

    hist.update_yaxes(title="Counts")
    return hist


@app.callback(Output(component_id='rush-hour-line-chart', component_property='figure'),
              Input(component_id='month-dropdown', component_property='value'))
def rush_by_w_by_m(month):
    df_month = df[df.month == month]
    rush_by_weekday = df_month.groupby(["weekday", "hour"]).day.count().reset_index()
    rush_by_weekday.rename(columns={"day": "count"}, inplace=True)
    rush = px.line(rush_by_weekday,
                   x="hour",
                   y="count",
                   color_discrete_sequence=["#C1F4C6", "#95EA9E", "#25C636", "#11621A", "#188924", "#57779D",
                                            "#83AAD7"],
                   color="weekday",
                   markers=True)

    rush.update_layout(title="Rush hours by weekday",
                       margin_t=100,
                       xaxis_title="Hour",
                       yaxis_title="Counts",
                       width=600,
                       height=400,
                       title_font_size=20,
                       plot_bgcolor='#262926',
                       paper_bgcolor='#262926'
                       )

    rush.update_yaxes(title_font_size=17)

    rush.update_xaxes(title_font_size=17)

    return rush


@app.callback(Output(component_id='map', component_property='figure'),
              [Input(component_id='base-dropdown', component_property='value'),
               Input(component_id='hour-dropdown', component_property='value'),
               Input(component_id='weekday-dropdown', component_property='value')])
def plot_map(base, hour, weekday):
    mask1 = df['Base'] == base
    mask2 = df['hour'] == hour
    mask3 = df["weekday"] == weekday
    df_out = df[mask1 & mask2 & mask3]
    api_token = "pk.eyJ1IjoibWlya2FqZXppayIsImEiOiJja3kwaTVpZHMwMXhqMm9vNmttNDhzNTNzIn0.IhRtFpw8vQwMF1E-Bgq8lA"
    map_rush = px.scatter_mapbox(df_out, lat="Lat", lon="Lon", opacity=0.2,
                                 color_discrete_sequence=["#56DC65"], zoom=10)
    map_rush.update_layout(title="Occupancy of base by hour and weekday",
                           mapbox_accesstoken=api_token,
                           width=600,
                           height=400,
                           title_font_size=20,
                           plot_bgcolor='#262926',
                           paper_bgcolor='#262926'
                           )
    return map_rush


if __name__ == '__main__':
    app.run_server()
