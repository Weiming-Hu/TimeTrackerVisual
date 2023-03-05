import os
import glob

import numpy as np
import pandas as pd

from config import *


def get_all_tags(table):
    all_tags = table['tags'].unique()
    all_tags = [i for i in all_tags if i != '']
    all_tags = [i.split(',') if ',' in i else [i] for i in all_tags]
    all_tags = pd.unique([x for y in all_tags for x in y])
    return all_tags


def datetime_to_unix(t):
    return (t.tz_convert('UTC') - pd.Timestamp('1970-01-01').tz_localize('UTC'))  // pd.Timedelta('1s')


def unix_to_datetime(t):
    return pd.to_datetime(t, unit='s', origin='unix').tz_localize('UTC').tz_convert(MY_TZ)


def count_days_since_last_use(table, remove_undefined=True):
    
    days_since_last_use = pd.Timestamp.now().tz_localize(MY_TZ) - table.groupby('project_name')['start'].max()
    days_since_last_use = days_since_last_use.dt.floor('d').dt.days
    days_since_last_use = pd.DataFrame(days_since_last_use.sort_values(ascending=True)).reset_index()
    
    if remove_undefined:
        days_since_last_use = days_since_last_use[days_since_last_use['project_name'] != 'UNDEFINED']
        
    return days_since_last_use


def read_tables(table_files=TABLE_FILES, table_dir=TABLE_DIR,
                filter_user='Weiming', remove_running=True, translate_time=True, tz=MY_TZ):
    
    tables = {}
    
    for k, (file_name, columns) in table_files.items():
        
        file_path = os.path.join(table_dir, file_name)
        
        # Make sure the number of columns match the shape of the table
        t = pd.read_csv(file_path, sep='\t')
        assert t.shape[1] == len(columns), 'Column mismatch for {}'.format(file_name)
        
        # Read table
        t = pd.read_csv(file_path, sep='\t', names=columns)
        
        if filter_user is not None:
            if 'user_uid' in columns: t = t[t['user_uid'] == 'Weiming']
            elif 'created_by_user_uid' in columns: t = t[t['created_by_user_uid'] == 'Weiming']
            elif k == 'client': t = t[t['name'] == 'Weiming']
        
        if remove_running and k == 'work_interval':
            t = t[t['running'] == 0]
        
        if translate_time:
            
            if k == 'work_interval': col = 'start'
            elif k in ['workint_to_tag', 'tag', 'project', 'client']: col = 'created_at'
                
            # Convert UNIX to datetime
            t[col] = pd.to_datetime(t[col], unit='s')
            
            # Convert timezone
            t[col] = t[col].dt.tz_localize('UTC').dt.tz_convert(tz)
        
        tables[k] = t
        
    
    # Make sure columns are of the correct type
    columns = {
        'work_interval': ['id', 'project_id', 'duration'],
        'workint_to_tag': ['id', 'work_interval_id', 'tag_id'],
        'tag': ['id'],
        'project': ['id', 'client_id'],
        'client': ['id'],
    }

    for k, columns in columns.items():
        for c in columns:
            tables[k].loc[tables[k][c] == r'\N', c] = np.NaN
            tables[k][c] = tables[k][c].astype(float)
        
    return tables


def get_work_interval(tables, add_tags=True, use_project_names=True):
    
    table = tables['work_interval'].copy()
    
    if add_tags:
        
        # Initialize a new column
        table['tags'] = 'UNDEFINED'
        
        # Get the lookup table for tags
        lookup = tables['workint_to_tag']
        lookup2 = tables['tag'].set_index('id')
        
        # Assign tags
        for index, row in table.iterrows():
            tag_ids = lookup['tag_id'][lookup['work_interval_id'] == row['id']].tolist()
            
            for i, n in enumerate(tag_ids):
                tag_ids[i] = lookup2.loc[n]['name']
                
            table.loc[index, 'tags'] = ','.join(tag_ids)
    
    if use_project_names:
        
        # Initialize a new column
        table['project_name'] = 'UNDEFINED'
        
        # Get the lookup table for project names
        lookup = tables['project'].set_index('id')
        
        # Assign names if they exist
        for index, row in table.iterrows():
            try:
                table.loc[index, 'project_name'] = lookup.loc[int(row['project_id']), 'name']
            except:
                pass
        
        # Remove old column
        del table['project_id']
        
    # Drop some columns that we do not need
    del table['id']
    del table['lineend']
    del table['user_uid']
    del table['running']
    
    # Check data
    mask = (table['project_name'] == 'UNDEFINED') & table['tags'].isin([''])
    
    if table[mask].shape[0] != 0:
        print(table[mask])
        raise Exception('The above rows do not have a project and tags assigned!')
        
    # Convert unit
    table['duration'] /= 3600
                
    return table


def summarize_duration_by_project(table, accumulate_duration, temporal_unit='D'):
    
    project_df = []
    
    for project in table['project_name'].unique():
        
        # Get entries associated with this project
        x = table[table['project_name'] == project]
        x = x.groupby(pd.Grouper(key='start', freq=temporal_unit))['duration'].sum()
        
        # Remove zero rows
        x = x[x > 0]
        
        # Create new data frame for this project
        df = pd.DataFrame(x)
        df['project'] = project

        if accumulate_duration:
            df['duration'] = df['duration'].cumsum()

        project_df.append(df)

    project_df = pd.concat(project_df).reset_index()
    
    return project_df
