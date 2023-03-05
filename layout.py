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

from dash import html, dcc


panel_layout = html.Div(
    [
        html.Div(tools.set_max_days_since_last_use),
        html.Div(tools.checklist_active_projects),
        html.Br(),
        html.Div(dcc.Checklist(
            ['Exclude undefined projects'],
            ['Exclude undefined projects'],
            labelStyle={'display': 'inline-block', 'width': '250px'},
            inputStyle={"margin-right": "5px"},
            id='checklist-exclude_undefined',
        )),
        html.Div(['Temporal resolution: ', dcc.Dropdown(
            {
                'D': 'Day',
                'W-MON': 'Week',
                'SM': 'Semi-month',
                'MS': 'Month',
                'Q-DEC': 'Quaterly'
            }, 'D',
            id='dropdown-temporal-unit',
            style={'width': '150px'},
            clearable=False,
        )]),
        html.Div(html.Button(id='submit-refresh-figures', n_clicks=0, children='Refresh Figures'),),
        html.Div(tools.graph_accum_duration_by_project),
        html.Div(tools.graph_daily_time_by_project),
    ],
            
    style={
        'width': '97%',
        # 'min-width': '500px',
        # 'min-height': '850px',
        'margin-left': 'auto',
        'margin-right': 'auto',
        # 'margin-bottom': '170px',
        # 'background': '#888888',
        # 'padding': '3px',
    }
)