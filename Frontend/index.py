import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import datetime as datetime
from wordcloud import WordCloud
import base64
from io import BytesIO
from collections import Counter
#from profanity_filter import ProfanityFilter
#import spacy
import time

# Read in csv files
ssh_data = pd.read_csv("/home/ubuntu/frontend/csv/Aggregate/sshAgg.csv")
telnet_data = pd.read_csv("/home/ubuntu/frontend/csv/Aggregate/telnetAgg.csv")
http_data = pd.read_csv("/home/ubuntu/frontend/csv/Aggregate/httpAgg.csv")
https_data = pd.read_csv("/home/ubuntu/frontend/csv/Aggregate/httpsAgg.csv")

ssh_sum = pd.read_csv("/home/ubuntu/frontend/csv/Summary/sshSum.csv")
telnet_sum = pd.read_csv("/home/ubuntu/frontend/csv/Summary/telnetSum.csv")
http_sum = pd.read_csv("/home/ubuntu/frontend/csv/Summary/httpSum.csv")
https_sum = pd.read_csv("/home/ubuntu/frontend/csv/Summary/httpsSum.csv")

# fill nan values with 'Not available'
ssh_data['province'] = ssh_data['province'].fillna('Not available')
telnet_data['province'] = telnet_data['province'].fillna('Not available')
http_data['province'] = http_data['province'].fillna('Not available')
https_data['province'] = https_data['province'].fillna('Not available')

# Wordcloud pre-processing
dfm = ssh_data['usernames'].append(ssh_data['passwords'])
dfm = dfm.dropna()
dfm = dfm.values.tolist()
# pf = ProfanityFilter()
# spacy.load('en')
# dfm_filtered = []
# for value in dfm:
#     filtered = pf.censor(value)
#     dfm_filtered.append(filtered)

dfm = Counter(dfm)
data = {
    "word": list(dfm.keys()),
    "count": list(dfm.values())
}
wordFreq = pd.DataFrame(data)
wordFreq = wordFreq.sort_values(by=['count'], ascending=False)

# data required for creating nice graphs
blank = pd.read_csv("/home/ubuntu/frontend/csv/blank.csv")
blank2 = pd.read_csv("/home/ubuntu/frontend/csv/blank2.csv")
honeypots =['SSH', 'Telnet', 'HTTP', 'HTTPS', 'SSH_secure', 'Telnet_secure', 'HTTP_secure', 'HTTPS_secure']
weekdays = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

app = dash.Dash(__name__, )

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('UofG_logo.png'),
                     id = 'UofG_logo',
                     style={'height': '125px',
                            'width': 'auto',
                            'margin-bottom': '25px'})

        ], className='one-third column'),

        html.Div([
            html.Div([
                html.H3('UofG MSc IT+ - Honeypot Project Dashboard', style={'margin-bottom': '0px', 'color': 'white'}),
                html.H5('GUID: 2591168o', style={'margin-bottom': '0px', 'color': 'white'})
            ])
        ], className='one-half column', id = 'title'),

        html.Div([
            html.H6('Dashboard last updated: ' + str(datetime.datetime.strptime(ssh_data['timestamp'].iloc[-1], '%Y-%m-%d %H:%M:%S.%f').strftime("%B %d, %Y at %H:%M (BST)")),
                    style={'color': 'orange'})

        ], className='one-third column', id = 'title1')

    ], id = 'header', className = 'row flex-display', style={'margin-bottom': '25px'}),

# Second row
    html.Div([
        html.Div([
            html.H5('Honeypot mimics vulnerable IoT device', style={'margin-bottom': '0px', 'color': '#99CCFF'})
        ])
    ], className='two-third column'),

# Third row of the dashboard app VULNERABLE HONEYPOT***
    #Third row first column
    html.Div([
        html.Div([
            html.H6(children='Total SSH connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{ssh_sum['# connections'].sum(): .0f}",  #paragraph
                   style={'textAlign': 'center',
                    'color': '#dd1e35',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Third row second column
html.Div([
            html.H6(children='Total Telnet connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{telnet_sum['# connections'].sum()}", #paragraph
                   style={'textAlign': 'center',
                    'color': 'orange',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Third row third column
html.Div([
            html.H6(children='Total HTTP connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{http_sum['# connections'].sum()}", #paragraph
                   style={'textAlign': 'center',
                    'color': 'yellow',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Third row fourth column
html.Div([
            html.H6(children='Total HTTPS connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{https_sum['# connections'].sum()}", #paragraph
                   style={'textAlign': 'center',
                    'color': '#66ff66',
                          'fontSize': 30}
                   )
        ],
    className='card_container three columns')

    ], className='row flex display'),

# Fourth row of the dashboard app
html.Div([
        html.Div([
            html.H5('Honeypot mimics IoT device with security features', style={'margin-bottom': '0px', 'color': '#99CCFF'})
        ])
    ], className='two-third column'),

# Fifth row of the dashboard app SECURE HONEYPOT***
    #Second row first column
    html.Div([
        html.Div([
            html.H6(children='Total SSH connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{'X'}",  #paragraph
                   style={'textAlign': 'center',
                    'color': '#dd1e35',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Fifth row second column
html.Div([
            html.H6(children='Total Telnet connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{'X'}", #paragraph
                   style={'textAlign': 'center',
                    'color': 'orange',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Fifth row third column
html.Div([
            html.H6(children='Total HTTP connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{'X'}", #paragraph
                   style={'textAlign': 'center',
                    'color': 'yellow',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Fifth row fourth column
html.Div([
            html.H6(children='Total HTTPS connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{'X'}", #paragraph
                   style={'textAlign': 'center',
                    'color': '#66ff66',
                          'fontSize': 30}
                   )
        ],
    className='card_container three columns')

    ], className='row flex display'),

# Fourth row of the dashboard app
html.Div([
        html.Div([
            html.H5('Select honeypot type to display data', style={'margin-bottom': '0px', 'color': '#99CCFF'})
        ])
    ], className='two-third column'),

#Sixth row
    html.Div([
        html.Div([
            #html.P('Select honeypot:', className='fix_label', style={'color':'white'}),
            dcc.Dropdown(id = 'honeypot',
                         multi =  False,
                         searchable=True,
                         value='',
                         placeholder='Select honeypot',
                         options=[{'label':c,'value':c}
                                  for c in (honeypots)], className='dcc_compon'),
        ],className='create_container three columns')
    ],className='row flex-display'),

# Bar chart
html.Div([
    html.Div([
        dcc.Graph(id = 'bar_chart', config={'displayModeBar': 'hover'})
    ], className='create_container four columns'),

# Pie chart
   html.Div([
dcc.Graph(id = 'pie_chart', config={'displayModeBar': 'hover'})
        ], className='create_container four columns'),

# Wordcloud
html.Div([
html.H6(children='Most frequent usernames/passwords',
                    style={'textAlign': 'center',
                    'color': 'white'}
                   ),
    html.Img(id="image_wc"),
], className='create_container four columns'),

], className='row flex-display'),

#Scatter map
    html.Div([
        html.Div([
            dcc.Graph(id = 'map_chart', config={'displayModeBar': 'hover'})
        ], className='create_container1 twelve columns')
    ], className='row flex-display'),

], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

def plot_wordcloud(data):
    d = {a: x for a, x in data.values}
    wc = WordCloud(background_color='#003366', width=400, height=450)
    wc.fit_words(d)
    return wc.to_image()

@app.callback(Output('image_wc', 'src'),
              [Input('image_wc', 'id')])
def make_image(b):
    img = BytesIO()
    plot_wordcloud(data=wordFreq.head(50)).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

@app.callback(Output('map_chart', 'figure'),
              [Input('honeypot','value')])
def update_graph(honeypot):
    if honeypot == 'SSH':
        geo_data = ssh_data
        colour = 'red'
    elif honeypot == 'Telnet':
        geo_data = telnet_data
        colour = 'orange'
    elif honeypot == 'HTTP':
        geo_data = http_data
        colour = 'yellow'
    elif honeypot == 'HTTPS':
        geo_data = https_data
        colour = '#66ff66'
    else:
        geo_data = blank
        colour = 'blue'

    zoom=1
    zoom_lat = 25
    zoom_long = 1

    return {
        'data': [go.Scattermapbox(
            lon=geo_data['long'],
            lat=geo_data['lat'],
            marker=go.scattermapbox.Marker(size=8,
                                            color=colour,
                                            colorscale='HSV',
                                            showscale=False,
                                            sizemode='area',
                                            opacity=0.3),
            hoverinfo='text',
            hovertext=
            '<b>Country</b>: ' + geo_data['country'].astype(str) + '<br>' +
            '<b>District</b>: ' + geo_data['province'].astype(str) + '<br>' +
            '<b>Longitude</b>: ' + geo_data['long'].astype(str) + '<br>' +
            '<b>Latitude</b>: ' + geo_data['lat'].astype(str) + '<br>'
        )],

        'layout': go.Layout(
            hovermode='x',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            margin=dict(r=0, l=0, t=0, b=0),
            mapbox=dict(
                accesstoken='pk.eyJ1IjoiczI1OTExNjhvIiwiYSI6ImNrdzB0bTEweTBuNnUydXJvZzg2emV6YzIifQ.JF_hRU0sU43KOnSkEgW4qQ',
                center = go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_long),
                style='dark',
                zoom=zoom,
            ),
            autosize=True
        )
    }


@app.callback(Output('bar_chart', 'figure'),
              [Input('honeypot','value')])
def update_graph(honeypot):
    if honeypot == 'SSH':
        daily_data = ssh_sum
        colour = 'red'
        honeypot_type = 'SSH'
    elif honeypot == 'Telnet':
        daily_data = telnet_sum
        colour = 'orange'
        honeypot_type = 'Telnet'
    elif honeypot == 'HTTP':
        daily_data = http_sum
        colour = 'yellow'
        honeypot_type = 'HTTP'
    elif honeypot == 'HTTPS':
        daily_data = https_sum
        colour = '#66ff66'
        honeypot_type = 'HTTPS'
    else:
        daily_data = blank2
        colour = 'blue'
        honeypot_type = '-'

    return {
        'data': [go.Bar(
            x=weekdays,
            y=daily_data['# connections'],
            name='Number of connections per day',
            marker=dict(color='#666699'),
            hoverinfo='text',
            # hovertext=
            # '<b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
            # '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['daily confirmed'].tail(30)] + '<br>' +
            # '<b>Country</b>: ' + covid_data_3['Country/Region'].tail(30).astype(str) + '<br>'
        )],

        'layout': go.Layout(
            title={'text': 'Connections per day to ' + honeypot_type + ' honeypot : ',
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Day of the week</b>',
                       color = 'white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )),
            yaxis=dict(title='<b>Daily Connections</b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )
                       )
        )
    }

@app.callback(Output('pie_chart', 'figure'),
              [Input('honeypot','value')])
def update_graph(honeypot):
    colors = ['orange', '#dd1e35', 'green', '#e55467']

    if honeypot == 'SSH':
        num_connections = ssh_sum['# connections'].sum()
        num_credentials = ssh_sum['# credentials'].sum()
        num_commands = ssh_sum['# commands'].sum()
        num_urls = ssh_sum['# urls'].sum()
        honeypot_type = 'SSH'
        legend = ['# connections', '# credentials', '# commands', '# urls']
        vals = [num_connections, num_credentials, num_commands, num_urls]
    elif honeypot == 'Telnet':
        num_connections = telnet_sum['# connections'].sum()
        num_commands = telnet_sum['# commands'].sum()
        num_urls = telnet_sum['# urls'].sum()
        honeypot_type = 'Telnet'
        legend = ['# connections', '# commands', '# urls']
        vals = [num_connections, num_commands, num_urls]
    elif honeypot == 'HTTP':
        num_connections = http_sum['# connections'].sum()
        honeypot_type = 'HTTP'
        legend = ['# connections']
        vals = [num_connections]
    elif honeypot == 'HTTPS':
        num_connections = https_sum['# connections'].sum()
        honeypot_type = 'HTTPS'
        legend = ['# connections']
        vals = [num_connections]
    else:
        num_connections = 0
        num_credentials = 0
        num_commands = 0
        num_urls = 0
        legend = ['# connections', '# credentials', '# commands', '# urls']
        vals = [num_connections, num_credentials, num_commands, num_urls]
        honeypot_type = '-'

    return {
        'data': [go.Pie(
            labels=legend,
            values=vals,
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            hole=.7,
            rotation=45,
            # insidetextorientation= 'radial'
        )],

        'layout': go.Layout(
            title={'text': 'Showing details for ' + honeypot_type + ' honeypot:',
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7}
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')

    # # Update server data every 10.58mins using cron
    # # print out shows what is happening
    # a = time.time()
    # b = 0
    # while True:
    #     if (b < 658):
    #         b = time.time() - a
    #     elif (b == 658):
    #         print('restarting script to update with new data')
    #         a = time.time()
    #         b = 0
    #         pass