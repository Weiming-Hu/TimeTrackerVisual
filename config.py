import os

# Time zone
MY_TZ = 'America/Los_Angeles'

# Root directory
ROOT_DIR = os.path.expanduser('~/github/TimeTrackerVisual')

# Directory for tables
TABLE_DIR = os.path.join(ROOT_DIR, 'tables')

# Table files to read and the included columns
TABLE_FILES = {
    # Key name: [file name, [column names]]
    
    'work_interval': ['oc_timetracker_work_interval.csv',
                      ['id', 'name', 'details', 'project_id', 'user_uid', 'start', 'duration', 'running', 'lineend']],
    
    'workint_to_tag': ['oc_timetracker_workint_to_tag.csv',
                       ['id', 'work_interval_id', 'tag_id', 'created_at']],
    
    'tag': ['oc_timetracker_tag.csv',
            ['id', 'name', 'user_uid', 'created_at']],
    
    'project': ['oc_timetracker_project.csv',
                ['id', 'name', 'client_id', 'created_by_user_uid', 'locked', 'archived', 'created_at', 'color']],
    
    'client': ['oc_timetracker_client.csv',
               ['id', 'name', 'created_at']],
}

# Set figure margin
FIG_MARGINS = {
    't': 20,
    'r': 10,
    'l': 10,
    'b': 20,
}