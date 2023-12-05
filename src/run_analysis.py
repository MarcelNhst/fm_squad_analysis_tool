import pandas as pd
import glob
import os
import uuid
import logging
from datetime import datetime
from kpi_calculations import calculate_kpi_score, calculate_custom_kpi_score
pd.set_option('display.max_columns', None)

path = 'H:/Python_Projects/fm_squad_analysis_tool/input'

now = datetime.now()
now_str = now.strftime("%Y%m%d%H%M%S")
logging.basicConfig(filename='log/' + now_str +'.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


list_of_files = glob.glob(os.path.join(path, '*'))
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)
logging.info('Processing file ' + latest_file)

# Read HTML file exported by FM - in this case an example of an output from the squad page
# This reads as a list, not a dataframe
squad_rawdata_list = pd.read_html(latest_file, header=0, encoding="utf-8", keep_default_na=False)

# turn the list into a dataframe
squad_rawdata = squad_rawdata_list[0]

squad_rawdata['Spd'] = ( squad_rawdata['Pac'] + squad_rawdata['Acc'] ) / 2
squad_rawdata['Work'] = ( squad_rawdata['Wor'] + squad_rawdata['Sta'] ) / 2
squad_rawdata['SetP'] = ( squad_rawdata['Jum'] + squad_rawdata['Bra'] ) / 2

# calculates gk score
squad_rawdata['gk'] = calculate_kpi_score(squad_rawdata, ['Agi', 'Ref'], ['1v1', 'Ant', 'Cmd', 'Cnt', 'Kic', 'Pos'], ['Acc', 'Aer', 'Cmp', 'Dec', 'Fir', 'Han', 'Pas', 'Thr', 'Vis'])

# calculates fb score
squad_rawdata['fb'] = calculate_kpi_score(squad_rawdata, ['Wor', 'Acc', 'Pac', 'Sta'], ['Cro', 'Dri', 'Mar', 'OtB', 'Tck', 'Tea'], ['Agi', 'Ant', 'Cnt', 'Dec', 'Fir', 'Pas', 'Pos', 'Tec'])

# calculates segundo volante on attack score
squad_rawdata['vol'] = calculate_custom_kpi_score(squad_rawdata, ['Wor', 'Pac'], ['Sta', 'Pas'], ['Tck', 'Ant', 'Cnt', 'Pos', 'Tea'], ['Fir', 'Mar', 'Agg', 'Cmp', 'Dec', 'Str'])

# calculates Advanced_forward_Attack score
squad_rawdata['af'] = calculate_kpi_score(squad_rawdata, ['Acc', 'Pac', 'Fin'], ['Dri', 'Fir', 'Tec', 'Cmp', 'OtB'], ['Pas', 'Ant', 'Dec', 'Wor', 'Agi', 'Bal', 'Sta'])

# calculates Ball_playing_defender_Defend score
squad_rawdata['bpd'] = calculate_kpi_score(squad_rawdata, ['Acc', 'Pac', 'Jum', 'Cmp'], ['Hea', 'Mar', 'Pas', 'Tck', 'Pos', 'Str'], ['Fir', 'Tec', 'Agg', 'Ant', 'Bra', 'Cnt', 'Dec', 'Vis'])


# builds squad dataframe using only columns that will be exported to HTML
squad = squad_rawdata[['Inf','Name','Age','Club','Transfer Value','Salary','Nat','Position','Personality','Media Handling','Left Foot', 'Right Foot','Spd','Jum','Str','Work','Height','gk', 'bpd', 'fb','vol', 'af']]

logging.info('Produced table with ' + str(squad.shape[0]) + ' entries and ' + str(squad.shape[1]) + ' columns')
# taken from here: https://www.thepythoncode.com/article/convert-pandas-dataframe-to-html-table-python
# creates a function to make a sortable html export

def generate_html(dataframe: pd.DataFrame):
    # get the table HTML from the dataframe
    table_html = dataframe.to_html(table_id="table", index=False)
    # construct the complete HTML with jQuery Data tables
    # You can disable paging or enable y scrolling on lines 20 and 21 respectively
    html = f"""
    <html>
    <header>
        <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
    </header>
    <body>
    {table_html}
    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready( function () {{
            $('#table').DataTable({{
                paging: false,
                order: [[12, 'desc']],
                // scrollY: 400,
            }});
        }});
    </script>
    </body>
    </html>
    """
    # return the html
    return html





latest_file_split = latest_file.split("\\")

filename = "output/" + now_str + '_' + latest_file_split[1]
print(filename)
logging.info('Writing result to ' + filename)

html = generate_html(squad)
open(filename, "w", encoding="utf-8").write(html)
logging.info('Writing result completed successfully')