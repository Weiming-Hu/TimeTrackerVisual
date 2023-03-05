#!/home/pi/venv_timetracker/bin/python3

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
# The main web GUI
#
# Usage: python main.py
#

import dash_bootstrap_components as dbc

from dash import Dash
from layout import panel_layout


# some external things
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
]

external_scripts = [
    'https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js',
]

# Main server
app = Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)

server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Time Tracker Visualization</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = panel_layout

from callbacks import *


if __name__ == '__main__':
    app.run_server(debug=True, port=41237)
    