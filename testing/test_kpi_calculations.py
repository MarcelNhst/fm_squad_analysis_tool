import pandas as pd
import sys
from pandas.testing import assert_frame_equal
import pytest
sys.path.append('H:/Python_Projects/fm_squad_analysis_tool/src/')

import kpi_calculations


def test_basic_kpi_calculations():
    df1 = pd.DataFrame({'Acc': [10, 0], 'Pac': [20, 10], 'Spd': [15.0, 5.0]})
    df2 = pd.DataFrame({'Acc': [10, 0], 'Pac': [20, 10]})

    df2['Spd'] = kpi_calculations.calculate_kpi_score(df2, ['Acc', 'Pac'], [], [])


    assert_frame_equal(df1, df2)


