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
# This script defines and create the various layouts.
#

import utils
import config

import pandas as pd

from dash import html, dcc


#############
# Read Data #
#############

max_days_since_last_use = 90

tables = utils.read_tables()
table_complete = utils.get_work_interval(tables)


############################
# Active Project Selection #
############################

set_max_days_since_last_use = [
    'Active projects are those used within the last ',
    dcc.Input(id='input-days-since-last-use',
              value=max_days_since_last_use,
              style={'width': '100px'},
              type='number'),
    ' days. ',
]

days_since_last_use = utils.count_days_since_last_use(table_complete, remove_undefined=False)
default_checked = days_since_last_use['project_name'][days_since_last_use.start <= max_days_since_last_use]
default_checked = default_checked[default_checked != 'UNDEFINED']

checklist_active_projects = [
    html.Div('The following projects are active projects:'),
    dcc.Checklist(
        options={x: '{} ({} days)'.format(x, y) for i, (x, y) in days_since_last_use.iterrows()},
        value=default_checked,
        labelStyle={'display': 'inline-block', 'width': '250px'},
        inputStyle={"margin-right": "5px"},
        id='checklist-active-projects',
    )
]


######################################
# Accumulated Duractions by Projects #
######################################

graph_accum_duration_by_project = dcc.Graph(
    id='graph-accum-duration-by-project',
)


#####################################
# Daily Time Allocation by Projects #
#####################################

graph_daily_time_by_project = dcc.Graph(
    id='graph-daily-time-by-project',
)


#####################################
# Select Project for Visualization #
#####################################

all_projects = table_complete.project_name.unique()
default_project_selection = table_complete['project_name'][table_complete['start'].idxmax()]

select_project = [
    'Select a project for the pie chart below: ',
    dcc.Dropdown(
        all_projects, default_project_selection,
        id='dropdown-pie-project',
        style={'width': '150px'},
        clearable=False,
    ),
    html.Div(dcc.Graph(id='pie-project')),
]


################################
# Select Tag for Visualization #
################################

select_tag = [
    'Select a tag for the pie chart below: ',
    dcc.Dropdown(
        id='dropdown-pie-tag',
        style={'width': '150px'},
        clearable=False,
    ),
    html.Div(dcc.Graph(id='pie-tag')),
]
