# Importing Required Libraries

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, html, dcc
from dash.exceptions import PreventUpdate

# Loading Data

url = 'https://raw.githubusercontent.com/NurulYakimKazal/Dash-App-For-Retail-Sales-Data/main/retail_sales.csv'

data = pd.read_csv(url, sep=',')
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')


# Helper Functions For Data Preparation

def monthly_data(dataframe):
    monthly_sales = dataframe.groupby(['month', 'Month'])['Weekly_Sales'].sum().reset_index()
    monthly_sales = monthly_sales.rename(columns={'Weekly_Sales': 'Monthly_Sales'})
    holiday_sales = dataframe[dataframe['IsHoliday'] == True].groupby(['month'])['Weekly_Sales'].sum().reset_index()
    holiday_sales = holiday_sales.rename(columns={'Weekly_Sales': 'Holiday_Sales'})
    merge_data = pd.merge(monthly_sales, holiday_sales, on='month', how='left').fillna(value=0)
    merge_data['Monthly_Sales'] = merge_data['Monthly_Sales'].round(1)
    merge_data['Holiday_Sales'] = merge_data['Holiday_Sales'].round(1)
    return merge_data


def weekly_data(dataframe):
    weekly_sales = dataframe.groupby(['month', 'Month', 'Date'])['Weekly_Sales'].sum().reset_index()
    weekly_sales['Weekly_Sales'] = weekly_sales['Weekly_Sales'].round(1)
    weekly_sales['Week_Number'] = weekly_sales.groupby(['month'])['Date'].rank(method='min').astype('int')
    return weekly_sales


def store_data(dataframe):
    store_sales = dataframe.groupby(['month', 'Month', 'Store'])['Weekly_Sales'].sum().reset_index()
    store_sales['Weekly_Sales'] = store_sales['Weekly_Sales'].round(1)
    store_sales['Store'] = store_sales['Store'].apply(lambda x: 'Store' + ' ' + str(x))
    return store_sales


def dept_data(dataframe):
    dept_sales = dataframe.groupby(['month', 'Month', 'Dept'])['Weekly_Sales'].sum().reset_index()
    dept_sales['Weekly_Sales'] = dept_sales['Weekly_Sales'].round(1)
    dept_sales['Dept'] = dept_sales['Dept'].apply(lambda x: 'Dept' + ' ' + str(x))
    return dept_sales


monthly_sales_data = monthly_data(data)
weekly_sales_data = weekly_data(data)
store_sales_data = store_data(data)
dept_sales_data = dept_data(data)

all_options = {x: [y for y in data['Month'].unique() if y != x] for x in data['Month'].unique()}

# Components Of Content

card_header1 = dbc.CardHeader('Select Months',
                              className='bg-dark bg-opacity-25 border-bottom border-secondary d-flex align-items-center justify-content-center',
                              style={'height': '30%', 'textAlign': 'center', 'fontSize': '14px', 'fontWeight': 500,
                                     'color': 'white'})

card_header2 = dbc.CardHeader('Total Sales',
                              className='bg-dark bg-opacity-25 border-bottom border-secondary d-flex align-items-center justify-content-center',
                              style={'height': '30%', 'textAlign': 'center', 'fontSize': '14px', 'fontWeight': 500,
                                     'color': 'white'})

card_header3 = dbc.CardHeader('Holiday Sales',
                              className='bg-dark bg-opacity-25 border-bottom border-secondary d-flex align-items-center justify-content-center',
                              style={'height': '30%', 'textAlign': 'center', 'fontSize': '14px', 'fontWeight': 500,
                                     'color': 'white'})

card_header4 = dbc.CardHeader('Total Stores',
                              className='bg-dark bg-opacity-25 border-bottom border-secondary d-flex align-items-center justify-content-center',
                              style={'height': '30%', 'textAlign': 'center', 'fontSize': '14px', 'fontWeight': 500,
                                     'color': 'white'})

card_header5 = dbc.CardHeader('Weekly Sales Comparison',
                              className='bg-dark bg-opacity-25 border-bottom border-secondary d-flex align-items-center justify-content-center',
                              style={'height': '14.5%', 'textAlign': 'center', 'fontSize': '14px', 'fontWeight': 500,
                                     'color': 'white'})

card_header6 = dbc.CardHeader(id='header',
                              className='bg-dark bg-opacity-25 border-bottom border-secondary d-flex align-items-center justify-content-center',
                              style={'height': '14.5%', 'textAlign': 'center', 'fontSize': '14px', 'fontWeight': 500,
                                     'color': 'white'})

card_header7 = dbc.CardHeader('Stores With Highest Sales',
                              className='bg-dark bg-opacity-25 border-bottom border-secondary d-flex align-items-center justify-content-center',
                              style={'height': '14.5%', 'textAlign': 'center', 'fontSize': '14px', 'fontWeight': 500,
                                     'color': 'white'})

card_body1 = dbc.CardBody([
    dbc.Row([
        dbc.Col([
            html.Label('Current Period', style={'fontSize': '15px', 'fontWeight': 500, 'color': 'white'}),
            dcc.Dropdown(
                id='current',
                options=list(all_options.keys()),
                value=list(all_options.keys())[0],
                multi=False,
                maxHeight=140,
                style={'width': '100%', 'textAlign':'left'})
        ], width=6, className='vstack gap-0 d-flex align-items-start justify-content-center',
            style={'height': '100%'}),
        dbc.Col([
            html.Label('Reference Period', style={'fontSize': '15px', 'fontWeight': 500, 'color': 'white'}),
            dcc.Dropdown(
                id='reference',
                multi=False,
                maxHeight=140,
                style={'width': '100%', 'textAlign':'left'})
        ], width=6, className='vstack gap-0 d-flex align-items-start justify-content-center', style={'height': '100%'})
    ], style={'textAlign': 'center', 'height': '100%', 'width': '100%'})
], className='mt-0 mb-0 d-flex flex-column align-items-center justify-content-start', style={'height': '70px'})

card_body2 = dbc.CardBody([
    dcc.Graph(
        id='card2',
        className='d-flex align-items-center justify-content-center',
        style={'height': '100%', 'width': '100%'}
    )
], style={'height':'70%'})

card_body3 = dbc.CardBody([
    dcc.Graph(
        id='card3',
        className='d-flex align-items-center justify-content-center',
        style={'height': '100%', 'width': '100%'}
    )
], style={'height':'70%'})

card_body4 = dbc.CardBody([
    dcc.Graph(
        id='card4',
        className='d-flex align-items-center justify-content-center',
        style={'height': '100%', 'width': '100%'}
    )
], style={'height':'70%'})

card_body5 = dbc.CardBody([
    dcc.Graph(
        id='graph1',
        className='d-flex align-items-center justify-content-center',
        style={'height': '100%', 'width': '100%'}
    )
], className='d-flex align-items-center justify-content-center', style={'height': '85.5%'})

card_body6 = dbc.CardBody([
    dcc.Graph(
        id='graph2',
        className='d-flex align-items-center justify-content-center',
        style={'height': '100%', 'width': '100%'}
    )
], className='d-flex align-items-center justify-content-center', style={'height': '85.5%'})

card_body7 = dbc.CardBody([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='graph3',
                className='d-flex align-items-center justify-content-center',
                style={'height': '100%', 'width': '100%'}
            )
        ], width=6, className='d-flex align-items-center justify-content-center', style={'height': '100%'}),
        dbc.Col([
            dcc.Graph(
                id='graph4',
                className='d-flex align-items-center justify-content-center',
                style={'height': '100%', 'width': '100%'}
            )
        ], width=6, className='d-flex align-items-center justify-content-center', style={'height': '100%'})
    ], className='d-flex align-items-center justify-content-center', style={'height': '100%', 'width': '100%'})
], className='d-flex align-items-center justify-content-center', style={'height': '85.5%'})

# App Initialization

plotly_logo = 'https://images.plot.ly/logo/new-branding/plotly-logomark.png'

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}])

app.title = 'Retail Sales Dashboard'

navbar = dbc.Navbar([
    dbc.Container([
        html.A([
            dbc.Row([
                dbc.Col(html.Img(src=plotly_logo, height='27.5px')),
                dbc.Col(dbc.NavbarBrand('Retail Sales Dashboard', className='ms-2',
                                        style={'fontWeight': 500, 'color': 'white'}))
            ], align='center', className='g-0', style={'opacity': '90%'})
        ], href='https://plotly.com', style={'textDecoration': 'none'})
    ])
], className='bg-dark', style={'height':'45px'})

# App Layout

app.layout = dbc.Container([
    navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([card_header1, card_body1], style={'height':'100%', 'width':'100%'})
                    ], width=12, className='m-0 d-flex align-items-center justify-content-center',
                        style={'height': '153px', 'padding':'3px'}),
                    dbc.Col([
                        dbc.Card([card_header2, card_body2], style={'height':'100%', 'width':'100%'})
                    ], width=4, lg=12, className='m-0 d-flex align-items-center justify-content-center',
                        style={'height': '153px', 'padding':'3px'}),
                    dbc.Col([
                        dbc.Card([card_header3, card_body3], style={'height':'100%', 'width':'100%'})
                    ], width=4, lg=12, className='m-0 d-flex align-items-center justify-content-center',
                        style={'height': '153px', 'padding':'3px'}),
                    dbc.Col([
                        dbc.Card([card_header4, card_body4], style={'height':'100%', 'width':'100%'})
                    ], width=4, lg=12, className='m-0 d-flex align-items-center justify-content-center',
                        style={'height': '153px', 'padding':'3px'})
                ], className='m-0 p-0')
            ], lg=4, className='m-0 p-0'),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([card_header5, card_body5], style={'height': '100%', 'width': '100%'})
                    ], width=12, md=6, className='m-0 d-flex align-items-center justify-content-center',
                        style={'height': '306px', 'padding': '3px'}),
                    dbc.Col([
                        dbc.Card([card_header6, card_body6], style={'height': '100%', 'width': '100%'})
                    ], width=12, md=6, className='m-0 d-flex align-items-center justify-content-center',
                        style={'height': '306px', 'padding': '3px'})
                ], className='m-0 p-0'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([card_header7, card_body7], style={'height': '100%', 'width': '100%'})
                    ], width=12, className='m-0 d-flex align-items-center justify-content-center',
                        style={'height': '306px', 'padding': '3px'})
                ], className='m-0 p-0')
            ], lg=8, className='m-0 p-0')
        ], className='m-0 p-0')
    ], className='m-0 p-0', fluid=True)
], className='m-0 p-0', fluid=True)

# App Callbacks

@app.callback(
    Output('reference', 'options'),
    Output('reference', 'value'),
    Input('current', 'value')
)
def set_reference_options_and_value(selected_option):
    if selected_option is None:
        raise PreventUpdate
    else:
        options = [{'label': x, 'value': x} for x in all_options[selected_option]]
        value = options[0]['label']
        return options, value
    
@app.callback(
    Output('card2', 'figure'),
    Input('current', 'value'),
    Input('reference', 'value')
)

def update_card2(current, reference):
    if ((current is None) or (reference is None)):
        raise PreventUpdate
    else:
        current_mask = monthly_sales_data[monthly_sales_data['Month']==current]
        current_total_sales = current_mask.reset_index().loc[0]['Monthly_Sales']
        reference_mask = monthly_sales_data[monthly_sales_data['Month']==reference]
        reference_total_sales = reference_mask.reset_index().loc[0]['Monthly_Sales'] 
        
        card2 = go.Figure()
        card2.add_trace(
            go.Indicator(
                mode = "number+delta",
                value = current_total_sales,
                number = {'valueformat':'$.2f', 'suffix':'M'},
                align='center',                
                delta={'reference': reference_total_sales, 'relative':False, 'position':'bottom', 'valueformat':'$.2f', 'suffix':'M'},
                domain = {'x': [0.15, 0.85], 'y': [0, 1]}                
            )
        )
        card2.update_layout(
            template='plotly_dark',
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return card2
    
@app.callback(
    Output('card3', 'figure'),
    Input('current', 'value'),
    Input('reference', 'value')
)

def update_card3(current, reference):
    if ((current is None) or (reference is None)):
        raise PreventUpdate
    else:
        current_holiday_mask = monthly_sales_data[monthly_sales_data['Month']==current]
        current_holiday_total_sales = current_holiday_mask.reset_index().loc[0]['Holiday_Sales']
        reference_holiday_mask = monthly_sales_data[monthly_sales_data['Month']==reference]
        reference_holiday_total_sales = reference_holiday_mask.reset_index().loc[0]['Holiday_Sales'] 
                
        card3 = go.Figure()
        card3.add_trace(
            go.Indicator(
                mode = "number+delta",
                value = current_holiday_total_sales,
                number = {'valueformat':'$.2f', 'suffix':'M'},
                align='center',                
                delta={'reference': reference_holiday_total_sales, 'relative':False, 'position':'bottom', 'valueformat':'$.2f', 'suffix':'M'},
                domain = {'x': [0.15, 0.85], 'y': [0, 1]}                
            )
        )
        card3.update_layout(
            template='plotly_dark',
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return card3
    
@app.callback(
    Output('card4', 'figure'),
    Input('current', 'value'),
    Input('reference', 'value')
)

def update_card4(current, reference):
    if ((current is None) or (reference is None)):
        raise PreventUpdate
    else:
        current_total_store = data[data['Month']==current]['Store'].drop_duplicates().count()
        reference_total_store = data[data['Month']==reference]['Store'].drop_duplicates().count()
    
        card4 = go.Figure()
        card4.add_trace(
            go.Indicator(
                mode = "number+delta",
                value = current_total_store,
                align='center',                
                delta={'reference': reference_total_store, 'relative':False, 'position':'bottom'},
                domain = {'x': [0.15, 0.85], 'y': [0, 1]}                
            )
        )
        card4.update_layout(
            template='plotly_dark',
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return card4

@app.callback(
    Output('graph1', 'figure'),
    Input('current', 'value'),
    Input('reference', 'value')
)
def update_graph1(current, reference):
    if ((current is None) or (reference is None)):
        raise PreventUpdate
    else:
        current_month = weekly_sales_data[weekly_sales_data['Month'] == current]
        reference_month = weekly_sales_data[weekly_sales_data['Month'] == reference]

        fig1 = go.Figure()

        fig1.add_trace(
            go.Scatter(
                x=current_month['Week_Number'],
                y=current_month['Weekly_Sales'],
                line=dict(color='cyan', width=3),
                name='{}'.format(current),
                text=current_month['Month'],
                hovertemplate=
                "<i><b>Week %{x}</b></i><br>" +
                "<i><b>Sales:</b> %{y}</i><br>" +
                "<extra></extra>",
            )
        )

        fig1.add_trace(
            go.Scatter(
                x=reference_month['Week_Number'],
                y=reference_month['Weekly_Sales'],
                line=dict(color='dodgerblue', width=3),
                name='{}'.format(reference),
                text=reference_month['Month'],
                hovertemplate=
                "<i><b>Week %{x}</b></i><br>" +
                "<i><b>Sales:</b> %{y}</i><br>" +
                "<extra></extra>"
            )
        )

        fig1.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='white',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                )
            ),
            yaxis=dict(
                showgrid=False,
                showline=True,
                showticklabels=True,
                linecolor='white',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                )
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            yaxis_tickformat='$',
            yaxis_ticksuffix='M',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1,
                font=dict(
                    family="Arial",
                    size=12,
                    color="white"
                )
            )
        )
        return fig1


@app.callback(
    Output('header', 'children'),
    Input('current', 'value'),
    Input('reference', 'value')
)
def update_header(current, reference):
    if ((current is None) or (reference is None)):
        raise PreventUpdate
    else:
        header = 'Sales Difference Between Top Departments ({0}-{1})'.format(current, reference)
        return header


@app.callback(
    Output('graph2', 'figure'),
    Input('current', 'value'),
    Input('reference', 'value')
)
def update_graph2(current, reference):
    if ((current is None) or (reference is None)):
        raise PreventUpdate
    else:
        current_dept = dept_sales_data[dept_sales_data['Month'] == current].sort_values('Weekly_Sales',
                                                                                        ascending=False).reset_index()[
                       :10]
        current_dept = current_dept.rename(columns={'Weekly_Sales': 'Current_Weekly_Sales'})
        reference_dept = dept_sales_data[dept_sales_data['Month'] == reference].sort_values('Weekly_Sales',
                                                                                            ascending=False).reset_index()
        reference_dept = reference_dept.rename(columns={'Weekly_Sales': 'Reference_Weekly_Sales'})
        merged_dept = pd.merge(current_dept, reference_dept, on='Dept', how='left')
        merged_dept['Difference'] = np.round(
            merged_dept['Current_Weekly_Sales'] - merged_dept['Reference_Weekly_Sales'], 1)

        fig2 = go.Figure()

        fig2.add_trace(
            go.Bar(
                x=merged_dept['Difference'],
                y=merged_dept['Dept'],
                marker=dict(
                    color='lightsteelblue'
                ),
                orientation='h',
                text=merged_dept['Difference'],
                textposition='outside',
                textfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                ),
                hovertemplate=
                "<i><b>%{y}</b></i><br>" +
                "<i><b>Sales Diff:</b> %{x}</i><br>" +
                "<extra></extra>"
            )
        )

        fig2.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                zeroline=False,
                showticklabels=True,
                linecolor='white',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                ),
                range=['{}'.format(merged_dept['Difference'].min() - 3),
                       '{}'.format(merged_dept['Difference'].max() + 3)]
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                )
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_tickformat='$',
            xaxis_ticksuffix='M'
        )
        return fig2


@app.callback(
    Output('graph3', 'figure'),
    Input('current', 'value')
)
def update_graph3(current):
    if current is None:
        raise PreventUpdate
    else:
        current_store_sales = store_sales_data[store_sales_data['Month'] == current].sort_values(by='Weekly_Sales',
                                                                                                 ascending=False).reset_index()[
                              :10]

        fig3 = go.Figure()

        fig3.add_trace(
            go.Bar(
                x=current_store_sales['Weekly_Sales'],
                y=current_store_sales['Store'],
                marker=dict(
                    color='cyan'
                ),
                orientation='h',
                text=current_store_sales['Weekly_Sales'],
                textposition='outside',
                textfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                ),
                name='{}'.format(current),
                hovertemplate=
                "<i><b>%{y}</b></i><br>" +
                "<i><b>Sales:</b> %{x}</i><br>" +
                "<extra></extra>"
            )
        )

        fig3.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                zeroline=False,
                showticklabels=True,
                linecolor='white',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                ),
                range=[0, '{}'.format(current_store_sales['Weekly_Sales'].max() + 2.75)]
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                )
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=27.5, b=0),
            xaxis_tickformat='$',
            xaxis_ticksuffix='M',
            title='{}'.format(current),
            title_x=0.5,
            title_y=0.99,
            title_font_family='Arial',
            title_font_color='white',
            title_font_size=15
        )
        return fig3


@app.callback(
    Output('graph4', 'figure'),
    Input('reference', 'value')
)
def update_graph4(reference):
    if reference is None:
        raise PreventUpdate
    else:
        reference_store_sales = store_sales_data[store_sales_data['Month'] == reference].sort_values(by='Weekly_Sales',
                                                                                                     ascending=False).reset_index()[
                                :10]

        fig4 = go.Figure()

        fig4.add_trace(
            go.Bar(
                x=reference_store_sales['Weekly_Sales'],
                y=reference_store_sales['Store'],
                marker=dict(
                    color='dodgerblue'
                ),
                orientation='h',
                text=reference_store_sales['Weekly_Sales'],
                textposition='outside',
                textfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                ),
                name='{}'.format(reference),
                hovertemplate=
                "<i><b>%{y}</b></i><br>" +
                "<i><b>Sales:</b> %{x}</i><br>" +
                "<extra></extra>"
            )
        )

        fig4.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                zeroline=False,
                showticklabels=True,
                linecolor='white',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                ),
                range=[0, '{}'.format(reference_store_sales['Weekly_Sales'].max() + 2.75)]
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                )
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=27.5, b=0),
            xaxis_tickformat='$',
            xaxis_ticksuffix='M',
            title='{}'.format(reference),
            title_x=0.5,
            title_y=0.99,
            title_font_family='Arial',
            title_font_color='white',
            title_font_size=15
        )
        return fig4

# App Execution

if __name__ == '__main__':
    app.run_server(debug=True)