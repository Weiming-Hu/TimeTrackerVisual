#############################################################
# Author: Weiming Hu <weiminghu@ucsd.edu>                   #
#                                                           #
#         Center for Western Weather and Water Extremes     #
#         Scripps Institution of Oceanography               #
#         UC San Diego                                      #
#                                                           #
#         https://weiming-hu.github.io/                     #
#         https://cw3e.ucsd.edu/                            #
#                _                                          #
#              (`  ).                   _                   #
#             (     ).              .:(`  )`.               #
#            _(       '`.          :(   .    )              #
#        .=(`(      .   )     .--  `.  (    ) )             #
#       ((    (..__.:'-'   .+(   )   ` _`  ) )              #
#       `(       ) )       (   .  )     (   )  ._           #
#         ` __.:'   )     (   (   ))     `-'.-(`  )         #
#      ( )       --'       `- __.'         :(      ))       #
#     (_.'          .')                    `(    )  ))      #
#                  (_  )                     ` __.:'        #
#                                                           #
#                      v  ~.      v                         #
#             v           /|                                #
#                        / |                v               #
#                 v     /__|__                              #
#                     \--------/                            #
#~~~~~~~~~~~~~~~~~~~~~~`~~~~~~'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#############################################################
#
# This script organizes the visualization layouts.
#

import tools

import dash_bootstrap_components as dbc

from dash import html, dcc, dash_table


basic_style = {
    'width': '99%',
    'min-width': '500px',
    # 'min-height': '850px',
    'margin-left': 'auto',
    'margin-right': 'auto',
    # 'margin-bottom': '170px',
    'background': '#888888',
    'padding': '15px',
}

tab_table = html.Div([
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='dropdown-table-project', clearable=True), width=2),
        dbc.Col(dcc.Dropdown(id='dropdown-table-tag', clearable=True), width=2),
        dbc.Col(dcc.DatePickerRange(id='table-date-range-picker', clearable=True), width=6),
    ], className='g-0', style={'background': 'white'}),
    dash_table.DataTable(id='table-content')
], id='tab-content-table')

tab_summary = html.Div(
    [
        html.Div(tools.set_max_days_since_last_use, style={'background': 'white'}),
        html.Div(tools.checklist_active_projects, style={'background': 'white'}),
        
        html.Br(),
        dbc.Row([
            html.Div('(Accumulated Time) Temporal resolution: '),
            dbc.Col(dcc.Dropdown(
                {
                    'D': 'Day',
                    'W-SUN': 'Week',
                    'SM': 'Semi-month',
                    'MS': 'Month',
                    'Q-DEC': 'Quaterly'
                }, 'D',
                id='dropdown-temporal-unit-1',
                clearable=False,
            ), width=1),
            dbc.Col(html.Button(id='submit-refresh-figure1', n_clicks=0, children='Refresh Line Plot'), width=2),
        ], className='g-0', style={'background': 'white'}),
        html.Div(tools.graph_accum_duration_by_project),
        
        html.Br(),
        dbc.Row([
            html.Div('(Non-Accumulated Time) Temporal resolution: '),
            dbc.Col(dcc.Dropdown(
                {
                    'D': 'Day',
                    'W-SUN': 'Week',
                    'SM': 'Semi-month',
                    'MS': 'Month',
                    'Q-DEC': 'Quaterly'
                }, 'W-SUN',
                id='dropdown-temporal-unit-2',
                clearable=False,
            ), width=1),
            dbc.Col(html.Button(id='submit-refresh-figure2', n_clicks=0, children='Refresh Bar Plot'), width=2),
        ], className='g-0', style={'background': 'white'}),
        html.Div(tools.graph_daily_time_by_project),
        
        html.Br(),
        dbc.Row([
            dbc.Col(tools.select_project, width=6),
            dbc.Col(tools.select_tag, width=6),
        ], className='g-0', style={'background': 'white'}),
    ],
    
    id='tab-content-summary',
)

panel_layout = html.Div([
    dcc.Tabs(id="tabs-top-level", value='tab-summary', children=[
        dcc.Tab(label='Summary', value='tab-summary'),
        dcc.Tab(label='Data Table', value='tab-table'),
    ]),
    tab_table,
    tab_summary,
])
