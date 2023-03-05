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
# This script define callback functions.
#

import utils
import config

import plotly.express as px

from main import app
from tools import table_complete
from dash import Input, Output, State


@app.callback(
    Output('checklist-active-projects', 'value'),
    Input('input-days-since-last-use', 'value'))
def update_active_project_selection(max_days_since_last_use):
    days_since_last_use = utils.calc_days_since_last_use(table_complete)
    days_since_last_use['label'] = ['{} ({} days)'.format(x, y) for i, (x, y) in days_since_last_use.iterrows()]
    return days_since_last_use[days_since_last_use.start <= max_days_since_last_use].label


@app.callback(
    [
        Output('graph-accum-duration-by-project', 'figure'), 
        Output('graph-daily-time-by-project', 'figure')
    ],
    Input('submit-refresh-figures', 'n_clicks'),
    State('checklist-active-projects', 'value'),
    State('checklist-exclude_undefined', 'value'),
    State('dropdown-temporal-unit', 'value'),)
def update_graph_timeseries(n_clicks, checked_items, exclude_undefined, temporal_unit):
    
    table = table_complete[table_complete.project_name != 'UNDEFINED'] \
            if len(exclude_undefined) > 0 else table_complete.copy()
    
    active_projects = [i.split(' ')[0] for i in checked_items]
    table = table[table.project_name.isin(active_projects)]
    
    fig_accum_duration_by_project = px.line(
        utils.summarize_duration_by_project(table, True, temporal_unit),
        x='start', y='duration', color='project')

    fig_accum_duration_by_project.update_layout(
        margin=config.FIG_MARGINS,
        xaxis={
            'rangeslider': {'visible': True},
            'title': '<sup>Data from only active projects</sup>',
        },
        yaxis_title='Accumulated Time Spent on Projects [h]',
        legend_title_text='Project',
    )
    
    fig_daily_time_by_project = px.bar(
        utils.summarize_duration_by_project(table, False, temporal_unit),
        x='start', y='duration', color='project',
        labels={
            'start': 'Date',
            'duration': 'Duration (h)',
            'project': 'Project',
        })

    fig_daily_time_by_project.update_layout(
        margin=config.FIG_MARGINS,
        xaxis={
            'rangeslider': {'visible': True},
            'title':'<sup>Data from only active projects</sup>'
        },
        yaxis_title='Everyday Time Spent on Projects [h]',
        legend_title_text='Project',
    )

    return fig_accum_duration_by_project, fig_daily_time_by_project
