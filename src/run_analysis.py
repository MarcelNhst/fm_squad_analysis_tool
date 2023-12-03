import pandas as pd
import glob
import os
import uuid
import logging
from datetime import datetime
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
squad_rawdata['gk_essential'] = (
    ( squad_rawdata['Agi'] + 
     squad_rawdata['Ref']) * 5)
squad_rawdata['gk_core'] = (
    ( squad_rawdata['1v1'] + 
     squad_rawdata['Ant'] + 
     squad_rawdata['Cmd'] + 
     squad_rawdata['Cnt'] + 
     squad_rawdata['Kic'] + 
     squad_rawdata['Pos']) * 3)
squad_rawdata['gk_secondary'] = (
    ( squad_rawdata['Acc'] +
     squad_rawdata['Aer'] +
     squad_rawdata['Cmp'] + 
     squad_rawdata['Dec'] + 
     squad_rawdata['Fir'] + 
     squad_rawdata['Han'] + 
     squad_rawdata['Pas'] + 
     squad_rawdata['Thr'] + 
     squad_rawdata['Vis']) * 1)
squad_rawdata['gk'] = ( ((squad_rawdata['gk_essential']) + (squad_rawdata['gk_core']) + (squad_rawdata['gk_secondary'])) / 37 )
squad_rawdata.gk= squad_rawdata.gk.round(1)

# calculates fb score
squad_rawdata['fb_essential'] = ( 
    squad_rawdata['Wor'] +
    squad_rawdata['Acc'] + 
    squad_rawdata['Pac'] + 
    squad_rawdata['Sta'])
squad_rawdata['fb_core'] = ( 
    squad_rawdata['Cro'] + 
    squad_rawdata['Dri'] + 
    squad_rawdata['Mar'] + 
    squad_rawdata['OtB'] + 
    squad_rawdata['Tck'] + 
    squad_rawdata['Tea'])
squad_rawdata['fb_secondary'] = ( 
    squad_rawdata['Agi'] + 
    squad_rawdata['Ant'] + 
    squad_rawdata['Cnt'] + 
    squad_rawdata['Dec'] + 
    squad_rawdata['Fir'] + 
    squad_rawdata['Pas'] + 
    squad_rawdata['Pos'] + 
    squad_rawdata['Tec'])
squad_rawdata['fb'] =( ( ( squad_rawdata['fb_essential'] * 5) + ( squad_rawdata['fb_core'] * 3) + (squad_rawdata['fb_secondary'] * 1)) / 46 )
squad_rawdata.fb= squad_rawdata.fb.round(1)

# calculates segundo volante on attack score
squad_rawdata['vol'] = ((
    ( squad_rawdata['Wor'] * 5) + 
    ( squad_rawdata['Pac'] * 5) + 
    ( squad_rawdata['Sta'] * 3) + 
    ( squad_rawdata['Pas'] * 3) + 
    ( squad_rawdata['Tck'] * 2) + 
    ( squad_rawdata['Ant'] * 2) + 
    ( squad_rawdata['Cnt'] * 2) + 
    ( squad_rawdata['Pos'] * 2) + 
    ( squad_rawdata['Tea'] * 2) + 
    ( squad_rawdata['Fir'] * 1) +
    ( squad_rawdata['Mar'] * 1) +
    ( squad_rawdata['Agg'] * 1) +
    ( squad_rawdata['Cmp'] * 1) +
    ( squad_rawdata['Dec'] * 1) +
    ( squad_rawdata['Str'] * 1) ) / 32)
squad_rawdata.vol= squad_rawdata.vol.round(1)

# calculates striker score
squad_rawdata['str_core'] = ( squad_rawdata['Cmp'] + squad_rawdata['Fin'] + squad_rawdata['OtB'] + squad_rawdata['Pac']) / 4
squad_rawdata['str_secondary'] = ( squad_rawdata['Acc'] + squad_rawdata['Agi'] + squad_rawdata['Ant']+ squad_rawdata['Bal']+ squad_rawdata['Dec']+ squad_rawdata['Dri']+ squad_rawdata['Fir']+ squad_rawdata['Pas']+ squad_rawdata['Sta']+ squad_rawdata['Tec']+ squad_rawdata['Wor']) / 11
squad_rawdata['str'] =( ( squad_rawdata['str_core'] * 0.5) + (squad_rawdata['str_secondary'] * 0.5))
squad_rawdata.str= squad_rawdata.str.round(1)

# calculates Goalkeeper_Defend score
squad_rawdata['gkd_key'] = ( squad_rawdata['Agi'] + squad_rawdata['Ref'] )
squad_rawdata['gkd_green'] = ( squad_rawdata['Aer'] + squad_rawdata['Cmd'] + squad_rawdata['Han'] + squad_rawdata['Kic'] + squad_rawdata['Cnt'] + squad_rawdata['Pos'] )
squad_rawdata['gkd_blue'] = ( squad_rawdata['1v1'] + squad_rawdata['Thr'] + squad_rawdata['Ant'] + squad_rawdata['Dec'] )
squad_rawdata['gkd'] =( ( ( squad_rawdata['gkd_key'] * 5) + (squad_rawdata['gkd_green'] * 3) + (squad_rawdata['gkd_blue'] * 1) ) / 32)
squad_rawdata.gkd= squad_rawdata.gkd.round(1)


# calculates Wide_centre_back_Support score
squad_rawdata['wcbs_key'] = ( squad_rawdata['Acc'] + squad_rawdata['Pac'] + squad_rawdata['Jum'] + squad_rawdata['Cmp'] )
squad_rawdata['wcbs_green'] = ( squad_rawdata['Dri'] + squad_rawdata['Hea'] + squad_rawdata['Mar'] + squad_rawdata['Tck'] + squad_rawdata['Pos'] + squad_rawdata['Str'] )
squad_rawdata['wcbs_blue'] = ( squad_rawdata['Cro'] + squad_rawdata['Fir'] + squad_rawdata['Pas'] + squad_rawdata['Tec'] + squad_rawdata['Agg'] + squad_rawdata['Ant'] + squad_rawdata['Bra'] + squad_rawdata['Cnt'] + squad_rawdata['Dec'] + squad_rawdata['OtB'] + squad_rawdata['Wor'] + squad_rawdata['Agi'] + squad_rawdata['Sta'] )
squad_rawdata['wcbs'] =( ( ( squad_rawdata['wcbs_key'] * 5) + (squad_rawdata['wcbs_green'] * 3) + (squad_rawdata['wcbs_blue'] * 1) ) / 51)
squad_rawdata.wcbs= squad_rawdata.wcbs.round(1)

# calculates Central_defender_Defend score
squad_rawdata['cdd_key'] = ( squad_rawdata['Acc'] + squad_rawdata['Pac'] + squad_rawdata['Jum'] + squad_rawdata['Cmp'] )
squad_rawdata['cdd_green'] = ( squad_rawdata['Hea'] + squad_rawdata['Mar'] + squad_rawdata['Tck'] + squad_rawdata['Pos'] + squad_rawdata['Str'] )
squad_rawdata['cdd_blue'] = ( squad_rawdata['Agg'] + squad_rawdata['Ant'] + squad_rawdata['Bra'] + squad_rawdata['Cnt'] + squad_rawdata['Dec'] )
squad_rawdata['cdd'] =( ( ( squad_rawdata['cdd_key'] * 5) + (squad_rawdata['cdd_green'] * 3) + (squad_rawdata['cdd_blue'] * 1) ) / 40)
squad_rawdata.cdd= squad_rawdata.cdd.round(1)

# calculates cb score
squad_rawdata['cb_core'] = ( squad_rawdata['Cmp'] + squad_rawdata['Hea'] + squad_rawdata['Jum']+ squad_rawdata['Mar']+ squad_rawdata['Pas']+ squad_rawdata['Pos']+ squad_rawdata['Str'] + squad_rawdata['Tck'] + squad_rawdata['Pac']) / 9
squad_rawdata['cb_secondary'] = ( squad_rawdata['Agg'] + squad_rawdata['Ant'] + squad_rawdata['Bra']+ squad_rawdata['Cnt']+ squad_rawdata['Dec']+ squad_rawdata['Fir']+ squad_rawdata['Tec']+ squad_rawdata['Vis']) / 8
squad_rawdata['cb'] =( ( squad_rawdata['cb_core'] * 0.75) + (squad_rawdata['cb_secondary'] * 0.25))
squad_rawdata.cb= squad_rawdata.cb.round(1)


# calculates Wing_back_Attack score
squad_rawdata['wba_key'] = ( squad_rawdata['Acc'] + squad_rawdata['Pac'] + squad_rawdata['Sta'] + squad_rawdata['Wor'] )
squad_rawdata['wba_green'] = ( squad_rawdata['Cro'] + squad_rawdata['Dri'] + squad_rawdata['Tck'] + squad_rawdata['Tec'] + squad_rawdata['OtB'] + squad_rawdata['Tea'] )
squad_rawdata['wba_blue'] = ( squad_rawdata['Fir'] + squad_rawdata['Mar'] + squad_rawdata['Pas'] + squad_rawdata['Ant'] + squad_rawdata['Cnt'] + squad_rawdata['Dec'] + squad_rawdata['Fla'] + squad_rawdata['Pos'] + squad_rawdata['Agi'] + squad_rawdata['Bal'] )
squad_rawdata['wba'] =( ( ( squad_rawdata['wba_key'] * 5) + (squad_rawdata['wba_green'] * 3) + (squad_rawdata['wba_blue'] * 1) ) / 48)
squad_rawdata.wba= squad_rawdata.wba.round(1)

# calculates Inverted_wing_back_Support score
squad_rawdata['iwbs_key'] = ( squad_rawdata['Acc'] + squad_rawdata['Pac'] + squad_rawdata['Sta'] + squad_rawdata['Wor'] )
squad_rawdata['iwbs_green'] = ( squad_rawdata['Fir'] + squad_rawdata['Pas'] + squad_rawdata['Tck'] + squad_rawdata['Cmp'] + squad_rawdata['Dec'] + squad_rawdata['Tea'] )
squad_rawdata['iwbs_blue'] = ( squad_rawdata['Mar'] + squad_rawdata['Tec'] + squad_rawdata['Ant'] + squad_rawdata['Cnt'] + squad_rawdata['OtB'] + squad_rawdata['Pos'] + squad_rawdata['Vis'] + squad_rawdata['Agi'] )
squad_rawdata['iwbs'] =( ( ( squad_rawdata['iwbs_key'] * 5) + (squad_rawdata['iwbs_green'] * 3) + (squad_rawdata['iwbs_blue'] * 1) ) / 46)
squad_rawdata.iwbs= squad_rawdata.iwbs.round(1)


# calculates Winger_Attack score
squad_rawdata['wa_key'] = ( squad_rawdata['Acc'] + squad_rawdata['Pac'] + squad_rawdata['Sta'] + squad_rawdata['Wor'] )
squad_rawdata['wa_green'] = ( squad_rawdata['Cro'] + squad_rawdata['Dri'] + squad_rawdata['Tec'] + squad_rawdata['Agi'] )
squad_rawdata['wa_blue'] = ( squad_rawdata['Fir'] + squad_rawdata['Pas'] + squad_rawdata['Ant'] + squad_rawdata['Fla'] + squad_rawdata['OtB'] + squad_rawdata['Bal'] )
squad_rawdata['wa'] =( ( ( squad_rawdata['wa_key'] * 5) + (squad_rawdata['wa_green'] * 3) + (squad_rawdata['wa_blue'] * 1) ) / 38)
squad_rawdata.wa= squad_rawdata.wa.round(1)

# calculates Inverted_winger_Support score
squad_rawdata['iws_key'] = ( squad_rawdata['Acc'] + squad_rawdata['Pac'] + squad_rawdata['Sta'] + squad_rawdata['Wor'] )
squad_rawdata['iws_green'] = ( squad_rawdata['Cro'] + squad_rawdata['Dri'] + squad_rawdata['Pas'] + squad_rawdata['Tec'] + squad_rawdata['Agi'] )
squad_rawdata['iws_blue'] = ( squad_rawdata['Fir'] + squad_rawdata['Lon'] + squad_rawdata['Cmp'] + squad_rawdata['Dec'] + squad_rawdata['OtB'] + squad_rawdata['Vis'] + squad_rawdata['Bal'] )
squad_rawdata['iws'] =( ( ( squad_rawdata['iws_key'] * 5) + (squad_rawdata['iws_green'] * 3) + (squad_rawdata['iws_blue'] * 1) ) / 42)
squad_rawdata.iws= squad_rawdata.iws.round(1)

# calculates Target_forward_Support score
squad_rawdata['tfs_key'] = ( squad_rawdata['Acc'] + squad_rawdata['Pac'] + squad_rawdata['Fin'] )
squad_rawdata['tfs_green'] = ( squad_rawdata['Hea'] + squad_rawdata['Bra'] + squad_rawdata['Tea'] + squad_rawdata['Bal'] + squad_rawdata['Jum'] + squad_rawdata['Str'] )
squad_rawdata['tfs_blue'] = ( squad_rawdata['Fir'] + squad_rawdata['Agg'] + squad_rawdata['Ant'] + squad_rawdata['Cmp'] + squad_rawdata['Dec'] + squad_rawdata['OtB'] )
squad_rawdata['tfs'] =( ( ( squad_rawdata['tfs_key'] * 5) + (squad_rawdata['tfs_green'] * 3) + (squad_rawdata['tfs_blue'] * 1) ) / 39)
squad_rawdata.tfs= squad_rawdata.tfs.round(1)

# calculates Poacher_Attack score
squad_rawdata['pa_key'] = ( squad_rawdata['Acc'] + squad_rawdata['Pac'] + squad_rawdata['Fin'] )
squad_rawdata['pa_green'] = ( squad_rawdata['Ant'] + squad_rawdata['Cmp'] + squad_rawdata['OtB'] )
squad_rawdata['pa_blue'] = ( squad_rawdata['Fir'] + squad_rawdata['Hea'] + squad_rawdata['Tec'] + squad_rawdata['Dec'] )
squad_rawdata['pa'] =( ( ( squad_rawdata['pa_key'] * 5) + (squad_rawdata['pa_green'] * 3) + (squad_rawdata['pa_blue'] * 1) ) / 28)
squad_rawdata.pa= squad_rawdata.pa.round(1)

# calculates dm score
squad_rawdata['dm'] = ((
    ( squad_rawdata['Wor'] * 5) + 
    ( squad_rawdata['Pac'] * 5) + 
    ( squad_rawdata['Sta'] * 3) + 
    ( squad_rawdata['Pas'] * 3) + 
    ( squad_rawdata['Tck'] * 2) + 
    ( squad_rawdata['Ant'] * 2) + 
    ( squad_rawdata['Cnt'] * 2) + 
    ( squad_rawdata['Pos'] * 2) + 
    ( squad_rawdata['Bal'] * 2) + 
    ( squad_rawdata['Agi'] * 2) + 
    ( squad_rawdata['Tea'] * 1) + 
    ( squad_rawdata['Fir'] * 1) +
    ( squad_rawdata['Mar'] * 1) +
    ( squad_rawdata['Agg'] * 1) +
    ( squad_rawdata['Cmp'] * 1) +
    ( squad_rawdata['Dec'] * 1) +
    ( squad_rawdata['Str'] * 1) ) / 35)
squad_rawdata.dm= squad_rawdata.dm.round(1)

# calculates winger score
squad_rawdata['w_core'] = ( squad_rawdata['Acc'] + squad_rawdata['Cro'] + squad_rawdata['Dri']+ squad_rawdata['OtB']+ squad_rawdata['Pac']+ squad_rawdata['Tec']) / 6
squad_rawdata['w_secondary'] = ( squad_rawdata['Agi'] + squad_rawdata['Fir'] + squad_rawdata['Pas']+ squad_rawdata['Sta']+ squad_rawdata['Wor']) / 5
squad_rawdata['w'] =( ( squad_rawdata['w_core'] * 0.75) + (squad_rawdata['w_secondary'] * 0.25))
squad_rawdata.w= squad_rawdata.w.round(1)

# calculates inverted winger score 
squad_rawdata['amrl'] = ((
    ( squad_rawdata['Acc'] * 5) + 
    ( squad_rawdata['Pac'] * 5) + 
    ( squad_rawdata['Wor'] * 5) + 
    ( squad_rawdata['Dri'] * 3) + 
    ( squad_rawdata['Pas'] * 3) + 
    ( squad_rawdata['Tec'] * 3) + 
    ( squad_rawdata['OtB'] * 3) +
    ( squad_rawdata['Cro'] * 1) + 
    ( squad_rawdata['Fir'] * 1) +
    ( squad_rawdata['Cmp'] * 1) +
    ( squad_rawdata['Dec'] * 1) +
    ( squad_rawdata['Vis'] * 1) +
    ( squad_rawdata['Agi'] * 1) + 
    ( squad_rawdata['Sta'] * 1))/ 34)
squad_rawdata.amrl= squad_rawdata.amrl.round(1)

# builds squad dataframe using only columns that will be exported to HTML
squad = squad_rawdata[['Inf','Name','Age','Club','Transfer Value','Salary','Nat','Position','Personality','Media Handling','Left Foot', 'Right Foot','Spd','Jum','Str','Work','Height','gk','cb','fb', 'dm','vol', 'str']]

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