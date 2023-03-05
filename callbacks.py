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
import layout

import pandas as pd
import plotly.express as px

from main import app
from tools import table_complete
from dash import Input, Output, State


@app.callback(
    [
        Output('tab-content-table', 'style'),
        Output('tab-content-summary', 'style'),
        Output('dropdown-table-project', 'options'),
        Output('dropdown-table-project', 'value'),
        Output('dropdown-table-tag', 'options'),
        Output('dropdown-table-tag', 'value'),
        Output('table-date-range-picker', 'min_date_allowed'),
        Output('table-date-range-picker', 'max_date_allowed'),
    ],
    Input('tabs-top-level', 'value'))
def render_content(tab):
    on = {**layout.basic_style, 'display': 'block'}
    off = {**layout.basic_style, 'display': 'none'}
    
    if tab == 'tab-summary':
        return off, on, [], None, [], None, None, None
    
    elif tab == 'tab-table':
        
        all_projects = table_complete.project_name.unique()
        default_project_selection = table_complete['project_name'][table_complete['start'].idxmax()]
        
        all_tags = utils.get_all_tags(table_complete)
        default_tag_selection = table_complete['tags'][table_complete['start'].idxmax()]
        
        min_date = table_complete.start.min()
        max_date = table_complete.start.max()
        
        return on, off, all_projects, default_project_selection, all_tags, default_tag_selection, min_date, max_date
    

@app.callback(
    [
        Output('table-content', 'data'),
        Output('table-content', 'columns'),
    ],
    Input('dropdown-table-project', 'value'),
    Input('dropdown-table-tag', 'value'),
    Input('table-date-range-picker', 'start_date'),
    Input('table-date-range-picker', 'end_date'),
)
def render_data_table(project, tag, start, end):
    if project or tag:
        
        table = table_complete.copy()
        
        if project:
            table = table[table.project_name == project]
            
        if tag:
            table = table[table.tags.str.contains(tag)]
            
        if start:
            table = table[pd.to_datetime(start).tz_localize(config.MY_TZ) <= table.start]
            
        if end:
            table = table[table.start <= pd.to_datetime(end).tz_localize(config.MY_TZ)]
            
        return table.to_dict('records'), [{'name': i, 'id': i} for i in table.columns]
    else:
        return (), []
    

@app.callback(
    Output('checklist-active-projects', 'value'),
    Input('input-days-since-last-use', 'value'))
def update_active_project_selection(max_days_since_last_use):
    days_since_last_use = utils.count_days_since_last_use(table_complete)
    return days_since_last_use['project_name'][days_since_last_use.start <= max_days_since_last_use]


@app.callback(
    [
        Output('dropdown-pie-tag', 'options'),
        Output('dropdown-pie-tag', 'value'),
    ],
    Input('checklist-active-projects', 'value'))
def update_tag_pie_project_selector(active_projects):
    table = table_complete[table_complete.project_name.isin(active_projects)]
    
    all_tags = utils.get_all_tags(table)
    default_tag_selection = table['tags'][table['start'].idxmax()]

    if ',' in default_tag_selection:
        default_tag_selection = default_tag_selection.split(',')[0]
        
    return all_tags, default_tag_selection


@app.callback(
    Output('graph-accum-duration-by-project', 'figure'), 
    Input('submit-refresh-figure1', 'n_clicks'),
    State('checklist-active-projects', 'value'),
    State('dropdown-temporal-unit-1', 'value'))
def update_figure1(n_clicks, active_projects, temporal_unit):
    
    table = table_complete.copy()
    
    # Select avtive projects
    table = table[table.project_name.isin(active_projects)]
    
    fig_accum_duration_by_project = px.line(
        utils.summarize_duration_by_project(table, True, temporal_unit),
        x='start', y='duration', color='project')

    fig_accum_duration_by_project.update_layout(
        margin=config.FIG_MARGINS,
        xaxis_title='',
        yaxis_title='Accumulated Time Spent on Projects [h]',
        legend_title_text='Project',
    )
    
    return fig_accum_duration_by_project


@app.callback(
    Output('graph-daily-time-by-project', 'figure'),
    Input('submit-refresh-figure2', 'n_clicks'),
    State('checklist-active-projects', 'value'),
    State('dropdown-temporal-unit-2', 'value'))
def update_figure2(n_clicks, active_projects, temporal_unit):
    
    table = table_complete.copy()
    
    # Select avtive projects
    table = table[table.project_name.isin(active_projects)]
    
    # Create table to visualize
    table = utils.summarize_duration_by_project(table, False, temporal_unit)
    
    # Create percentage
    week_total = table.groupby('start')['duration'].sum()
    table['perc'] = table['duration'].to_numpy() / week_total[table.start].to_numpy() * 100
    
    fig_daily_time_by_project = px.bar(
        table, x='start', y='duration', color='project',
        hover_data={'project': True,  'start': True, 'duration': True, 'perc': ':.2f'},
    )

    fig_daily_time_by_project.update_layout(
        margin=config.FIG_MARGINS,
        xaxis_title='',
        yaxis_title='Non-Accumulated Time Spent on Projects [h]',
        legend_title_text='Project',
    )

    return fig_daily_time_by_project


@app.callback(
    Output('pie-project', 'figure'),
    Input('dropdown-pie-project', 'value'))
def update_pie_1(project):
    table = table_complete[table_complete.project_name == project].copy()
    table.loc[table.tags == '', 'tags'] = 'Untagged'
    fig = px.pie(table, values='duration', names='tags')
    fig.update_layout(
        margin=config.FIG_MARGINS,
        legend_title_text='Tag',
    )
    return fig


@app.callback(
    Output('pie-tag', 'figure'),
    Input('dropdown-pie-tag', 'value'),
    State('checklist-active-projects', 'value'))
def update_pie_2(tag, active_projects):
    if tag:
        table = table_complete[table_complete.project_name.isin(active_projects)]
        table = table[table.tags.str.contains(tag)]
        fig = px.pie(table, values='duration', names='project_name')
        fig.update_layout(
            margin=config.FIG_MARGINS,
            legend_title_text='Project',
        )
        return fig
