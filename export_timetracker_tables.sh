#!/bin/bash

# The output directory for storing CSV files
out_dir=./tables

for table in oc_timetracker_client oc_timetracker_goal oc_timetracker_lpa_tags oc_timetracker_project oc_timetracker_tag oc_timetracker_timeline oc_timetracker_timeline_entry oc_timetracker_user_to_client oc_timetracker_user_to_project oc_timetracker_work_interval oc_timetracker_workint_to_tag; do
    echo Processing table: $table
    command="SELECT * FROM $table INTO OUTFILE '/tmp/$table.csv'"
    sudo mysql -D nextcloud -e "$command"
    sudo mv /tmp/$table.csv $out_dir
    sudo chown pi:pi $out_dir/$table.csv
done

echo Done!

